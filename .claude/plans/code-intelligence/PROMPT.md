# Write the requirements for a Rust code-intelligence platform

> **Trigger prompt.** Paste everything below the horizontal rule into a fresh Claude Code session
> started in `~/repos/woven/forks/git-cmds`. **Requirements authorship only — it stops short of
> writing Rust, choosing crate names, or designing modules.**
>
> Drafted 2026-08-19, from the grounding recorded in
> `~/repos/woven/forks/gitnexus/.claude/plans/hosted-service/`.

---

## Mission

Produce the requirements documentation for a **Rust implementation of a code-intelligence platform**:
a system that parses repositories into a queryable knowledge graph and serves that graph to humans
over a web UI and to AI agents over MCP, in two deployment shapes — a local CLI and a
Kubernetes-native microservice.

Your output is consumed by a **Software Architect** whose first two tasks are:

1. **Identify the flows** — for Users, Admins, Agents, Data, and Developers.
2. **Decide the module shapes** — from a business-logic standpoint, and from a software-engineering
   standpoint: libraries vs SDKs vs application code, and where the module seams go.

**Therefore: specify behaviour, not structure.** Do not name crates, do not draw a module diagram, do
not decide the workspace layout. Your job is to make those decisions *possible and well-informed* —
surface every force that bears on them, and stop.

## Clean-room protocol — BINDING, read before anything else

A reference implementation exists (**GitNexus**, TypeScript) licensed **PolyForm Noncommercial
1.0.0**. Its licensor confirmed in writing that internal use at a for-profit company requires a paid
commercial licence. PolyForm's **No Other Rights** clause forbids sublicensing, so **a derivative
work could not be released under this repository's AGPL-3.0 licence at all.** The clean room is what
makes the licence choice coherent — treat it as a hard constraint, not hygiene.

**You are the "dirty" side of a dirty-team / clean-team split.** You may read the prior grounding
research. The architect and implementers may not, and will work only from what you write.

| You MAY | You MUST NOT |
|---|---|
| Read `~/repos/woven/forks/gitnexus/.claude/plans/hosted-service/{FINDINGS,RESEARCH,QUESTIONS}.md` and `adrs/0001-*.md` (on `main`) | **Read GitNexus source code.** Not `gitnexus/src/**`, not its tests, not its schema files |
| Read GitNexus's public-facing docs for capability vocabulary | Copy code, schema DDL, or type definitions |
| State required behaviour in our own words | Reproduce internal names — module, file, function, phase, table, or tool names |
| Give numeric budgets we chose and can justify | Carry over magic constants from the reference (fusion K values, pool sizes, node caps, embedding widths, timeouts) |

**The laundering test — apply it to every line you write:** *would this requirement be readable,
unambiguous and implementable by an engineer who has never heard of GitNexus?* If it only makes sense
as a description of that codebase, rewrite it as a requirement.

**One consequence for you personally:** having read the research, you are tainted. Do not also write
the implementation. Say so in your handoff.

## Scope boundary

- **This plan owns requirements documentation only.** No Rust. No `Cargo.toml`. No crate names beyond
  a clearly-marked placeholder.
- **Rust crates plus the server/API surface are in scope.** The **web UI is a downstream consumer**:
  specify it as an interface contract and a performance budget the crates must satisfy, and leave the
  frontend technology unchosen.
- Deployment manifests, Helm charts and cluster plumbing are out of scope.

## What you inherit, and what you do not

Nothing is in your context that you do not read. Specifically:

- **Project memory is empty.** No `MEMORY.md`, no memory files — for this repo or any other.
- `~/.claude/rules/**` auto-loads — in particular `plans-and-docs.md`, which governs where your
  output goes, and `tool-call-plumbing.md`, whose constraints are measured, not theoretical.
