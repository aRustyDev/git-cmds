# Analysis 0007 — The target corpus, and what it changes

- **Date:** 2026-08-20 · **Status:** derivation from a requester answer of the same date
- **Purpose:** the target corpus was answered, and the answer propagates into a dozen requirements.
  This document derives the implications **once**; the affected requirements carry dated amendments
  pointing here rather than restating them.
- **Vocabulary:** [`GLOSSARY.md`](../GLOSSARY.md)

## The answer

> - A collection of crates/modules as libraries and SDKs, all under `git-cmds/crates/**`
> - Binaries that consume those libraries to effectuate business logic, also under `git-cmds/crates/**`
> - Potentially multiple binaries interacting in a microservice pattern over gRPC/HTTP

Three facts, each with consequences:

1. **It is a Rust workspace.** So Rust is the primary *target* language, not merely the implementation
   language — the system analyses codebases of the same shape as itself.
2. **It is one repository containing many deployable units.** A monorepo, in the sense that matters.
3. **The deployable units talk to each other over gRPC/HTTP.** So service-to-service contracts are
   **intra**-repository, not inter-repository.

## The finding that matters most: the graph is conditional

**Rust conditional compilation makes edges conditional on a feature set, and nothing in this corpus
handles that.**

`CON-7` — a house convention this project must follow — mandates **per-backend feature flags with an
in-memory default**. So the target corpus, including this project's own code, will carry
`#[cfg(feature = "...")]` throughout precisely at the store seam that `EXT-1`–`EXT-6` describe.

The consequence is sharp: **a blast radius computed under one feature set is wrong under another.** A
symbol reachable only when a feature is enabled is either included — overstating reach for a deployment
that does not enable it — or excluded, understating it for one that does. Both are wrong answers, and
neither is currently expressible: `FR-024`'s response states its edge set and depth bound, and says
nothing about a build configuration.

This is not a Rust curiosity. It is the same shape as conditional configuration in any language, and the
grounding recorded that the reference implementation kept conditional-configuration edges **out** of its
impact defaults and made them opt-in — a defensible call for an *edge class*, but this is not an edge
class. It is a predicate over the whole graph.

**Options, none of which this document chooses:** index the union of all feature sets and label each edge
with the predicate that admits it; index one canonical feature set and state it in every answer; or index
per feature set and treat the set as part of the index identity. The first is most correct and most
expensive; the second is cheapest and is a **correctness statement that must be in the response**, not a
footnote.

**Filed as `GAP-018`.** It is owned by **B3**, because it is a data-model question before it is a query
question, and it should be settled before any schema.

## What the answer settles

### `questions/0007` — the authorisation unit

**It is a monorepo, so repository-level authorisation is inadequate.** One repository containing every
library and every binary means repository-level entitlement is all-or-nothing over the entire estate's
code. That eliminates option A.

**And the natural unit is now obvious and better than "path":** a **workspace member**. Crate boundaries
are a human-authored, declared decomposition — not a path convention someone might reorganise. Path-level
entitlement expressed as `crates/<name>/**` is the same thing with a weaker guarantee.

Node-level authorisation remains available and remains the option with the traversal consequence
(`SEC-8`) and no precedent.

### `questions/0005` — AGPL linkability

**Narrowed usefully.** The binaries consuming the libraries are *in the same workspace and under the same
licence*, so there is no licence tension **within** the corpus. `CON-4` therefore bites only on consumers
outside `git-cmds`, which is a much smaller and more answerable question: does any codebase outside this
workspace need to link, rather than call?

### `SCALE-1` — the scale target may be miscalibrated

A Rust workspace of libraries and binaries is **very unlikely to reach one million nodes**. `SCALE-1`'s
v1 target was derived from "a large monorepo reaches single-digit millions of addressable symbols", which
describes a large polyglot product repository rather than a crate workspace.

**This is not an argument to lower the target** — a code-intelligence platform whose scale target is its
own repository is a platform that will not survive its second customer. It is an argument that the target
is currently **uncalibrated against the primary corpus**, so the budgets in `specs/03` are being validated
against a corpus nobody has measured and may be met trivially. Filed as `GAP-019`.

## What the answer changes, per requirement

| Requirement | Change | Why |
|---|---|---|
| `FR-003` extraction depth | **Rust is priority one**, and its extraction contract is unusual — see below | Primary target language |
| `FR-005` declarative formats | **Promoted from SHOULD toward core.** Cargo manifests are declarative config, and workspace membership, dependency edges and feature declarations live only there | Workspace structure is not in any `.rs` file |
| `FR-006` cross-file resolution | Must handle **re-exports**. `pub use` means the path a symbol is imported by is not the path it is defined at, so an import graph built naively is wrong | Rust module system |
| `FR-008` RPC/tool-definition mapping | **Promoted from peripheral to primary.** gRPC service definitions are the boundary between deployable units in this corpus | The microservice pattern |
| `FR-034` response-shape conformance | **Materially de-risked.** Protobuf and OpenAPI declare schemas, so shapes are *declared* rather than inferred | See below |
| `FR-043`, `FR-044` group membership | **The member unit is a deployable unit, not a repository** | Contracts are intra-repository here |
| `FR-024`, `FR-026`–`FR-028` | **Need a feature-set predicate** they do not have | `GAP-018` |
| `FR-032` sub-directory scoping | **Load-bearing rather than convenient.** Scoping to a crate is the primary way a developer narrows a monorepo | Monorepo |
| `SCALE-1` | Uncalibrated against the primary corpus | `GAP-019` |

