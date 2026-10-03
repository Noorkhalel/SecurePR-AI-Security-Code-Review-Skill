# Community and Pro: proposed product model

**Status:** v1.0.0 ships as SecurePR Community under the existing [MIT license](LICENSE).
“Lite” may be used as a listing alias for Community, not a separate reduced-security
edition. SecurePR Pro is a proposal, not an available product, hosted service or
promised entitlement. No price, marketplace integration or support SLA is announced.

## What remains in Community

Keep evidence requirements, confidence/severity rules, source-to-sink reasoning,
multi-file analysis, authorization/BOLA guidance, prompt-injection defenses,
safe static defaults, PR/repository/snippet review, fix guidance, regression-test
generation, current JS/TS/Express/Next.js references, helpers and evaluation assets.
Do not gate correct authorization advice, remove safe examples, weaken redaction
or suppress known security fixes to encourage an upgrade. Community remains useful
on its own. The host model and its usage costs are separate from this repository.

## Proposed differentiation

| Offering | Community v1.0.0 today | Candidate Pro value, not implemented |
| --- | --- | --- |
| Review methodology | Full current evidence, confidence and control analysis | Maintained organization-specific policies with conflict handling and auditable provenance |
| Multi-file review | Agent-directed cross-file reasoning within host context | Explicit scope budgeting, review queues and resumable large-repository coverage records |
| Framework/language packs | JS/TS, Node.js, Express, Next.js | Separately tested Python/Java/Go/PHP packs and versioned framework integrations |
| API workflows | Current auth, tenancy, webhook and business-logic guidance | Domain-specific workflow packs with independently curated evaluation sets |
| Remediation | Scoped patch guidance and regression-test generation | Opt-in, isolated patch validation and human approval workflows |
| Reporting | Markdown templates and evidence-bound JSON validation | Organization templates, traceability exports and evidence retention controls |
| PR/CI integration | Local helpers; CI validates this skill's artifacts | Explicitly authorized review orchestration, PR comments, deduplication and approval gates |
| Support | Public contribution/security processes; no SLA | Contracted onboarding, configuration assistance, maintenance and support terms |

Automation and maintenance are stronger paid differentiators than a larger prompt
file. Evaluate integrations on actual repositories before claiming improved
detection. Existing multi-file reasoning is not a future paid-only capability.
The project's current CI does not review customer pull requests.

## Delivery and commercial validation

Start with an optional, separately documented integration/policy pack or onboarding
service alongside the unchanged Community repository. Define exactly what is
delivered, compatible host versions, update duration, support boundaries and
refund/cancellation terms before accepting orders. Choose distribution channels
only after checking their current file formats, terms and payment capabilities.
This document asserts no marketplace approval or checkout availability.

Before pricing, interview prospective AppSec teams and maintainers, run consented
pilots, and measure setup time, review usefulness, false-positive burden and patch
acceptance. Price against the actual maintenance/integration service and support
costs; no willingness-to-pay or revenue claim is established here.

## Security, licensing and release commitments

Keep Community security corrections public and timely. New automation must default
to read-only, use scoped credentials, avoid repository execution and source upload
without explicit action, and disclose the model provider's data handling. A future
hosted offering would need its own documented retention/deletion controls, tenant
isolation, incident process and terms before launch; none is supplied by this skill.

Retain the existing MIT notices with Community distribution. Any future proprietary
additions or service terms need a clearly separate license/contract and ownership
review; this proposal does not alter existing permissions or grant exclusivity.
Do not sell the present community files as a different detection engine, imply
certification, or promise fixes are safe without application-specific verification.

Release Pro only with its own versioned deliverables, acceptance tests, accurate
evaluation population, security review and supported-host matrix. Publish which
capabilities are measured, which are guidance, and which remain planned.
