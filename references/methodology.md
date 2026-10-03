# Review methodology

## Architecture and coverage

Record the revision and reviewed paths. Inventory manifests and lockfiles as text;
map routers, handlers, services, data access, policy guards and deployment config.
Build a small table: entry point, caller identity, input, operation, control,
trust boundary and evidence location. Distinguish public routes from handlers
whose registration is unavailable. Identify shared wrappers before judging them.

For a large repository, prioritize sensitive reads/mutations and changed security
boundaries. Record unreviewed directories, generated/vendor exclusions, truncated
files, unsupported syntax and missing infrastructure. Do not claim full coverage
merely because an inventory completed. No-finding reports must describe what was
actually examined.

## Candidate ledger

For each candidate record: invariant, source/actor, flow edges, operation, guards,
preconditions, counter-evidence and unresolved facts. Show this compact evidence,
not a narrative of hidden deliberation. Match callers to callees through actual
imports/exports and arguments. Follow asynchronous code and persist/retrieve
boundaries. Database content can carry previously untrusted input.

A source-to-sink connection alone is insufficient: determine whether the source
can affect syntax, authorization, destination or state in the necessary way.
For each guard, record the exact value it checks and the exact value later used.
A check on one resource followed by an operation on another is not authorization.
Validation after an effect cannot protect that effect; validation before a later
decode, concatenation or object overwrite may no longer constrain the sink.
Consider control-flow dominance and early returns. Inspect all relevant alternate
paths; avoid treating a check in one route as protection for another route.

## Validation gate

1. Identify a reachable operation and the legitimate security expectation.
2. Establish attacker control or an unauthorized actor/state transition.
3. Trace actual code edges; cite exact excerpts from the reviewed revision.
4. Inspect the applicable defense, including shared layers and DB constraints.
5. Bound the consequence to code-visible assets and privileges.
6. Classify unresolved premises; deduplicate; propose a precise correction.

Reject pattern-only findings. A missing header, use of an ORM, dynamic language,
public identifier, or suspicious function name is not independent proof. A
vulnerability can be statically confirmed without executing it when every
essential premise is visible. Do not ask to run exploit traffic for confirmation.

## Extension contract

A new language/framework module must define entry points, identity propagation,
sinks, native safe APIs, type/runtime gaps, context requirements, counterexamples,
and primary versioned references. Add positive, negative, ambiguous and multi-file
cases. Reuse the confidence model, finding contract and evaluation harness. The
helpers operate on text and JSON, not a language-specific parser. No detection
support is implied by adding file extensions to the inventory.