### Why `FR-034` is materially de-risked

`analysis/0003` marked response-shape conformance as **inaccessible** — precedent only in the reference —
and noted it was *"the capability whose correctness is least well-defined, because an inferred shape
yields findings that are evidence rather than proof."*

**With gRPC, the shape is declared.** A protobuf message definition is an authoritative contract, so
conformance checking becomes: compare declared schema against observed consumer field accesses. That is a
far stronger position than inferring a producer's shape from its return statements, and `FR-034`'s
requirement to distinguish declared from inferred shapes now has a corpus where the declared case
dominates.

**It remains `inaccessible` for the inferred case** — plain HTTP handlers returning ad-hoc JSON — but the
primary corpus's hardest instance just became its easiest.

### Rust's extraction contract is unusual, and three parts are genuinely hard

Recorded because `FR-003` requires a **declared** extraction depth per language, and the honest
declaration for Rust has to name these:

1. **Traits and `impl` blocks, not classes.** A method's defining type and its trait are separate
   relationships, a trait may be implemented for a foreign type, and the "override" relationship that
   `FR-022` categorises has no direct analogue. Blanket implementations mean one `impl` block can supply
   methods to an unbounded set of types.
2. **Macros.** Macro-generated code is **not in the syntax tree**. Derive macros generate trait
   implementations; procedural macros can generate arbitrary items, including whole modules. A graph
   built from unexpanded syntax is blind to them; a graph built from expanded source has nodes that
   correspond to no source location a developer can open. Both are defensible and they are different
   products. **This is the single largest Rust-specific extraction question** and it belongs in sync
   **C1**.
3. **Generics.** A generic function is one symbol; its monomorphised instances are many. Call edges
   through a generic parameter are resolved only at the instantiation site, so a call graph that does
   not model instantiation will miss real reach — which is `FR-024`'s soundness posture, expressed in a
   language feature.

**None of these is a reason to deprioritise Rust.** They are the content of its extraction-depth
declaration, and declaring "trait implementations: yes; macro-generated items: no" is exactly what
`FR-003` exists to force.

## What becomes possible: the system can analyse itself

The target corpus is the same shape as this project's own repository, so the platform can index
`git-cmds`. That is worth more than a convenience:

- **A real test corpus exists from day one**, with hand-verifiable expectations, which `QA-1` requires
  and which is otherwise expensive to build.
- **`SCALE-1`'s calibration has a starting point**, even if it is a small one (`GAP-019`).
- **The feature-flag problem is self-demonstrating.** This project's own store seam is feature-flagged by
  `CON-7`, so `GAP-018` can be reproduced against the platform's own source rather than a synthetic
  fixture.
- **Dogfooding pressures the right requirements.** The developer flow (`specs/01` §E) stops being
  hypothetical.

**One caution.** A system verified primarily against its own source risks fitting to Rust and to a crate
workspace — which is a real risk given that `FR-005`'s declarative formats and the polyglot case are both
weaker in the requirements than Rust now is. `QA-6`'s per-language conformance suites are the guard, and
they need a non-Rust language exercised for that guard to mean anything.

## Verification

### What is proven

- **The answer eliminates one option in `questions/0007`** and supplies a better unit than the one that
  question offered, on the strength of the monorepo fact alone.
- **`questions/0005` is narrowed** by an argument that follows directly from the corpus being one
  workspace under one licence.
- **`GAP-018` is derived, not speculated.** `CON-7` mandates feature flags; feature flags make edges
  conditional; `FR-024` has no way to express a build configuration. Each step follows from a document in
  this corpus.
- **`FR-034`'s de-risking follows from gRPC being declarative**, which is a property of the corpus rather
  than an assumption about it.

### What is NOT proven

- **The Rust extraction difficulties are stated from language knowledge, not measured.** Nobody has
  attempted extraction against this corpus, so "macros are the largest question" is judgement.
- **`GAP-019` asserts that a crate workspace is well under a million nodes without measuring one.**
  Cheap to check, and not checked — the platform that would measure it does not exist, but a crude
  count would settle the order of magnitude today.
- **"Potentially multiple binaries" is conditional.** The requester said *potentially*. If the
  microservice pattern does not materialise, `FR-008`'s promotion and `FR-043`/`FR-044`'s
  member-unit change are premature — though both are cheap and neither is wrong.
- **No decision here.** Every implication is filed against a requirement or a gap; none is resolved,
  and `GAP-018` in particular is a data-model question this document deliberately does not answer.

## Amendments

- **2026-08-20** — Created, from the requester's answer on the target corpus.

## Related

- `specs/02-functional-requirements.md` — `FR-003`, `FR-005`, `FR-006`, `FR-008`, `FR-024`, `FR-032`, `FR-034`, `FR-043`, `FR-044`.
- `specs/06-constraints.md` — `CON-7` (feature flags) and `CON-10` (grammars and extension).
- `questions/0005-agpl-linkability-for-internal-consumers.md` · `questions/0007-what-is-the-unit-of-authorisation.md`
- `GAPS.md` — `GAP-018` (conditional edges), `GAP-019` (scale calibration).
- `analysis/0003-feature-gaps.md` — `FR-034`'s precedent class, now improved for the declared case.
