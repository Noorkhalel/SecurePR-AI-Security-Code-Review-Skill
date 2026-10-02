# Primary sources and taxonomy

Documentation checked on 2026-10-02. Recheck version-sensitive behavior when
reviewing a particular application. These references informed original guidance;
no copied implementation or third-party code is bundled.

| Source | Purpose |
| --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | Frontmatter, progressive disclosure and portable skill structure |
| [Express security](https://expressjs.com/en/advanced/best-practice-security/) | Production controls and framework review |
| [Express proxy guide](https://expressjs.com/en/guide/behind-proxies/) | Forwarded header trust assumptions |
| [Next.js data security](https://nextjs.org/docs/app/guides/data-security) | Server/client data and action boundaries |
| [Next.js authentication](https://nextjs.org/docs/app/guides/authentication) | Server-side identity and authorization |
| [Node child_process](https://nodejs.org/api/child_process.html) | Shell versus argument-array semantics |
| [OWASP authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | Object/action policy review |
| [OWASP SSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) | URL/redirect/DNS control boundaries |
| [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/) | Edition-qualified awareness categories |
| [OWASP API Top 10:2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) | API object/property/function authorization |
| [MITRE CWE-639](https://cwe.mitre.org/data/definitions/639.html) | User-controlled object-key authorization |

## Selected root-cause mappings

Use a specific root cause only if supported, rather than stacking overlapping
CWEs. CWE syntax validation cannot prove a correct mapping. CWE-840 is a category,
not a substitute for a concrete business-logic weakness. A finding may omit OWASP
when no precise mapping is useful.

| Weakness | CWE | Optional awareness mapping |
| --- | --- | --- |
| SQL syntax injection | CWE-89 | A05:2025 Injection |
| OS command injection | CWE-78 | A05:2025 Injection |
| XSS | CWE-79 | A05:2025 Injection |
| SSRF | CWE-918 | A01:2025 Broken Access Control / API7:2023 |
| Path traversal | CWE-22 | A01:2025 Broken Access Control |
| Dangerous file upload | CWE-434 | Context-dependent |
| User-controlled key authorization bypass | CWE-639 | API1:2023 Broken Object Level Authorization |
| Missing function authorization | CWE-862 | API5:2023 Broken Function Level Authorization |
| Unsafe attribute modification | CWE-915 | API3:2023 Broken Object Property Level Authorization |
| Sensitive logging | CWE-532 | Context-dependent |
| Hardcoded cryptographic key | CWE-321 | A04:2025 Cryptographic Failures |
| Improper signature verification | CWE-347 | Context-dependent |
| Insufficient data-origin authenticity | CWE-345 | Context-dependent |
| Open redirect | CWE-601 | Context-dependent |
| Externally controlled assumed-immutable parameter | CWE-472 | Context-dependent |
| Weak PRNG for security | CWE-338 | A04:2025 Cryptographic Failures |
| Query-logic injection | CWE-943 | A05:2025 Injection |

Do not reuse A03:2021 for Injection while calling it 2025: the editions differ.
A10:2021 SSRF was consolidated into A01:2025; API7:2023 remains a separate API label.
