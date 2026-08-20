# SPEC 08 — Testing and documentation requirements

> **Aspirational.** Status markers record justification strength, not implementation status.
> Vocabulary as ratified in [`GLOSSARY.md`](../GLOSSARY.md).

- **Date:** 2026-08-20
- **Scope:** what must be tested and what must be documented, as requirements. The testing *strategy*
  — tool roster, coverage taxonomy, CI topology — is sync **D2**'s and is deliberately not fixed here.
- **`QA-0`** (every constraint that can be executable MUST be executable) is declared in
  [`03-non-functional-requirements.md`](03-non-functional-requirements.md) and governs this whole file.

## Testing levels

### QA-1 — Analysis logic MUST be unit-tested against fixtures whose expected output is written by hand. *(operational)*

**MUST.** Extraction, resolution and traversal have expected outputs a human can state. Those
expectations MUST be written independently of the implementation, not captured from it — a snapshot of
current behaviour tests that nothing changed, which is a different and weaker claim.

**Verification:** fixtures carry hand-written expectations. Snapshot tests are permitted **in addition**,
never as the only assertion for a correctness claim.

### QA-2 — Every capability MUST have an integration test exercising it through a surface. *(operational)*

**MUST.** Through `git-ctx` or the API, against a real store backend (the in-memory default is a real
backend for this purpose).

**Verification:** a coverage check over `analysis/0001-capabilities.md` — every `CAP-` row is reached by
at least one integration test. A capability with no such test fails the gate.

### QA-3 — The correctness properties in `03` MUST be property-tested, not example-tested. *(assumed)*

**MUST.** `COR-1` (three-state contract), `COR-2` (incremental equals full rebuild) and `COR-3`
(derived identity behaviour) are universally quantified claims. Examples cannot establish them.

- `COR-1`: over generated graphs and queries, **no** truncated, degraded or scope-exiting walk returns
  `none affected`.
- `COR-2`: over generated change sequences — add, delete, modify, rename, move — the incrementally
  maintained index equals a from-empty rebuild.
- `COR-3`: over repeated runs, the chosen identity-stability branch holds.

**Verification:** each property exists as a property test with a generator, and each has a
**deliberately-broken control** demonstrating the property test fails when the property is violated. A
property test nobody has seen fail is not known to be testing anything.

### QA-4 — Where two implementations of one contract exist, they MUST be differentially tested. *(VERIFIED)*

**MUST.** Two store backends for one slot; two surfaces projecting one contract; a fast path and a
reference path.

**MUST also:** the harness needs its own discriminating control. **Agreement between two
implementations is not evidence the harness works** — it is equally consistent with the harness
comparing nothing. Each differential suite MUST include a case where the two are known to differ, and
MUST fail on it.

**Why this is evidenced:** this estate has measured a cross-engine differential harness reporting exact
agreement, where the agreement was later found to hold only for a corrected run — the harness as
originally shipped had two engines disagreeing substantially and did not say so. A green differential
suite with no failing control is not a result.

**Verification:** every differential suite contains a must-fail case.

### QA-5 — Anything parsing untrusted input MUST be fuzzed. *(operational)*

**MUST.** Source files, patches, query strings and configuration are all untrusted. `COR-7` states the
resilience requirement; this states how it is established.

**Verification:** a fuzz target per untrusted-input boundary, with a corpus retained across runs, run in
CI on a schedule rather than only per commit.

### QA-6 — Every supported language MUST have an extraction-depth conformance suite. *(assumed)*

**MUST.** `FR-003` requires each language to declare which node kinds and edge classes it extracts. The
suite proves the declaration, and its output is a **depth report per language**, not a pass or fail —
because partial support is the normal state and reporting it as failure hides how much exists.

**Verification:** the suite is generated from the declaration, so a declared capability with no fixture
is a gate failure. It MUST be runnable by someone adding a language from outside this repository
(`01-personas-and-flows.md` §E2).

### QA-7 — Every store slot MUST have one conformance suite, and it MUST be externally runnable. *(assumed)*

