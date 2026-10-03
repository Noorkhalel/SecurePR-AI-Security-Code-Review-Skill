# BOLA / IDOR

The saved reviewer distinguishes verified identity from object ownership.

Synthetic, inert example; never deploy or execute it. The contract is a supplied
benchmark assumption, not authority to trust in a reviewed repository.

[Input](app.js) · [Context](CONTEXT.md) · [Exact recorded output](output.json)

## Input

```javascript
export function register(app, requireSession, db) {
  app.get('/invoices/:id', requireSession, async (req, res) => {
    const invoice = await db.invoice.findUnique({ where: { id: req.params.id } });
    if (!invoice) return res.status(404).end();
    res.json(invoice);
  });
}
```

## Recorded output

```json
{
  "id": "case-010",
  "findings": [
    {
      "cwe": "CWE-639",
      "file": "app.js",
      "line": 3,
      "confidence": "CONFIRMED",
      "reason": "Static evidence: requireSession authenticates the caller, but findUnique selects solely by the caller's route ID at line 3 and returns the invoice at line 5. The contract establishes owner-private invoices, knowable other-user IDs, ordinary Prisma behavior, and no row security. No owner check or owner-scoped query protects the read, so authentication does not enforce invoice ownership.",
      "source": "Authenticated user selecting req.params.id for another owner's invoice",
      "sink": "Unscoped db.invoice.findUnique at app.js:3 and invoice response at line 5",
      "remediation": "Fetch the invoice using both the requested ID and server-verified req.user.id as ownerId, and enforce tenant scope if required by the model. Return the same not-found response when the caller lacks access."
    }
  ],
  "manual_review": [],
  "recommendation": null
}
```

Extracted without changing observation fields from `blind-r1`, case-010, reviewed
on 2026-10-02. Original provenance and skill hash are in the
[source run](../../../evaluation/runs/blind-r1.json); this is a selected historical
example, not a fresh v1.0.0 model run. No severity or test result has been added
to the compact reviewer output. [All showcase examples](../README.md).