- **muster's rules do NOT auto-load** (different repo). Read them by absolute path — they are the
  house reference and they answer several questions you would otherwise ask:
  - `~/repos/woven/forks/muster/.claude/rules/00-non-negotiables.md`
  - `~/repos/woven/forks/muster/.claude/rules/04-rust-conventions.md`
  - `~/repos/woven/forks/muster/.claude/rules/02-decision-records.md`
  - `~/repos/woven/forks/muster/.claude/rules/10-docs-structure.md`
- **This repository is AGPL-3.0** (`LICENSE`, 661 lines) and otherwise nearly empty. Its `README.md`
  reads *"Collection of Crates (Lib/SDK/Bins) for building and running git subcommands"*.

**Write project memories as you go** — at minimum the clean-room protocol, the AGPL consequences, and
the house-format pointers — so your successors inherit them instead of rediscovering them. One fact
per file, with frontmatter, plus a one-line pointer in `MEMORY.md`.

## Phase 0 — Orient (cheap, do it first)

Read, in this order: this repo's `README.md` and `LICENSE`; `~/.claude/rules/plans-and-docs.md`; the
four muster rules above; then the grounding research named in the clean-room table.

Then read the **house format exemplars** and match their shape, vocabulary and heading style:

| Read | For |
|---|---|
| `~/repos/woven/forks/muster/.claude/plans/orrery/specs/00-overview.md` … `05-testing-criteria.md` | The multi-file SPEC split, and the non-functional vocabulary: Performance budgets / Scale targets / Correctness / Security and privacy / Operability / Reversibility |
| `~/repos/woven/forks/muster/.claude/plans/orrery/prds/00-orrery-engine.md` | The house PRD outline |
| `~/repos/woven/infrastructure/infrastructure/docs/src/dev/specs/cluster-egress-requirements.md` | Requirement-ID style — `### E-1 — <Component> MUST <do X>. *(VERIFIED)*` — and `## Verification` split proven / not-proven |
| `~/repos/woven/infrastructure/infrastructure/.claude/plans/airgap-bootstrap/{PRD.md,SPEC.md}` | The richest PRD in the estate, the **contract seam register** pattern, and `## How we will know we were wrong` |
| `~/repos/woven/forks/muster/.claude/plans/quality-review/01-gap-matrix.md` | The gap-matrix pattern (`✓ covered · ◐ partial · ✗ gap · — N/A`) for your analysis docs |
| `~/repos/woven/forks/muster/.claude/plans/orrery/questions/` | One numbered file per architectural fork |

⚠️ **Do not** imitate GitNexus's own root docs (emoji priority markers, Title Case headings) — that
is upstream style and is inconsistent with house style. House style is sentence-case headings, no
emoji, en-dashes, inline `(ADR-00NN)` / `(Q4)` cross-references, dated amendments, and a closing
`## Amendments` / `## Related`.

**External reference on SRS structure**, supplied by the requester — read it for the shape of a
requirements specification and for what counts as a well-formed requirement, then defer to house
style wherever the two differ:
<https://www.computer.org/resources/software-requirements-specifications#what-are-some-examples-of-requirements-in-software>.
Cite it in the references appendix.

## Phase 1 — The laundered capability baseline

Before writing requirements, build the behavioural inventory the requirements trace to. Two halves.

### 1a. Required capabilities

The requester's authoritative list is **Appendix A**. For each entry: restate it as behaviour, assign
a requirement ID, and note whether it is *table stakes* (the reference does something equivalent) or
*net-new* (it does not). Do **not** copy the reference's tool names.

### 1b. Negative requirements — the highest-value inheritance

The grounding measured specific failure modes in the reference implementation. **These are the most
valuable thing you inherit**, because a reimplementation that reproduces them wastes the exercise.
Express each as a positive, laundered requirement with a verification method. At minimum:

- **Concurrent reads must scale with readers per replica.** The reference funnels every API read
  through one process-wide mutex against a single open database handle, so concurrent requests
  complete strictly one at a time — measured as a clean FIFO latency staircase. Specify the required
  concurrency property and how it will be proven.
