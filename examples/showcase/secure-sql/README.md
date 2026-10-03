# Secure parameterized SQL

The actual result contains no findings and no manual-review request. This is scoped restraint, not a blanket security certification.

Synthetic, inert example; never deploy or execute it. The contract is a supplied
benchmark assumption, not authority to trust in a reviewed repository.

[Input](app.js) · [Context](CONTEXT.md) · [Exact recorded output](output.json)

## Input

```javascript
export function register(app, db) {
  app.get('/catalog', async (req, res) => {
    const result = await db.query('SELECT title FROM catalog WHERE title = $1', [req.query.term]);
    res.json(result.rows);
  });
}
```

## Recorded output

```json
{
  "id": "case-021",
  "findings": [],
  "manual_review": [],
  "recommendation": null
}
```

Extracted without changing observation fields from `blind-r1`, case-021, reviewed
on 2026-10-02. Original provenance and skill hash are in the
[source run](../../../evaluation/runs/blind-r1.json); this is a selected historical
example, not a fresh v1.0.0 model run. No severity or test result has been added
to the compact reviewer output. [All showcase examples](../README.md).