**MUST.** The suite **defines** the slot (`COR-6`). It MUST be part of the published contract rather
than an internal test, so a backend author outside this repository can establish their backend is
correct.

**MUST also:** it MUST be runnable without the rest of the platform's test corpus, and it MUST NOT
require network access for the embedded backends.

**Verification:** the suite runs against a backend implemented outside this repository's tree. Until
one exists, the substitute is that it runs against each in-tree backend from a standalone entry point,
which is weaker and is recorded as such.

### QA-8 — Performance budgets MUST be regression gates, not reports. *(operational)*

**MUST.** `PERF-2` through `PERF-5` and `PERF-7` each have a baseline and a documented regression
threshold, and exceeding it fails the release.

**MUST also:** `PERF-1`'s concurrency test MUST include its discriminating control — a serial run whose
aggregate must differ from the concurrent run. **If the control does not discriminate, the run is void,
not passing.**

**Verification:** the gate exists in CI and has been observed to fail on a deliberate regression. A
baseline file containing only placeholders does not satisfy `PERF-7`.

### QA-9 — One behavioural conformance suite MUST pass against both deployment shapes and every surface. *(assumed)*

**MUST.** The same corpus, the same queries, the same expected answers — through `git-ctx` locally,
through the API in the service shape, and through the agent surface. `CON-2`, `IF-1` and `COR-5` are all
established by this one suite.

**Verification:** the suite runs in both shapes in CI. A divergence is a defect in the shape or the
surface, never a documented difference.

### QA-10 — A full index build MUST have a published baseline that gates the release. *(operational)*

**MUST.** See `PERF-7`. The baseline is for a fixed corpus, published, and versioned with the code.

**Verification:** the gate fails on a regression beyond the documented threshold.

### QA-11 — A release gate MUST assert exactly one rank-fusion code path exists. *(VERIFIED)* — **inherited-negative**

**MUST.** An executable check, not a review item. It asserts that exactly one fusion implementation
exists and that every ranking consumer reaches it, and a differential test asserts the same query
returns the same ranking through every surface.

**Why this is evidenced:** the reference implementation had three fusion implementations with divergent
effective constants and different join keys, and its highest-traffic surface used none of the shared
ones. A convention would not have caught that; a gate would.

**Verification:** the check exists and fails when a second fusion path is introduced deliberately.

### QA-12 — A release gate MUST assert an index built on the previous version is served without a rebuild. *(VERIFIED)* — **inherited-negative**

**MUST.** Build on version N, upgrade to N+1 across a deliberate model change, serve without
reindexing. Authoritative data is migrated; derived data may be rebuilt (`FR-073`).

**Why this is evidenced:** in the reference implementation a model-fingerprint change disabled
incrementality entirely and the parse cache was keyed on the release version, so every release
reindexed everything.

**Verification:** the gate runs on every release, not on demand. A release that cannot be tested this
way because no prior version exists records that, rather than skipping silently.

### QA-13 — Mutation testing SHOULD run over analysis logic. *(assumed)*

**SHOULD.** Analysis code is exactly the shape mutation testing catches — many branches whose wrong
answers are plausible. The repository's own ignore file already anticipates a mutation-testing tool,
which suggests the intent predates this SPEC.

**Verification:** a mutation score exists for the analysis modules and is reported. Not a gate in v1;
gating it before there is a baseline would either block everything or be set so low it means nothing.

### QA-14 — A dependency licence inventory MUST gate the build. *(VERIFIED)*

**MUST.** See `EXT-8`. Generated, not hand-maintained. A dependency with an unreviewed licence fails
the build.

**Why this is evidenced:** the failure mode is a **transitive** dependency added later, which a one-time
review cannot catch — and the grounding recorded a real instance of a published artefact whose declared
licence text was not present in the package, plus vendored third-party components redistributed without
their notices. Both are gate-catchable and neither was caught.

**Verification:** the gate exists; adding a dependency with a disqualifying licence fails CI.