- **The number of simultaneously-served repositories must not be a hard low constant.** The reference
  caps resident repositories at a small integer with LRU eviction, where eviction costs a full
  database reopen.
- **Indexing must not be single-slot.** In the reference, one repository's index run rejects every
  other repository's, in memory, with no queue and no durable job state — one tenant blocks all
  others.
- **Incrementality must be decidable before the expensive work, not after.** In the reference the
  full parse-and-analyse pipeline always runs to completion, and only *then* is the
  incremental-vs-full decision made; only the database write is incremental. Specify what must be
  skippable, and at what granularity change is detected.
- **Global partitioning must not force full recomputation.** Whole-graph community detection and
  derived flow extraction are recomputed wholesale every run in the reference, and their identities
  are primary keys of the query surface — so making them incremental changes *output*, not just cost.
  Specify whether stable identities across runs are required.
- **Identity must be per-principal, not a shared secret.** The reference's only credential is one
  static shared token with no claims and no expiry, validated at an edge proxy that strips it before
  the upstream hop — so "which agent asked for this?" is unanswerable *in principle*. Specify the
  identity, attribution and audit requirements.
- **Fail closed, not open.** In the reference an unset token authorises every request, and a
  contended global registry lock degrades to unlocked with a logged warning and a possible lost
  update.
- **Refactoring operations must be AST-accurate and must update the index.** The reference's rename is
  a whole-file word-boundary regex that rewrites comments and string literals, writes nothing back to
  the graph, and silently swallows its search tool's failure.
- **Ranking and fusion logic must have exactly one implementation.** The reference implements its
  result fusion three times, with divergent effective constants and different join keys.
- **A version upgrade must not force a full reindex.** In the reference a schema-fingerprint change
  disables incrementality entirely, and the parse cache is keyed on the package version.

Mark each as *inherited-negative*, so the architect can see which requirements exist because
something was measured rather than imagined.

## Phase 2 — The SPEC

Split across numbered files under `specs/`. Cover **all** of the requester's sections; the mapping to
house form is yours, but this split is suggested:

| File | Requester's sections it carries |
|---|---|
| `00-overview.md` | Introduction + Purpose (problem statement · target users · value proposition · constraints); Business Requirements; Product Overview (how it works · key features) |
| `01-personas-and-flows.md` | User Personas / Roles; and **the five flows the architect asked for — Users, Admins, Agents, Data, Developers.** Data flow and Dev flow are the two most often skipped; do not skip them |
| `02-functional-requirements.md` | Functional Requirements — every entry in Appendix A, ID'd |
| `03-non-functional-requirements.md` | Non-Functional Requirements; Performance (**both deployment shapes**); Quality Assurance |
| `04-interfaces-and-external-systems.md` | Interface Requirements (incl. the web-UI contract and the MCP surface); External System Requirements (the pluggable-backend matrix) |
| `05-security-requirements.md` | Security Requirements; optional external AuthN and AuthZ |
| `06-constraints.md` | Design Constraints; Implementation Constraints (**including AGPL-3.0 and its two consequences**) |
| `07-use-cases.md` | User Stories + Use Cases — scenarios and steps |
| `08-testing-and-documentation.md` | Documentation Requirements; testing levels; release gates |
| `09-references-and-appendices.md` | Definitions / glossary; external documents; visuals |

**Requirement style is mandatory:**
`### <PREFIX>-<n> — <Component> MUST <do X>. *(VERIFIED | assumed | operational | satisfied by design)*`
Every requirement gets an ID. Every SPEC file ends with `## Verification`, split into
`### What is proven` and `### What is NOT proven`. Distinguish MUST / SHOULD / WON'T explicitly.

**Two things to get right, because they drive the architect's decisions:**

- **The deployment duality is a first-class force.** Local CLI (single binary, embedded stores, no
  auth, one user) and K8s microservice (external stores, authenticated, ~20–50 humans plus up to
  ~10 000 mostly read-only agents) are not two configurations of one design; they are two points a
  single design must reach. State which requirements apply to which, and which stores must be
  swappable without touching business logic. The house precedent is per-backend feature flags with an
  in-memory default so tests need no external engine — cite it as precedent, do not mandate it.
