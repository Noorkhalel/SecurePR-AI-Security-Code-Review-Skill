# Install SecurePR v1.0.0

Use an AI coding agent that can load a trusted local skill and read authorized
source files. Review the skill before granting access. Obtain the tagged source:

```sh
git clone --branch v1.0.0 --depth 1 https://github.com/Noorkhalel/SecurePR-AI-Security-Code-Review-Skill.git securepr
```

Put the complete `securepr` folder in your client's documented skill directory,
or explicitly provide its SKILL.md path. If using a GitHub source archive, rename
the extracted top-level directory to `securepr`. Keep all relative references
intact; do not install only SKILL.md. Client discovery and invocation syntax vary.

Confirm the agent can read the trusted skill and a linked reference, then ask:

```text
Use SecurePR to review this PR against its base revision. Inspect surrounding
authorization controls, report introduced issues with evidence, and state gaps.
```

No npm install, package scripts, SecurePR API key or background service is required.
Your host may require its own account/model access. Optional helpers require
Python 3.10+ on POSIX; maintained demonstrations use Node.js 20+ with built-ins.
Helpers do not call a model. See [usage and safety](../README.md) and the
[reproducible demo](../examples/release-demo/README.md).
