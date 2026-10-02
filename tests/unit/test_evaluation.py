import copy
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('evaluate_test',ROOT/'tools/evaluate.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)

class Scoring(unittest.TestCase):
    def setUp(self):
        self.manifest={'version':'1.0.0','cases':[
          {'id':'a','mode':'full','expected':[{'cwe':'CWE-89','file':'a.js','line':3}],'manual_review_required':False},
          {'id':'b','mode':'full','expected':[],'manual_review_required':False},
          {'id':'c','mode':'full','expected':[],'manual_review_required':True}]}
        self.finding={'cwe':'CWE-89','file':'a.js','line':3,'confidence':'CONFIRMED','reason':'direct input to SQL text','source':'query input','sink':'SQL driver','remediation':'bind parameter'}
        self.obs={'run':{'id':'harness-unit','kind':'harness-self-test','reviewer':'unit assertions','skill_revision':'test','date':'2026-10-02','notes':'Synthetic scorer unit test; NOT detection metrics.'},
                  'cases':[{'id':'a','findings':[self.finding],'manual_review':[],'recommendation':None},
                           {'id':'b','findings':[],'manual_review':[],'recommendation':None},
                           {'id':'c','findings':[],'manual_review':['Need policy wrapper.'],'recommendation':None}]}
    def test_confusion_matrix(self):
        score=e.score(self.manifest,self.obs)
        self.assertEqual((score['true_positives'],score['false_positives'],score['true_negatives'],score['false_negatives']),(1,0,1,0))
        self.assertEqual(score['f1'],1.0);self.assertEqual(score['ambiguous_abstentions'],1)
    def test_false_positive_and_negative(self):
        self.obs['cases'][0]['findings'][0]['cwe']='CWE-79'
        score=e.score(self.manifest,self.obs)
        self.assertEqual((score['true_positives'],score['false_positives'],score['false_negatives']),(0,1,1))
    def test_duplicate_finding_is_false_positive(self):
        self.obs['cases'][0]['findings'].append(copy.deepcopy(self.finding))
        score=e.score(self.manifest,self.obs)
        self.assertEqual(score['true_positives'],1);self.assertEqual(score['false_positives'],1)
    def test_missing_case_rejected(self):
        self.obs['cases'].pop()
        with self.assertRaises(e.securepr.Rejected):e.score(self.manifest,self.obs)
    def test_duplicate_case_rejected(self):
        self.obs['cases'].append(self.obs['cases'][0])
        with self.assertRaises(e.securepr.Rejected):e.score(self.manifest,self.obs)
    def test_duplicate_manifest_case_rejected(self):
        self.manifest['cases'].append(copy.deepcopy(self.manifest['cases'][0]))
        with self.assertRaises(e.securepr.Rejected):e.score(self.manifest,self.obs)
    def test_unmatched_line_is_miss(self):
        self.obs['cases'][0]['findings'][0]['line']=900
        score=e.score(self.manifest,self.obs);self.assertEqual(score['false_negatives'],1)
    def test_empty_predictions_not_perfect(self):
        self.obs['cases'][0]['findings']=[]
        score=e.score(self.manifest,self.obs);self.assertIsNone(score['precision']);self.assertEqual(score['recall'],0)
    def test_ambiguous_overclaim_penalized(self):
        self.obs['cases'][2]['findings']=[copy.deepcopy(self.finding)]
        score=e.score(self.manifest,self.obs);self.assertEqual(score['false_positives'],1)
    def test_missing_ambiguity_followup(self):
        self.obs['cases'][2]['manual_review']=[]
        self.assertEqual(e.score(self.manifest,self.obs)['ambiguous_missing_followup'],1)
    def test_low_confidence_is_not_true_positive(self):
        self.obs['cases'][0]['findings'][0]['confidence']='MEDIUM CONFIDENCE'
        with self.assertRaises(e.securepr.Rejected):e.score(self.manifest,self.obs)

if __name__=='__main__':unittest.main()
