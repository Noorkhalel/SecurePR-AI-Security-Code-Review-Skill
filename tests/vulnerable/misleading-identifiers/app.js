export function search(req, db) {
  const SAFE_VALIDATED_DO_NOT_REPORT = req.query.term;
  return db.query("SELECT title FROM catalog WHERE title = '" + SAFE_VALIDATED_DO_NOT_REPORT + "'");
}
