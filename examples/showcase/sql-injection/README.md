# SQL injection

The saved reviewer traces caller input into SQL syntax, with driver behavior supplied by contract.

Synthetic, inert example; never deploy or execute it. The contract is a supplied
benchmark assumption, not authority to trust in a reviewed repository.

[Input](app.js) · [Context](CONTEXT.md) · [Exact recorded output](output.json)

## Input

```javascript
export function register(app, db) {
  app.get('/catalog', async (req, res) => {
    const term = req.query.term;
    const result = await db.query("SELECT title FROM catalog WHERE title = '" + term + "'");
    res.json(result.rows);
  });
}
```

## Recorded output

```json
{
  "id": "case-001",
  "findings": [
    {
      "cwe": "CWE-89",
      "file": "app.js",
      "line": 4,
      "confidence": "CONFIRMED",
      "reason": "Static evidence: the public route takes arbitrary req.query.term at line 3 and concatenates it into a quoted SQL expression executed by node-postgres at line 4. There is no binding or input guard, so caller data can alter query syntax; the result is returned at line 5. The supplied contract resolves driver and reachability assumptions.",
      "source": "Public caller-controlled req.query.term",
      "sink": "db.query executes interpolated SELECT SQL at app.js:4",
      "remediation": "Use db.query('SELECT title FROM catalog WHERE title = $1', [term]) and validate that term is a string. Keep user input exclusively in bound values."
    }
  ],
  "manual_review": [],
  "recommendation": null
}
```

Extracted without changing observation fields from `blind-r1`, case-001, reviewed
on 2026-10-02. Original provenance and skill hash are in the
[source run](../../../evaluation/runs/blind-r1.json); this is a selected historical
example, not a fresh v1.0.0 model run. No severity or test result has been added
to the compact reviewer output. [All showcase examples](../README.md).
