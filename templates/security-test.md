# Security regression test specification

- **Finding and invariant:** identify the policy/behavior being protected.
- **Layer:** unit, handler, integration or controlled concurrency; explain coverage.
- **Preconditions:** synthetic actors, roles, tenants, data and relevant state.
- **Valid control:** legitimate input/actor succeeds with the intended result.
- **Negative behavior:** forbidden input/actor is rejected with no sensitive output.
- **Side effects:** assert no unauthorized mutation, request, log or file operation.
- **Boundary cases:** absent credentials, other tenant, unexpected type or replay
  where relevant; avoid unrelated exhaustive testing.
- **Isolation:** no production connection, real secrets or operational payloads.
- **Status:** proposed / executed-pass / executed-fail / blocked, with evidence.
- **Limits:** what mocked adapters and absent integration layers leave unproven.

Only claim red/green after running the same assertion on original and fixed logic.
