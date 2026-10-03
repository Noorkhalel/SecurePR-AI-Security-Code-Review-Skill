# Recorded review examples

Four small synthetic inputs with **unchanged actual reviewer observations**, suitable
for a short walkthrough or screenshot. Each includes its application contract;
show that limitation alongside the output. No credentials or customer data appear.

| Example | What the saved review does |
| --- | --- |
| [BOLA / IDOR](bola/README.md) | Explains why authentication does not enforce ownership |
| [SQL injection](sql-injection/README.md) | Traces caller input into query syntax |
| [Secure parameterized SQL](secure-sql/README.md) | Reports no material finding |
| [Missing context](missing-context/README.md) | Requests the policy wrapper and storage controls |

These are selected extracts from the historical 49-case `blind-r1` run, not four
additional measurements. Exact case IDs and source paths are retained in
[provenance](provenance.json). There are no live endpoints or executable demos in
this directory. No secure-system certification is implied by an empty findings list.
For a before/after PR walkthrough with runnable trusted regression tests, see the
[release demo](../release-demo/README.md).
