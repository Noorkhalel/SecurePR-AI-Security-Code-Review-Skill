# XSS and browser output

Establish the browser sink and output context: HTML text, attribute, URL,
JavaScript, CSS or DOM. Trace stored content back to a user-controlled write where
possible. Storage does not make content trusted. Identify the rendering response
and content type; a JSON response is not automatically HTML execution.

Review raw HTML sinks, dangerouslySetInnerHTML, template escaping overrides and
unsafe URL schemes. React text interpolation normally escapes text; do not report
it as XSS. A parameterized database query prevents SQL syntax injection, not XSS
at a later HTML sink. Encoding for HTML text is not interchangeable with script
or URL context. Sanitizer name/comments are insufficient; inspect its actual
implementation/configuration and transformations after it.

Treat CSP as defense-in-depth, with actual policy and context; do not claim it
makes arbitrary HTML safe. Do not claim HttpOnly eliminates XSS impact. Severity
depends on whose browser processes the content and the application's authority.
Self-only rendering may materially reduce the supported impact.

Prefer text rendering for text-only requirements. For deliberate rich HTML, use
a maintained sanitizer with a restrictive policy suited to the sink, and avoid
post-sanitization changes that reintroduce active content. Regression tests should
assert escaped/text output or sanitizer policy with harmless markup and verify
legitimate content still renders. Do not run a browser payload against a target.
