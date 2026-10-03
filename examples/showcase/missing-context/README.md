# Missing authorization context

The actual result requests the absent policy wrapper and storage controls instead of confirming a vulnerability.

Synthetic, inert example; never deploy or execute it. The contract is a supplied
benchmark assumption, not authority to trust in a reviewed repository.

[Input](route.js) · [Context](CONTEXT.md) · [Exact recorded output](output.json)

## Input

```javascript
import { protectedRoute } from './missing-policy.js';
export const handler = protectedRoute(async (req, res, db) => {
  res.json(await db.invoice.findUnique({ where: { id: req.params.id } }));
});
```

## Recorded output

```json
{
  "id": "case-036",
  "findings": [],
  "manual_review": [
    "MEDIUM CONFIDENCE: route.js:3 looks up a private invoice by the caller-selected id, but protectedRoute, database extensions and row-security rules are missing. Supply those controls and actor/ownership policy to determine whether every lookup is restricted to the authorized owner or tenant."
  ],
  "recommendation": null
}
```

Extracted without changing observation fields from `blind-r1`, case-036, reviewed
on 2026-10-02. Original provenance and skill hash are in the
[source run](../../../evaluation/runs/blind-r1.json); this is a selected historical
example, not a fresh v1.0.0 model run. No severity or test result has been added
to the compact reviewer output. [All showcase examples](../README.md).
