# Limitations

- This is an agent workflow, not a standalone scanner, AST/taint engine or automatic fixer.
- Dedicated guidance focuses on JS/TS, Node.js, Express and Next.js; language expansion is planned.
- Findings depend on available code, trustworthy policy context and the host model.
- Static confirmation does not establish a live exploit, severity calibration or patch compatibility.
- Large repositories, dynamic behavior, opaque wrappers and infrastructure policies may exceed context.
- Prompt-injection defenses and best-effort redaction cannot guarantee safety.
- Saved evaluation replay verifies artifacts and scoring, not fresh model behavior.
- Synthetic results are not production accuracy; no independent human certification,
  held-out production benchmark or broad framework integration coverage is claimed.
- No automated PR posting, hosted service, enterprise controls or Pro entitlement ships in v1.0.0.
- Windows helper support is not implemented; optional helpers require POSIX/Python 3.10+.

Use SecurePR alongside SAST, DAST, manual code review and penetration testing.
Review proposed patches and validate them in the actual application's isolated test
environment before relying on them. [Full evaluation and populations](../EVALUATION.md).
