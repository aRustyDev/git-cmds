# code-intelligence

Requirements for a **Rust code-intelligence platform** — a system that parses repositories into a
queryable knowledge graph and serves it to humans over a web UI and to AI agents over MCP, in two
deployment shapes: a local CLI and a Kubernetes-native microservice.

**This plan owns requirements documentation only.** It produces the SPEC, PRD, feature list and
analysis documents that a Software Architect consumes. It deliberately writes **no Rust, no
`Cargo.toml`, and no crate names** — module decomposition is the architect's deliverable, and
pre-empting it is the main way this work fails.

**Status (2026-08-20): the requirements corpus is authored.** A PRD, a ten-file SPEC carrying **163
requirements**, a ratified glossary, a flat feature list traced both ways, six analysis documents, two
discussions and eleven questions. **No sync has been held** — the corpus is one party's work, and every
sync's inputs are recorded in [`SYNCS.md`](SYNCS.md) `## Status`.

Three things a reader should know before going further:

1. **The author is clean-room tainted and must not implement.** They read the prior grounding research;
   implementers may not. See `specs/06-constraints.md` `CON-1`.
2. **`git-ctx` is taken on crates.io** — verified 2026-08-20, by a live 2022 crate that is a git
   subcommand for switching branches, which is the exact semantic collision `questions/0001` had
   recorded as an acceptable risk. The decision stands as written; the finding is `GAP-014`.
3. **The risk is concentrated, not spread.** `analysis/0003` collapses fifteen high-risk capabilities
   into one entangled cluster: flow and cluster derivation, their identities, and change detection.
   That cluster is the project.
4. **The target corpus is a Rust workspace** — libraries, SDKs and consuming binaries under
   `crates/**`, potentially several binaries over gRPC/HTTP. Answered 2026-08-20; the implications are
   derived in `analysis/0007-target-corpus-implications.md` and propagate into eight requirements. The
   headline consequence is `GAP-018`: **feature flags make graph edges conditional, and no requirement
   can express a build configuration** — so a blast radius is currently answerable only relative to a
   feature set nobody states.
5. **One earlier claim in this corpus was wrong and is corrected in place.** `FR-036` was called
   unimplementable for want of an output contract. The prior art ships the capability and its **public**
   documentation describes the contract — and reading public docs is explicitly permitted by the clean
   room. See `GAP-016` and note 17 of `analysis/0003`, which generalise the lesson: `inaccessible` means
   the *design* is unreadable, and a capability's public documentation is not its design.

## Why this plan exists

A mature reference implementation of this capability already exists — **GitNexus** (TypeScript) —
and hosting it was the original plan. That plan is blocked. GitNexus is **PolyForm Noncommercial
1.0.0**, and its licensor confirmed in writing that internal use at a for-profit company requires a
paid commercial licence. The full determination, with quoted clauses and primary sources, is in
`gitnexus/.claude/plans/hosted-service/FINDINGS.md` §0 (on `main`).

`gitnexus/.claude/plans/hosted-service/adrs/0001-gitnexus-licensing-path.md` framed four options —
buy, adopt permissive alternatives, stop, or managed SaaS. **A clean-room Rust implementation is
effectively a fifth**, and the only one that keeps every capability without a recurring licence or a
fragmented three-tool composition.

## The clean-room constraint is load-bearing

PolyForm's **No Other Rights** clause forbids sublicensing. A derivative of GitNexus therefore
**could not be released under this repository's AGPL-3.0 licence at all.** The clean room is not
hygiene — it is what makes the licence choice coherent.

The protocol is a **dirty-team / clean-team split**, specified in full in `PROMPT.md`:

- The requirements author **may** read the prior grounding research, and **may not** read GitNexus
  source.
- The architect and implementers read **only** what the author writes.
- Every requirement must pass the laundering test: *would this be implementable by an engineer who
  has never heard of GitNexus?*

## Known constraints

1. **This repository is AGPL-3.0.** Unlike PolyForm Noncommercial it places no bar on internal
   commercial use, so it solves the original problem — but two consequences shape the library / SDK /
   binary split: internal consumers must accept AGPL to *link* the libraries, and §13's network
   clause binds if the service is ever exposed beyond the organisation.
2. **Two deployment shapes, one design.** Local CLI (single binary, embedded stores, one user) and
   K8s microservice (external stores, authenticated, ~20–50 humans plus up to ~10 000 mostly
   read-only agents). Not two configurations — two points a single design must reach.
3. **The house Rust conventions already answer several architectural questions.**
   `muster/.claude/rules/{00-non-negotiables,04-rust-conventions}.md` establish
   persistence behind a repository trait with no concrete datastore type in the public API,
   per-backend feature flags with an in-memory default, `thiserror` in libraries and `anyhow` in
   binaries, and that the async decision must be resolved during screening because retrofitting it
   is a rewrite.
