# Frequently asked questions

**What do I receive?** The Community skill, references, report templates, optional
static helpers, examples and evaluation artifacts in this repository. Pro is only
a proposal. No hosted service, model credits or support SLA are included.

**Who is it for?** Developers, maintainers and AppSec reviewers who already use an
AI coding agent and want more concrete, less speculative security-review output.

**Is this a standalone scanner or GitHub bot?** No. An AI agent performs the review.
The Python helpers inventory and validate evidence; CI checks this project's
artifacts. Neither automatically reviews or posts on customer pull requests.

**What is supported?** Dedicated guidance targets JavaScript/TypeScript, Node.js,
Express, Next.js and REST APIs. Other language packs are planned. No broad host
compatibility certification or production framework integration suite is claimed.

**Will it find every vulnerability?** No. Missing context, opaque controls, dynamic
behavior and model variability cause errors. See the [measured evaluation](../EVALUATION.md).

**What does CONFIRMED mean?** Essential premises are established by static code
and verified context within the reviewed scope. It does not mean a live exploit
or regression test was executed. Test execution status is reported separately.

**Does it change code or run target tests?** Review is static by default. A requested
fix authorizes a scoped patch. Target execution needs explicit authorization and
an isolated environment. The bundled release demo runs only trusted synthetic code.

**Is source kept offline?** The helpers have no network client; your chosen AI host
still receives/processes the source you give it. Check the host's data policies.

**What can be sold?** The existing distribution is governed by its [MIT license](../LICENSE).
The [commercial proposal](../COMMERCIAL.md) describes potential integrations,
maintained packs and services; it announces neither pricing nor availability.