- **The async question is load-bearing and must be surfaced, not decided.** House convention: *"if
  any candidate backend is async-only, the trait is async and everything above it inherits that —
  resolve during screening, not after; retrofitting async through a synchronous trait is a rewrite."*
  File it as a question and note which required backends force the answer.

## Phase 3 — Analysis documents

Under `analysis/`, three documents. These are what let the architect cluster behaviour into modules,
so they matter as much as the SPEC.

1. **Capabilities** — the atomic capability inventory. One row per capability: what it does, who
   consumes it (User / Admin / Agent / Dev), read or write, which stores it touches, and which
   deployment shapes must support it. This is the raw material for module decomposition.
2. **Feature clusters** — capabilities grouped by cohesion, with the *reason* for each grouping
   stated (shared state? shared dependency? same consumer? same change rate?). Offer more than one
   plausible clustering where the evidence is genuinely ambiguous, and say what would decide between
   them. **Do not present a single clustering as settled — that is the architect's call.**
3. **Feature gaps** — a matrix using `✓ covered · ◐ partial · ✗ gap · — N/A` across required
   capabilities × (reference-tool precedent · permissive-alternative precedent · net-new). Flag every
   capability with **no** precedent anywhere as elevated risk: those carry no proof of feasibility.

## Phase 4 — Questions and handoff

`questions/NNNN-*.md`, one file per genuine architectural fork, plus a `QUESTIONS.md` index. Expect at
least: the product and crate naming decision; the async decision; whether stable cross-run identities
are required for derived graph structures; the AGPL linkability question for internal consumers;
which of the reference tool's capabilities are deliberately *not* wanted (see Appendix A's closing
note); the authorisation model's unit (repository / path / graph node); and the embedding provider and
vector-width policy.

Close with a short handoff note: what you are confident in, what you are not, and the explicit
statement that you are clean-room-tainted and must not implement.

## Appendix A — the requester's capability list

Authoritative input, not a finished requirement set. Restate each behaviourally, assign IDs, and
reconcile conflicts.

**Graph and query.** Generate a repository wiki from the knowledge graph · raw Cypher-style graph
queries · process-grouped hybrid search combining graph traversal, keyword ranking, semantic vectors
and rank fusion · explain persisted taint findings · a 360-degree symbol view with categorised
references and process participation · query control- and data-dependence at statement level ·
git-diff impact mapping changed lines to affected processes · read-only structural checks against the
indexed graph · filter by node and edge type · show nodes within N hops of a selection, configurably ·
report node and edge counts · scope or filter the graph to a project sub-directory.

**Repositories.** Discover all indexed repositories, paginated by limit/offset · index a repository or
update a stale index · show index status for the current repository · list configured repository
groups · rebuild a group's contract registry and cross-repository links · swap between analysed
repositories · display more than one repository at once for cross-repository analysis.

**Pluggable stores** — each must swap between local and remote without touching business logic: graph
(embedded ↔ networked openCypher) · vectors (embedded ↔ networked) · SQL (embedded ↔ server) ·
optional external search indexes · optional external text-search indexes · optional external
key-value store. *(The requester named specific products per slot; treat those as compatibility
targets, and name them only in the external-systems section, not throughout.)*

**Security.** Optional external authentication (OAuth2, JWT) · optional external authorisation (RBAC,
ABAC, ReBAC).

**AI provider configuration.** Configurable from deployment config *and* from the web UI at runtime,
with the runtime path **toggleable so administrators can restrict it**.

**Web UI.** Force-directed, sequential and radial graph layouts · a locally cached graph object ·
**n95 query time under 1 s**.

**Scale.** ~20–50 humans and up to ~10 000 agents, predominantly read-only.

**User stories are required in these minimum counts:** Admins ≥ 5 · Developers/Engineers ≥ 10 ·
Agents ≥ 10 · Non-technical personnel ≥ 3.