4. **The CLI is `git-ctx`; the engine-library name is deferred.** `git-graph` was rejected because
   *"git graph"* already means the commit DAG to every git user, while this product's graph is a
   code-structure graph. The engine name waits behind a gate — **once the mapping of engine
   components, module members, domains, features and seams is drafted** — because you cannot name the
   engine until you know what is inside it, and a premature name either gets outgrown or degenerates
   into a `-core` suffix, of which there are none in this estate. Write `git-ctx` literally and
   `<ENGINE>` as a visible placeholder. See `questions/0001-product-and-crate-naming.md` — **amended
   2026-08-20: `git-ctx` is taken on crates.io**, by a live crate that switches branches, so the
   `-ctx`-means-context-switching risk that document accepted is now a real collision (`GAP-014`).
5. **A module-seam sketch exists and is explicitly not pressure-tested.** The requester supplied it
   (recorded verbatim as Appendix B of `PROMPT.md`) with the intent that logic be split into crates
   assembled into either a microservice or a CLI. It is **input to be tested, not the answer** — the
   architect owns the final shape. Appendix B also lists ten requirements-coverage gaps the sketch
   does not yet place, and the questions it raises.

## Architectural syncs

The requester wants **recurring syncs with the Software Architect while the crate and module seams,
and the SDK-versus-library-versus-binary clusters, are being defined.** [`SYNCS.md`](SYNCS.md) is the
catalogue — **twenty-one syncs in four tracks**, because a flat list of twenty-odd checkpoints is not a
process:

| Track | Gates | Syncs |
|---|---|---|
| **A — Requirements** | the SPEC | capability review · **vocabulary review** · feature-list review · capability wishlist · the impact decision |
| **B — Architecture and seams** | the crate layout | seam pressure test · abstractions · data models · data flows · interfaces and protocols · library/SDK/binary split · async |
| **C — Extensibility and prior art** | specific capabilities | grammars and LSP · ast-grep · difftastic · Serena |
| **D — Engineering practice** | how the project is run | telemetry · testing · CI/CD and supply chain · context files and commit hygiene |

**Track D does not block requirements** — except telemetry, which does, because the read-concurrency
property, the latency budget and index staleness are all requirements that cannot be verified without
it, and an unverifiable requirement is a wish.