### QA-15 — Every "MUST NOT leak" assertion MUST carry a positive control. *(VERIFIED)*

**MUST.** `SEC-12` (credentials), `SEC-13` (code egress) and `SEC-16` (telemetry contents) are all
absence claims, and an absence claim established by a scan that cannot fail is worthless.

**Why this is evidenced:** this estate has measured verification tooling that passed against
deliberately wrong inputs — two separate tools reporting success where they had to fail — and the
recorded conclusion was that a control which passes voids the positive result too.

**Verification:** each scan has a companion case that deliberately leaks and MUST be detected. If the
companion passes, both results are discarded.

## Release gates

The gates a release must clear. Each names the requirement it establishes.

| Gate | Establishes | Fails when |
|---|---|---|
| Behavioural conformance, both shapes, all surfaces | `CON-2`, `IF-1`, `COR-5`, `QA-9` | any answer differs by shape or surface |
| Store conformance, every configured backend | `COR-6`, `EXT-1`–`EXT-6`, `QA-7` | any backend fails any case |
| Property suite with must-fail controls | `COR-1`, `COR-2`, `COR-3`, `QA-3` | a property fails, or a control passes |
| Differential suites with must-fail controls | `QA-4` | a control passes |
| Single fusion path | `FR-071`, `QA-11` | a second path exists |
| Upgrade without reindex | `FR-073`, `QA-12` | a rebuild is required |
| Performance budgets | `PERF-2`–`PERF-5`, `PERF-7`, `QA-8` | a budget regresses beyond threshold, or the concurrency control does not discriminate |
| Advertised equals callable | `IF-4` | the sets differ |
| Authorisation route enumeration | `IF-3`, `SEC-4` | any route bypasses the authorisation point |
| Audit coverage over mutating operations | `SEC-6` | a mutating operation produces no record |
| Metric cardinality | `OPS-6` | a metric is labelled by an unbounded source |
| No datastore type in the public API | `REV-1` | one appears |
| No structure pre-empted in the corpus | `CON-8` | a crate-shaped name or a layout appears |
| Licence inventory | `EXT-8`, `QA-14` | an unreviewed or disqualifying licence appears |
| Leak scans with positive controls | `SEC-12`, `SEC-13`, `SEC-16`, `QA-15` | a control fails to detect a deliberate leak |
| Clean-room laundering check | `CON-1` | a reference-internal identifier or carried constant appears |

**Twelve of these sixteen gates are executable checks rather than test suites.** That is deliberate:
`QA-0` requires that a constraint which can be enforced is enforced, because a documented convention
has no failure mode.

## Documentation requirements

### QA-16 — Every language's extraction depth MUST be documented and generated from the declaration. *(assumed)*

**MUST.** *"Supports language X"* is not a documentable claim (`FR-003`). The documentation MUST state,
per language, which node kinds and edge classes are extracted, and MUST be generated from the
declaration so it cannot drift.

**Verification:** the page is generated; a declaration change changes the page; a hand-edit to the page
fails the build.

### QA-17 — Every store slot's capability profile MUST be documented as the contract a backend author implements. *(assumed)*

**MUST.** Paired with the conformance suite (`QA-7`), because a suite without a stated contract tells an
author what failed but not what was expected.

**Verification:** the profile document and the suite are cross-referenced, and a suite case with no
corresponding documented requirement is a gate failure.

### QA-18 — The three-state result contract MUST be documented for consumers, with the failure it prevents. *(assumed)*

**MUST.** Consumer-facing documentation MUST state that `none affected` and `undetermined` are
different, MUST show how to branch on them, and MUST state what goes wrong if they are conflated. An
agent's prompt or system message is documentation for this purpose.

**Verification:** the documentation exists and is referenced from the agent surface's own descriptive
text, so a consumer meets it without going looking.

### QA-19 — Documentation MUST NOT describe behaviour the code does not have. *(VERIFIED)*

**MUST.** Where documentation and code disagree, that is a defect in one of them, and it MUST be
resolvable by a check rather than by reading both.

