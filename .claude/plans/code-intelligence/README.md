# code-intelligence

Requirements for a **Rust code-intelligence platform** — a system that parses repositories into a
queryable knowledge graph and serves it to humans over a web UI and to AI agents over MCP, in two
deployment shapes: a local CLI and a Kubernetes-native microservice.

**This plan owns requirements documentation only.** It produces the SPEC, PRD, feature list and
analysis documents that a Software Architect consumes. It deliberately writes **no Rust, no
`Cargo.toml`, and no crate names** — module decomposition is the architect's deliverable, and
pre-empting it is the main way this work fails.

**Status (2026-08-19): trigger prompt written, not yet executed.** Only `PROMPT.md` and this file
exist.

## Why this plan exists

A mature reference implementation of this capability already exists — **GitNexus** (TypeScript) —
and hosting it was the original plan. That plan is blocked. GitNexus is **PolyForm Noncommercial
1.0.0**, and its licensor confirmed in writing that internal use at a for-profit company requires a
paid commercial licence. The full determination, with quoted clauses and primary sources, is in
`~/repos/woven/forks/gitnexus/.claude/plans/hosted-service/FINDINGS.md` §0 (on `main`).

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
   `~/repos/woven/forks/muster/.claude/rules/{00-non-negotiables,04-rust-conventions}.md` establish
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
   `<ENGINE>` as a visible placeholder. See `questions/0001-product-and-crate-naming.md`.
5. **A module-seam sketch exists and is explicitly not pressure-tested.** The requester supplied it
   (recorded verbatim as Appendix B of `PROMPT.md`) with the intent that logic be split into crates
   assembled into either a microservice or a CLI. It is **input to be tested, not the answer** — the
   architect owns the final shape. Appendix B also lists ten requirements-coverage gaps the sketch
   does not yet place, and the questions it raises.

## Architectural syncs

The requester wants **recurring syncs with the Software Architect while the crate and module seams,
and the SDK-versus-library-versus-binary clusters, are being defined.** [`SYNCS.md`](SYNCS.md) is the
catalogue — **twenty syncs in four tracks**, because a flat list of twenty checkpoints is not a
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
Eight entries are seeded, covering every confidence level. There is **no backlog yet**
(`questions/0002`), so `scheduled` entries carry acceptance criteria inline until there is one.

## Map

| Path | What it is | Exists |
|---|---|---|
| `PROMPT.md` | Trigger prompt — write the requirements documentation. Appendices carry the capability list and the module-seam sketch. | ✅ |
| `README.md` | This file: what the plan is, and the map. | ✅ |
| `SYNCS.md` | The sync catalogue — twenty syncs, four tracks, ordering and hard gates. Living. | ✅ |
| `GAPS.md` | Gap taxonomy, lifecycle, the four rhythms, and the register. Eight entries seeded. Living. | ✅ |
| `discussions/0001-what-impact-analysis-means.md` | **Open.** Seven axes on which "impact" varies; the non-negotiable three-state result contract; a proposed vocabulary. | ✅ |
| `questions/0001-product-and-crate-naming.md` | **Partially decided.** CLI is `git-ctx`; engine-library name deferred behind the seam-mapping gate. | ✅ |
| `questions/0002-where-does-the-backlog-live.md` | **Open.** No backlog exists. Recommends deferring with an explicit revisit trigger. | ✅ |
| `PRD.md` or `prds/` | Problem, why now, functional requirements, out of scope, user flows, dependencies, success criteria. | ⬜ |
| `specs/NN-*.md` | The SPEC, split across numbered files. | ⬜ |
| `FEATURES.md` | Flat, ID'd feature list traceable to SPEC requirement IDs. | ⬜ |
| `analysis/` | Capabilities · feature clusters · feature gaps. | ⬜ |
| `QUESTIONS.md` | Index over `questions/`. | ⬜ |

Directories are created on their first real document — a stub tree reads as coverage and is a lie.
Numbering is global per kind, so gaps are expected; note them here rather than renumbering.

## Related

- `~/repos/woven/forks/gitnexus/.claude/plans/hosted-service/` — the grounding research this plan
  inherits: `FINDINGS.md` (licensing verdict, then the evidence), `RESEARCH.md` (~1,830 lines of
  archaeology across five lanes), `QUESTIONS.md`, and `adrs/0001-gitnexus-licensing-path.md`.
- `~/repos/woven/forks/muster/` — the estate's target pattern for Rust workspaces and for
  plan-scoped specs and PRDs. Its `.claude/plans/orrery/{specs,prds,questions,research}/` is the
  format to mirror.
- `~/repos/woven/infrastructure/infrastructure/docs/src/dev/specs/` — graduated specs, and the
  source of the requirement-ID and `## Verification` conventions.
- `~/.claude/rules/plans-and-docs.md` — governs this layout, and the aspirational-vs-graduated
  distinction for specs and PRDs.