**Closing note — a real gap to resolve, not an oversight to paper over.** This list omits several
capabilities the reference tool provides: transitive blast-radius analysis with a depth bound;
shortest-path tracing between two symbols; route-to-handler mapping; RPC/tool-definition mapping;
response-shape conformance checking; pre-change reports for a route handler; and coordinated
multi-file rename. **Ask whether each is wanted rather than assuming either way** — and note that the
grounding found the reference's own diff-impact to be a single-hop lookup rather than a transitive
walk, so "impact analysis" needs defining precisely before it can be specified.

## Appendix B — the requester's module-seam sketch

The requester supplied the crate sketch below, **explicitly labelled "not pressure tested or
reviewed"**, alongside the intent: *break the logic into separate crates that can be dynamically
included and assembled into either a microservice, a CLI, or a similar form.*

**Treat this as input to be tested, not as a constraint to satisfy, and not as the answer.** The
architect owns the final shape. Your job is to make sure the requirements cover everything the sketch
implies *and* everything it does not yet place.

```text
crates/
├── graph/
│   ├── status/     : Show index status for current repo
│   ├── analyze/    : Index a repository (or update a stale index)
│   │   └── taints  : source→sink data-flow findings (--pdg index)
│   ├── wiki/       : Generate repository wiki from knowledge graph
│   ├── explain/    : Explain persisted taint findings (source→sink flows, --pdg indexes)
│   ├── cypher/     : Raw Cypher graph queries
│   ├── rename/     : Multi-file coordinated rename with graph + text search
│   ├── trace/      : Shortest directed path between two symbols (call + class-member edges)
│   ├── impact/     : Blast radius analysis with depth grouping and confidence
│   │   └── api     : Pre-change impact report for an API route handler
│   ├── context/    : 360-degree symbol view — categorized refs, process participation
│   ├── query/      : Process-grouped hybrid search (BM25 + semantic + RRF)
│   │   └── pdg     : Query control/data dependence at statement level (--pdg indexes)
│   ├── detect/
│   │   └── changes : Git-diff impact — maps changed lines to affected processes
│   ├── schema/     :
│   ├── check/      : Read-only structural checks against the indexed graph
│   │   └── shape   : Validate API response shapes against consumers' property accesses
│   ├── group/
│   │   ├── list    : List configured repository groups
│   │   └── sync    : Rebuild a group's Contract Registry and cross-repo links
│   └── repo/
│       └── list    : Discover all indexed repositories (paginated — limit/offset)
├── sql/            : # (out of scope) an ORM interface for Dolt
├── dolt/           : # (out of scope) a different product copying from what beads and dolt server
│                     do, to support direct writes to the git DB
└── gud/            : # (out of scope) a different product 'git-U-data' or 'git-Union-data'
                      (like DVC or LakeFS)
```

### What the sketch does not yet place — requirements-coverage gaps

These are **factual gaps in coverage**, not architectural opinions. Each names a capability the
requirement set demands that has no home in the sketch. Make sure each is specified, and flag it for
the first architectural sync so the architect can decide where it belongs:

1. **Ingestion and parsing** — turning source into the graph. Language coverage, per-language
   extraction, and the extensibility contract for adding a language.
2. **The storage abstraction** — the requirement list demands graph, vector, SQL, search, text-search
   and key-value stores each swap between embedded and networked *without touching business logic*.
   Nothing in the sketch owns that seam, and it is the single most consequential one.
3. **Embedding generation and provider selection**, including the runtime-toggleable AI provider
   configuration and its administrative restriction.
4. **Ranking and fusion** — keyword, semantic and rank fusion appear under `query/`, but `context/`
   and `impact/` also rank. The requirement that this have **exactly one implementation** needs a
   home.
5. **The service surfaces** — the MCP endpoint and the HTTP/API layer, which are how agents and the
   web UI actually arrive.