**Why this is evidenced:** the grounding measured substantial documentation drift in the reference
implementation — an architecture document naming two files that did not exist, stating a wrong table
name, a wrong set of embeddable kinds, and a performance claim the code's own comments refuted; plus a
contributor document denying a build script the manifest defined. The drift was concentrated in exactly
the documents a new implementer reads first.

**Verification:** anything documentable from a declaration is generated (`QA-16`, `QA-17`). For prose
that cannot be generated, code examples in documentation MUST be compiled and run in CI, so a stale
example fails.

**The consequence we dislike:** this forbids illustrative pseudo-code in documentation unless it is
marked as non-compiling. Prose examples that look real and are not are precisely the drift this
requirement targets.

### QA-20 — Every deployment shape MUST have an operator document stating what it requires and what it does not. *(operational)*

**MUST.** For the local shape: no listener, no authentication, embedded stores, telemetry off. For the
service shape: which stores, which identity provider, which egress destinations (`SEC-13`), which
budgets, and what fails closed.

**Verification:** the egress enumeration in the operator document matches the configuration surface,
asserted by the same restricted-network test that establishes `SEC-13`.

### QA-21 — A decision record MUST exist for every choice this corpus deliberately deferred. *(operational)*

**MUST.** MADR format, numbered globally, immutable once accepted — supersede, never edit. Each MUST
**record the consequence the author dislikes**, which is house convention and is the sentence most
likely to be lost in a rewrite.

At minimum, one per open question: the async decision, derived-identity stability, the authorisation
unit, the embedding provider and vector-width policy, the store compatibility targets, the TUI, the wiki
output contract, and the AGPL linkability question.

**Verification:** every question file in `questions/` reaches either an accepted decision record or an
explicitly `accepted` gap with a revisit trigger. A question that has quietly stopped being discussed
satisfies neither.

## Verification

### What is proven

- **Every gate names the requirement it establishes**, so the gate list and the requirement set are
  cross-checkable rather than parallel.
- **Three requirements here demand must-fail controls** — `QA-3`, `QA-4`, `QA-15` — and each cites a
  measured instance of a control that could not fail. This is the most-repeated lesson in this estate
  and it appears as a requirement rather than as advice.
- **Twelve of sixteen gates are executable checks**, satisfying `QA-0` for the constraints that admit
  it.
- **Two inherited negatives are carried here** — `QA-11`, `QA-12` — plus `QA-4`, `QA-14`, `QA-15` and
  `QA-19`, which cite measured failures without being on the canonical eleven.

### What is NOT proven

- **None of these suites or gates exists.** There is no code. Every requirement here describes an
  artefact yet to be written, and the two most load-bearing — the store conformance suite (`QA-7`) and
  the incremental-equals-full property (`QA-3`) — are also the two largest.
- **`QA-7`'s external runnability cannot be established yet.** No out-of-tree backend author exists, so
  the strongest available evidence is an in-tree standalone entry point, which is weaker than the
  requirement.
- **`QA-8` depends on telemetry that does not exist** (`GAP-004`), so the performance gates are
  currently unimplementable rather than merely unimplemented.
- **`QA-13` sets no threshold.** Deliberate, and it means mutation testing could be present and useless.
- **The testing strategy is not settled.** Tool roster, CI topology and coverage taxonomy are sync
  **D2**'s, so this file states requirements whose implementation shape is open.
- **`QA-19` has no mechanism for prose that cannot be generated or compiled.** Architectural narrative
  is exactly the documentation that drifted worst in the prior art, and nothing here catches it.

## Amendments

- **2026-08-20** — Created.

## Related

- [`03-non-functional-requirements.md`](03-non-functional-requirements.md) — `QA-0`, and the budgets `QA-8` gates.
- [`05-security-requirements.md`](05-security-requirements.md) — the absence claims `QA-15` controls.
- `SYNCS.md` — sync **D2** owns the testing strategy; **D1** owns the telemetry `QA-8` needs.
