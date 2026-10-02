# TypeScript

Apply the JavaScript runtime methodology. Type annotations, interfaces, generics,
non-null assertions, `as`, `satisfies` and compile-time readonly do not validate
untrusted runtime data. Trace request/JSON values to actual schema parsing,
refinement, transformations and handling of parser failure.

Inspect unknown-field stripping versus passthrough before judging mass assignment.
A type-narrowed value may still originate from an unchecked assertion. Conversely,
a runtime schema that constructs a constrained DTO is real counter-evidence.
Discriminated unions are useful only when their runtime discriminator is validated.

Trace server-only modules and client boundary imports in frameworks. Do not treat
an exported type as executable exposure. Test contracts should include out-of-type
runtime inputs and valid data; do not claim the compiler proves authorization.