6. **Authentication, per-principal identity, authorisation, and the audit trail.**
7. **Indexing as durable, queued, cancellable work** — the requirement that indexing not be
   single-slot implies a job model that no sketched crate owns.
8. **Repository acquisition** — fetching and updating repositories, and credential handling for
   private remotes.
9. **Configuration and deployment-shape assembly** — the sketch's own stated goal (assemble into
   microservice or CLI) needs a composition layer.
10. **Observability** — the concurrency, latency and staleness requirements are unverifiable without
    one.

### Questions the sketch raises — for the first architectural sync

Do not resolve these yourself. Record them as questions:

- **The sketch is organised by command, not by domain.** Every node maps to a CLI verb. That is a
  legitimate *surface* decomposition; whether it is also the right *crate* decomposition is the
  question, because shared machinery (graph access, parsing, ranking, storage) has no home in a
  command-shaped tree and tends to end up either duplicated or in one god-crate.
- **Read and write are not separated.** `analyze`, `rename` and `group/sync` mutate; everything else
  reads. With a target profile of ~10 000 mostly read-only agents, read/write asymmetry is arguably
  the primary seam, and the sketch does not draw it.
- **`impact/` and `detect/changes` are two homes for what may be one traversal.** See
  `discussions/0001-what-impact-analysis-means.md` — this is exactly the split that produced two
  incompatible mechanisms in the reference implementation.
- **PDG work spans `analyze/taints` (produce), `explain/` (report) and `query/pdg` (interrogate).**
  Reasonable as a write/read split, but the shared dependence model needs an owner.
- **`schema/` is an unlabelled slot.** What is it for?
- **`sql/` is marked out of scope as "an ORM interface for Dolt"** — but the requirement list needs a
  SQL store that swaps between embedded and server. Are those the same crate or different concerns?
  If different, the requirement's SQL store has no home in the sketch.
- **`rename/` is a write operation with a poor precedent.** The grounding found the reference's
  equivalent to be text-level with no index writeback. Confirm it is wanted, and specify it as
  AST-accurate with graph update — or drop it.

## Architectural syncs — a standing working agreement

The requester wants **recurring architectural syncs with the Software Architect while the crate and
module seams, and the SDK-versus-library-versus-binary clusters, are being defined.** Structure them
by checkpoint rather than by calendar, and treat each as producing a recorded decision.

| Sync | Fires when | Input the architect needs | Output |
|---|---|---|---|
| **S1 — capability review** | The capability inventory and the five flows are drafted | `analysis/` capabilities table, `01-personas-and-flows.md` | Agreement that the inventory is complete, and a first read on natural groupings |
| **S2 — seam pressure test** | Before any clustering is written down as preferred | The sketch in Appendix B, plus the coverage gaps and questions above | Which gaps land where; whether the decomposition stays command-shaped or turns domain-shaped |
| **S3 — the impact decision** | Before impact requirements are finalised | `discussions/0001-what-impact-analysis-means.md` | The seven axes settled, and whether one traversal serves all projections |
| **S4 — library / SDK / binary split** | Before the split is fixed | The AGPL linkability constraint, the deployment duality, read/write asymmetry | The cluster boundaries, and what may not appear in a library's public API |
| **S5 — the async decision** | During backend screening, **never after** | Which required stores are async-only | An ADR. House rule: retrofitting async through a synchronous trait is a rewrite |

**Rules for these syncs, so they stay useful:**

- **You bring requirements; the architect brings structure.** When the two conflict, the requirement
  is the thing that must be true and the structure is the thing that must change — unless the
  requirement turns out to be unfounded, in which case say so and amend it.
- **Never settle a seam in a sync on your own authority.** Your role is to test proposals against
  requirements and to say what a proposal would make impossible.
- **Every sync ends with something written down** — a closed question, a new question, an ADR, or an
  amended requirement. A sync that produces only shared understanding has produced nothing.
- **Bring the disliked consequence.** House ADR convention; it applies here too. If a proposal has a
  cost, name it in the sync rather than in review.