Five hard gates: **vocabulary before any SPEC prose** (drift compounds) · **difftastic before the
impact decision** (a structural-diff choice changes impact's input contract) · **async during backend
screening, never after** (retrofitting is a rewrite) · **data models before any schema** (the
evolution strategy is not retrofittable) · **telemetry before the non-functional requirements are
called done.**

The standing rule: **the requirements author brings requirements, the architect brings structure, and
every sync ends with something written down** — a closed question, a new question, an ADR, or an
amended requirement.

## Capability gaps

[`GAPS.md`](GAPS.md) carries the process and the register. Every sync files its gaps **as it goes**,
because a gap remembered is a gap lost.

The requester's six-term taxonomy is split into two orthogonal axes, since `accepted` is a
*disposition* while the rest state *confidence*:

- **confidence:** `known` · `discovered` · `inferred` · `presumed` · `hypothetical`
- **disposition:** `open` · `scheduled` · `accepted` · `refuted` · `closed`
- **kind:** `capability` · `coverage` · `verification` · `knowledge`

**Nothing unverified gets scheduled** — a `presumed` or `hypothetical` gap must be promoted to `known`
or `refuted` first. And `accepted` is not `closed`: it is a deliberate documented hole, and it needs a
**revisit trigger** or it becomes permanent by default.

Four rhythms — file on sight · triage every sync · verification pass and sweep at each track boundary.
**Nineteen entries** as of 2026-08-20: eight seeded, eleven filed while authoring the requirements, and a
dated triage plus verification pass over the original eight. All are `open`; **nothing is `scheduled`**,
which is correct, because there is **no backlog yet** (`questions/0002`) and three of the highest-value
entries are unverified and therefore ineligible under the binding rule. Until there is a backlog,
`scheduled` entries would carry acceptance criteria inline.

**The entry to act on first is `GAP-007`** — derived-structure identity stability. Its verification is a
single cheap check, and the best available outcome is that it is **refuted**, which would delete the
hardest algorithmic requirement in the corpus rather than solve it.

## Map

| Path | What it is | Exists |
|---|---|---|
| `PROMPT.md` | Trigger prompt — write the requirements documentation. Appendices carry the capability list and the module-seam sketch. | ✅ |
| `README.md` | This file: what the plan is, and the map. | ✅ |
| [`GLOSSARY.md`](GLOSSARY.md) | **Ratified vocabulary, written before any SPEC prose** (the A2 gate). Adopts the four analysis terms; renames "process" → **flow**; adds evidence class, index generation, torn read, advertised inventory, change set input. | ✅ |
| [`PRD.md`](PRD.md) | Problem, why now, users, twelve goals with done-conditions, must/should/won't, constraints, the eleven inherited negatives, out-of-scope **by name**, and `## How we will know we were wrong`. | ✅ |
| `specs/00-overview.md` | Introduction, purpose, business requirements, **how to read a requirement**, the identifier registry, the deployment duality. | ✅ |
| `specs/01-personas-and-flows.md` | Five personas; **all five flows** — user, admin, agent, **data**, **developer**. | ✅ |
| `specs/02-functional-requirements.md` | 51 functional requirements, every Appendix A capability ID'd. | ✅ |
| `specs/03-non-functional-requirements.md` | Performance per shape, scale, correctness, operability, reversibility. Every budget derived from a stated premise. | ✅ |
| `specs/04-interfaces-and-external-systems.md` | All surfaces, and the six store slots as capability profiles. **The only file naming products.** | ✅ |
| `specs/05-security-requirements.md` | Identity, authorisation, audit, fail-closed, abuse, privacy. | ✅ |
| `specs/06-constraints.md` | Design and implementation constraints, **including AGPL-3.0 with both consequences and the tension between them**. | ✅ |
| `specs/07-use-cases.md` | 34 user stories (6 admin · 12 developer · 12 agent · 4 non-technical) and 6 stepped use cases. | ✅ |
| `specs/08-testing-and-documentation.md` | Testing levels, sixteen release gates — twelve of them executable checks — and documentation requirements. | ✅ |
| `specs/09-references-and-appendices.md` | Mapping to the external SRS reference, and an honest assessment against its own quality criteria. | ✅ |
| [`FEATURES.md`](FEATURES.md) | 61 features covering all 163 requirements, **traced both ways by an executable ID-set diff**. | ✅ |
| `analysis/0001-capabilities.md` | 60 capabilities with consumer, mode, store and shape metadata. The architect's raw material. | ✅ |
| `analysis/0002-feature-clusters.md` | **Four candidate clusterings, none preferred**, plus ten invariants any clustering must satisfy. | ✅ |
| `analysis/0003-feature-gaps.md` | Precedent matrix, and the `inaccessible` risk class the clean room creates. | ✅ |
| `analysis/0004-store-capability-matrix.md` | The six slots as profiles, their portability hazards, and the **async screening record** (empty, and why). | ✅ |
| `analysis/0005-deployment-shape-contrast.md` | Applicability per requirement, distinguishing *unimposed* locally from *inapplicable* locally. | ✅ |
| `analysis/0006-threat-model.md` | Assets, principals, trust boundaries per shape, adversaries in and out of scope. | ✅ |
| `analysis/0007-target-corpus-implications.md` | The target corpus (a Rust workspace over gRPC/HTTP) and the eight requirements it changes. Carries the conditional-edge finding. | ✅ |
| [`QUESTIONS.md`](QUESTIONS.md) | Index over `questions/` and `discussions/`, with the dependency chain that ends in a rewrite. | ✅ |
| `questions/0001` … `0011` | Naming · backlog · async · derived identities · AGPL linkability · v1 scope · authorisation unit · embedding provider · TUI · store targets · wiki contract. | ✅ |
| `discussions/0001` · `0002` | What "impact analysis" means · is read/write asymmetry the primary seam. | ✅ |
| [`SYNCS.md`](SYNCS.md) | The sync catalogue — **twenty-one** syncs, four tracks, ordering, hard gates, and a per-sync status. Living. | ✅ |
| [`GAPS.md`](GAPS.md) | Gap taxonomy, lifecycle, the four rhythms, and the register — **19 entries**, with a dated triage and verification pass, and a recorded failure of the register's own rule. Living. | ✅ |
| `HANDOFF.md` | What the author is confident in, what they are not, and the clean-room taint statement. | ✅ |
| `scripts/audit-corpus.py` | **The executable audit.** Two-way traceability, story minimums, inherited-negative tagging, a verification method per requirement, the proven/not-proven split, no structure pre-empted (with a discriminating control), the laundering denylist, and the AGPL clauses. Run it with the plan directory as its only argument. | ✅ |
| `prds/` · `phases/` · `research/` · `findings/` | Not created — no document needs them yet. | ⬜ |

Directories are created on their first real document — a stub tree reads as coverage and is a lie.
Numbering is global per kind, so gaps are expected; note them here rather than renumbering.

**Numbering gaps currently present, all expected:** `FR-051`–`FR-067`, `FR-069`, `FR-070`, `FR-072` and
`FR-074` are unused, because the `CAP-0nn` ↔ `FR-0nn` alignment sends most cross-cutting capabilities to
`SEC-`, `EXT-`, `OPS-`, `PERF-` and `SCALE-` identifiers instead. The gaps are the price of a mechanical
mapping and are cheaper than renumbering — see `specs/09` Appendix D.

## Related

- `gitnexus/.claude/plans/hosted-service/` — the grounding research this plan
  inherits: `FINDINGS.md` (licensing verdict, then the evidence), `RESEARCH.md` (~1,830 lines of
  archaeology across five lanes), `QUESTIONS.md`, and `adrs/0001-gitnexus-licensing-path.md`.
- `muster/` — the estate's target pattern for Rust workspaces and for
  plan-scoped specs and PRDs. Its `.claude/plans/orrery/{specs,prds,questions,research}/` is the
  format to mirror.
- `infrastructure/docs/src/dev/specs/` — graduated specs, and the
  source of the requirement-ID and `## Verification` conventions.
- `~/.claude/rules/plans-and-docs.md` — governs this layout, and the aspirational-vs-graduated
  distinction for specs and PRDs.