## Deliverables

Under `.claude/plans/code-intelligence/`, on a worktree feature branch (`docs/<slug>`), Conventional
Commits, never on `main`.

| Document | Contents |
|---|---|
| `README.md` | Update the `## Map` table as documents land |
| `PRD.md` or `prds/00-*.md` | House PRD outline |
| `specs/NN-*.md` | The SPEC, per the Phase 2 split |
| `FEATURES.md` | Flat, ID'd feature list traceable to SPEC IDs |
| `analysis/` | Capabilities · feature clusters · feature gaps |
| `questions/NNNN-*.md` + `QUESTIONS.md` | One file per architectural fork, plus an index |
| `discussions/NNNN-*.md` | Multi-axis design questions that are not yet single decisions |

**Already seeded — read both before starting, and extend rather than duplicating:**

- `discussions/0001-what-impact-analysis-means.md` — seven axes on which "impact" varies, the
  three-state result contract that is non-negotiable, and a proposed vocabulary
  (**reachability / blast radius / dependence / diff impact**). **Adopt that vocabulary in the SPEC**;
  if you do, the phrase "impact analysis" should not appear in any requirement, because it is a
  category rather than a capability.
- `questions/0001-product-and-crate-naming.md` — candidates are `git-graph` and `git-ctx`. The
  subcommand name and the engine-library name are **separate decisions**; use `<PRODUCT>` as a marked
  placeholder until both are settled, and do not half-rename a document.

Create each directory on its first real document — **never scaffold.** Numbering is global per kind,
so gaps are expected; note them in `README.md` rather than renumbering.

**This list is a floor, not a ceiling.** If the work surfaces something the architect will need that
has no home above — a data-flow diagram, a store-capability comparison matrix, a deployment-shape
contrast table, a threat model, a glossary large enough to stand alone — add it and record it in the
`## Map`. Say in your handoff which artifacts you added and why.

## Non-goals

No Rust written. No `Cargo.toml`. No crate names beyond a marked placeholder. No module diagram and no
proposed workspace layout — that is the architect's deliverable, and pre-empting it is the main way
this task fails. No chart or cluster work. No ADR graduated to `docs/src/`. Nothing pushed, no PR
opened. **No GitNexus source read.**

## Working rules

- **The capability list is input, not gospel.** It was written before this codebase existed. Finding a
  conflict, a redundancy or a missing prerequisite in it is the job.
- **Every requirement gets an ID, a verification method, and a MUST/SHOULD/WON'T.** A requirement
  nobody can test is a wish.
- **Record the consequence you dislike** — house ADR convention, and it applies to requirements too.
- Prefer "we do not yet know", written down, over a confident guess. `## Not yet specified` is a house
  heading for a reason.
- Sentence-case headings, no emoji, en-dashes. Match muster and infrastructure, not the reference
  tool's own docs.

## How the requester will judge the result

1. **The laundering test passes on a sample** — pick 10 requirements at random; none should be
   comprehensible only as a description of GitNexus, and none should carry a reference-internal name
   or magic constant.
2. **The architect's two goals are executable from the documents alone** — five flows documented, and
   a capability inventory carrying enough consumer / read-write / store / deployment metadata to
   cluster into modules without re-reading anything.
3. **No module decision pre-empted** — no crate names, no workspace layout, no dependency diagram;
   feature clusters offer alternatives where evidence is ambiguous.
4. **Every inherited-negative requirement present and laundered**, each with a verification method.
5. **Requirement IDs traceable both ways** between `FEATURES.md` and the SPEC files.
6. **User-story minimums met** — ≥5 admin, ≥10 developer, ≥10 agent, ≥3 non-technical.
7. **Deployment duality and the async question surfaced as decisions**, not silently resolved.
8. **AGPL-3.0 in the implementation constraints**, with the linkability and §13 consequences stated.
9. **Project memories exist** for the clean-room protocol and the AGPL constraint, with `MEMORY.md`
   pointers.
