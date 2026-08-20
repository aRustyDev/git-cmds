# Architectural syncs — the catalogue

- **Date:** 2026-08-19 · **Status:** living document; update as syncs complete
- **Purpose:** the requester wants recurring syncs with the Software Architect while the crate and
  module seams, and the SDK-versus-library-versus-binary clusters, are defined. This is the register
  of those syncs.

## How to read this

**Twenty-one syncs across four tracks** (**A6** added 2026-08-20). A flat list of twenty-odd checkpoints
is not a process, so they are grouped by what they gate, and the tracks run with different urgency:

| Track | Gates | Can it run in parallel? |
|---|---|---|
| **A — Requirements** | the SPEC | Mostly serial; A1 → A2 gate everything |
| **B — Architecture and seams** | the crate layout | Serial within the track, after A2 |
| **C — Extensibility and prior art** | specific capabilities | Parallel with B; each is independent |
| **D — Engineering practice** | how the project is run, not what it does | Fully parallel; **does not block requirements** |

**Track D is deliberately separated.** Telemetry, testing, CI/CD and commit hygiene are project
practice, not product behaviour. They matter, and mixing them into the requirements conversation
dilutes both. The one exception is noted at D1.

## Standing rules for every sync

- **The requirements author brings requirements; the architect brings structure.** When they conflict,
  the requirement is what must be true and the structure is what changes — unless the requirement
  turns out to be unfounded, in which case say so and amend it.
- **Never settle a seam on the requirements author's authority.** Their role is to test proposals
  against requirements and say what a proposal would make impossible.
- **Every sync ends with something written down** — a closed question, a new question, an ADR, or an
  amended requirement. A sync producing only shared understanding has produced nothing.
- **Every sync files its gaps immediately**, into the register in [`GAPS.md`](GAPS.md), not at the end
  of the track. A gap remembered is a gap lost.
- **Bring the disliked consequence.** House ADR convention; it applies to sync proposals too.
- **Prior-art syncs (C2–C4) share one outcome vocabulary:** *adopt as dependency · vendor · emulate
  the design · take the UX only · decline* — each with a reason, and a licence check.

---

## Status — 2026-08-20

The requirements corpus has been authored. **No sync has been held**, because no sync has taken place
with the architect — the standing rule is that a sync ends with something written down *jointly*, and
one party writing a document is not a sync. What follows is what each sync's inputs now are.

| Sync | State | What exists now |
|---|---|---|
| **A1** capability review | **ready to fire** | `analysis/0001-capabilities.md` (60 capabilities with consumer, mode, store and shape metadata) and `specs/01-personas-and-flows.md` (five personas, five flows) |
| **A2** vocabulary | **satisfied on the requirements side; ratification outstanding** | [`GLOSSARY.md`](GLOSSARY.md), written **before** any SPEC prose and used by every later document. Three deliberate renames, recorded with their aliases. **The architect has not reviewed it**, so it is ratified *for this corpus*, not jointly. |
| **A3** feature-list review | **ready to fire** | [`FEATURES.md`](FEATURES.md) — 61 features, 163 requirements, traced both ways by an **executable** ID-set diff rather than by reading |
| **A4** capability wishlist | **not started** | `GAP-006` awaits it. This is the one Track-A sync the authoring did not prepare, because it is generative rather than descriptive — and doing it alone would have produced the requirements author's wishlist rather than the requester's |
| **A5** the impact decision | **partially advanced** | `discussions/0001`'s four-term vocabulary is **adopted**, and "impact analysis" appears in no requirement. The seven axes remain open, and the default edge set — the highest-leverage single decision in the analysis surface — is unspecified. Still gated by **C3** |
| **A6** feasibility prototype gate | **new — see below** | `analysis/0003` produced the input |
| **B1** seam pressure test | **ready to fire** | `analysis/0002-feature-clusters.md` (four candidate clusterings, none preferred, ten invariants each cited to a requirement) and `discussions/0002-read-write-asymmetry.md` |
| **B2** abstractions | inputs partial | `analysis/0004-store-capability-matrix.md` — capability profiles per slot, and the portability hazards |
| **B3** data models | inputs partial | the authoritative-versus-derived table in `analysis/0004`; `questions/0004` on derived identities. **No schema exists**, correctly |
| **B4** data flows | inputs partial | flow **D** in `specs/01` — stages, ordering requirements, and what crosses a network hop per shape |
| **B5** interfaces and protocols | **ready to fire** | `specs/04` (`IF-1`–`IF-14`), `questions/0009` (TUI), and `GAP-017` (streaming may be latent in the contract) |
| **B6** library/SDK/binary split | inputs partial | `CON-4`/`CON-5` and their tension; `questions/0005`. **Also unblocks the engine name** |
| **B7** async | **blocked** | `EXT-9` requires a screening record; `analysis/0004` holds it and it is **empty** because no candidate exists (`GAP-010`, `questions/0010`) |
| **C1**–**C4** prior art | not started | `analysis/0003`'s permissive column is a **survey**, not verified use (`GAP-012`). Track C exists to convert claims into evidence |
| **D1** telemetry | **necessity now fully specified** | `specs/03` names the measuring signal for every budget, and `OPS-1` states plainly that `PERF-1`, `PERF-2`, `PERF-6`, `SCALE-3`, `SCALE-4` and staleness are unverifiable without it. `GAP-004` unchanged and unclosed |
| **D2**–**D4** practice | not started | `specs/08` states the testing and documentation **requirements**; the strategy is still D2's |

**The blocking chain to be aware of:** `questions/0010` → `EXT-9` screening → **B7** → the first store
implementation. Every step is cheap except the last, and the last is a rewrite if the order is wrong.

---

## Track A — Requirements

### A1 — Capability review
**Fires:** the capability inventory and the five flows are drafted.
**Input:** `analysis/` capabilities table; `01-personas-and-flows.md`.
**Output:** agreement the inventory is complete; a first read on natural groupings.

### A2 — Vocabulary review
**Fires:** immediately after A1, and **before any SPEC prose is written.**
**Input:** the candidate term list extracted from the capability inventory, plus the vocabulary
proposed in `discussions/0001`.
**Output:** **a ratified glossary every later document must use.** Terms added later are ratified at
the next sync as a dated amendment.

**Write the glossary first, not last.** A glossary written last summarises whatever vocabulary
emerged, which is why glossaries are usually useless; one written second is a constraint the SPEC
must satisfy. The hardest case already exists: *"impact analysis"* looks like one capability and is a
category containing four distinct terms (`discussions/0001`).

### A3 — Feature list review
**Fires:** `FEATURES.md` is drafted and traceable to SPEC requirement IDs.
**Input:** `FEATURES.md`; the SPEC requirement IDs; the capability inventory from A1.
**Output:** every feature traces both ways to a requirement; every requirement is reachable from a
feature; anything in neither is either filed as a gap or explicitly dropped.

This is the **traceability** checkpoint, and it is distinct from A1. A1 asks "have we found
everything?"; A3 asks "does the feature list and the requirement set describe the same system?" The
failure it catches is a feature nobody can point at a requirement for, and a requirement no feature
delivers — both of which are common and neither of which A1 sees.

### A4 — Capability wishlist: what we want that the prior art does not have
**Fires:** after A1, before the SPEC's functional requirements are finalised.
**Input:** the capability inventory; the feature-gap matrix; the reference tool's known surface; the
permissive-alternative survey.
**Output:** a ranked list of **net-new** capabilities we want, each marked with a confidence level and
filed into the gap register.

**This is a deliberately generative sync, not an audit.** Every other sync in Track A is about
faithfully capturing what was asked for. This one asks what nobody has asked for yet. Prompts worth
bringing:

- What can a **code graph plus a fleet of agents** do that neither does alone?
- What does an agent need that a *human*-oriented tool would never build — machine-readable
  confidence, budget-aware truncation, stable ids across runs, batch queries?
- What becomes possible once **cross-repository** contracts are first-class?
- What does the **write** side look like? The prior art is overwhelmingly read-only; refactoring,
  codemods and migration assistance are barely touched.
- Which of the reference tool's **known weaknesses** is actually an opportunity rather than a defect
  to avoid?

Ideas that survive get filed as `hypothetical` gaps and must be promoted to `known` before anything
is scheduled — see [`GAPS.md`](GAPS.md).

### A5 — The impact decision
**Fires:** before impact requirements are finalised.
**Input:** `discussions/0001-what-impact-analysis-means.md`.
**Output:** the seven axes settled; whether one traversal serves all projections. Feeds terms back to
the A2 glossary.

### A6 — Feasibility prototype gate *(added 2026-08-20)*
**Fires:** after A1, and **before anything is scheduled** against a capability the precedent analysis
marks `elevated`.
**Input:** `analysis/0003-feature-gaps.md`, specifically the seven `elevated` and nine `inaccessible`
entries.
**Output:** for each `elevated` capability, either a prototype that establishes feasibility, or an
explicit `accepted` gap with a revisit trigger.

**Why this sync did not exist and needs to.** The gap register's binding rule is *nothing unverified
gets scheduled* — but that rule is about the confidence in a **gap**, and it does not cover a
requirement whose *feasibility* is unestablished. `analysis/0003` found seven capabilities with **no
precedent anywhere**, which means no proof they can be built at all, and nothing in the other nineteen
syncs owns that. A requirement with a verification method and no feasibility evidence is not a wish —
it is worse, because it looks rigorous.

**The candidates, and they are not evenly distributed.** Four of the seven are one entangled cluster:
flow derivation, cluster derivation, their **identities** (`GAP-007`), and the compute-set rule for
change detection (`GAP-009`). Derived structures are what make incrementality change *output* rather
than merely cost, and identity stability is what makes recomputation safe or unsafe. **Prototype the
cluster, not the four items.** The remaining three — patch-without-checkout diff impact, evidence-class
weighting, and AST-accurate rename with atomic index writeback — are independent.

**Cheapest first, and one of them may delete work rather than create it:** `GAP-007`'s verification is a
single check of whether derived identifiers are externally visible at all. If they are not, the hardest
algorithmic requirement in the corpus is **refuted**. Do that before prototyping anything.

**Note also the `inaccessible` class**, which this sync should treat differently from `elevated`:
feasibility is proven and the design is unavailable under the clean room. Those need design effort, not
feasibility prototypes, and conflating the two wastes the prototype budget.

---

## Track B — Architecture and seams

### B1 — Seam pressure test
**Fires:** before any clustering is written down as preferred.
**Input:** the requester's module-seam sketch (Appendix B of `PROMPT.md`), plus its ten
coverage gaps and the questions it raises.
**Output:** where each coverage gap lands; whether the decomposition stays command-shaped or turns
domain-shaped.

### B2 — Architectural abstractions
**Fires:** after B1, before the abstractions are implemented anywhere.
**Input:** the swappable-store requirements; the deployment duality; the read/write asymmetry.
**Output:** the named abstraction set, and for each: what it hides, what it must not leak, and what
the default implementation is.

The abstractions in play, at least: **storage** (graph · vector · SQL · search · text-search ·
key-value — six store kinds, each embedded↔networked), **networking and transport**, **repository
acquisition and credentials**, **parsing and language support**, **embedding provision**, **ranking
and fusion**, **job execution and scheduling**, **configuration**, **identity and authorisation**,
**telemetry**.

House precedent to cite, not to mandate: all persistence behind a repository trait with **no concrete
datastore type in the public API**, and per-backend feature flags with an in-memory default so tests
need no external engine.

### B3 — Data models: the core, and how it stays fluid
**Fires:** after B2, before any schema is written.
**Input:** the capability inventory; the ratified glossary from A2; the store set from B2.
**Output:** the core model, the peripheral model, the evolution strategy, and a placement table.

Three distinct questions, and the third is the one usually skipped:

1. **What is core?** Which entities and relations are so central that changing them is a redesign —
   and which are additive detail. Anything core needs a much higher bar for change.
2. **What goes where?** A placement table: for each data kind, which store owns it and why.
   Graph for structure and traversal; vectors for similarity; text/search indexes for ranking;
   key-value for ephemeral and derived; SQL for registries, metadata and anything relational. Every
   placement needs a reason, and every duplication across stores needs an owner.
3. **How does the model evolve without a full reindex?** This is a hard requirement, not an
   aspiration: the grounding found that in the reference implementation **any schema-fingerprint
   change disabled incrementality entirely and forced a full reindex**, and the parse cache was keyed
   on the package version, so *every release* reindexed everything. Patterns to consider: additive-only
   changes, versioned node and edge kinds, a migration path per store, tolerating unknown fields on
   read, and separating the *derived* model (rebuildable, may be dropped) from the *authoritative*
   model (must be migrated).

### B4 — Data flows across the ecosystem
**Fires:** after B3.
**Input:** the placement table from B3; the pipeline's phase structure.
**Output:** a data-flow document, and the consistency contract between stores.

The question the requester asked directly — **how does graph data relate to vector, key-value and SQL
data?** Sub-questions that have to be answered together:

- **What is the system of record?** If the graph is authoritative, everything else is a projection
  and can be rebuilt. If not, there are multiple truths and they can disagree.
- **Which stores are derived and therefore droppable?** Vectors and search indexes are usually
  rebuildable from source; key-value is usually a cache. Say so explicitly, because it determines
  what a disaster-recovery path has to preserve.
- **Can the stores diverge, how is divergence detected, and what happens then?** Two stores updated
  non-atomically will diverge. A checksum, a generation counter, or a reconciliation pass — pick one.
- **What is the write ordering** on index, on incremental update, and on delete? A vector left behind
  after its symbol is gone is a wrong answer, not a leak.
- **What crosses a network hop** in the microservice shape that does not in the CLI shape, and what
  does that do to latency budgets?

### B5 — Interfaces and protocols
**Fires:** after B2, parallel with B3/B4.
**Input:** the capability inventory; the consumer list from the flows.
**Output:** which surfaces exist, which are first-class, and what they share.

Surfaces named by the requester: **API · WebUI · TUI · CLI · MCP.**

⚠️ **A TUI is not in the capability list at all.** It arrived in this instruction and is a genuine new
requirement — file it as a gap (`discovered`) and specify it, or explicitly decline it.

The real question is not "which surfaces" but **what sits underneath them**: is there one contract all
five project, or does each grow its own? Five surfaces over five hand-rolled adapters is how a
codebase ends up with divergent behaviour per interface — the grounding found exactly that in the
reference, where two entry points to nominally the same functionality had different authentication,
different concurrency behaviour, and different tool inventories. Decide:

- One internal contract with thin per-surface projections, or per-surface implementations?
- Which surfaces are **read-only** and which may mutate?
- Where does authentication terminate, and is it the same place for all five?
- The WebUI is specified **by contract** as a downstream consumer — does the TUI get the same
  treatment, or is it in-tree?
- MCP is an agent protocol with its own conventions (tool inventories, session semantics, output
  budgets). Is it a projection of the API, or a first-class surface with its own contract?

### B6 — Library / SDK / binary split
**Fires:** before the split is fixed.
**Input:** the AGPL linkability constraint; the deployment duality; read/write asymmetry; the
abstraction set from B2.
**Output:** the cluster boundaries; what may not appear in a library's public API. **Also unblocks the
engine-library name** (`questions/0001`).

### B7 — The async decision
**Fires:** during backend screening, **never after.**
**Input:** which required stores are async-only.
**Output:** an ADR. House rule: *retrofitting async through a synchronous trait is a rewrite.*

---

## Track C — Extensibility and prior art

Each of C2–C4 uses the shared outcome vocabulary and a scorecard. House precedent for the method is
the estate's 20-candidate datastore screening, which pairs a mandate document with a per-candidate
scorecard template — copy that shape rather than inventing one.

### C1 — Custom tree-sitter grammars and LSP servers
**Fires:** before language-support requirements are finalised.
**Input:** the required language list; the extensibility requirement.
**Output:** whether either extension path is supported, and what the contract is.

Two separable questions that the capability list bundles:

- **Custom grammars.** Can a deployment add a language without a fork? Grammars are usually native
  code compiled at build time, which makes "configurable" much harder than it sounds — a
  runtime-loadable grammar is a very different commitment from a build-time one. Note also the
  escape hatch the grounding found in the reference: a language can be supported by a **standalone
  processor bypassing the grammar contract entirely**, which is materially cheaper for declarative
  config formats where most of the extraction contract is meaningless.
- **LSP servers.** Driving analysis from a language server would inherit resolution quality from
  tooling that properly understands each language. But the grounding found the reference's
  per-language contract is **shaped entirely around syntax-tree access**, so an LSP-backed provider
  could not satisfy it — meaning this is a *second analysis architecture*, not a configuration flag.
  Decide whether that is wanted, and if so whether the two paths share a model.

### C2 — ast-grep
**Fires:** parallel; before the rename and structural-check requirements are finalised.
**Why it matters here:** structural search and rewrite over syntax trees, with a pattern language.
It bears directly on two requirements — **AST-accurate rename** (the grounding's inherited-negative:
the reference's rename was a whole-file regex that rewrote comments and string literals) and
**read-only structural checks**. Permissively licensed, so a dependency is licence-compatible with
AGPL.
**Decide:** adopt as a dependency for rewriting · emulate the pattern language · take only the UX
concept of structural patterns · decline. And if adopted: does its pattern language become part of our
public interface, which is a compatibility commitment.

### C3 — difftastic
**Fires:** parallel; **before the diff-impact requirements are finalised** — this one has a hard
dependency into A5.
**Why it matters here:** it computes diffs **structurally over syntax trees** rather than over lines.
That is directly relevant to the weakest link in diff impact: mapping a **line**-based diff onto
symbols is lossy, and a syntactic diff would give a far better change→symbol mapping. If diff impact
is a first-class capability, this is the most architecturally consequential item in Track C.
**Decide:** adopt · emulate the approach · use line diffs and accept the loss · decline. And: does a
structural diff change the *input contract* for impact (`discussions/0001` axis 5)?

### C4 — Serena
**Fires:** parallel; alongside C1 and B5.
**Reference:** <https://oraios.github.io/serena/01-about/000_intro.html>
**Why it matters here:** an LSP-backed, symbol-level toolkit exposed over MCP — so it overlaps both
the LSP question (C1) and the MCP surface (B5). It is also the tool that was recommended, in the
upstream discussion of the reference implementation's licence, as the thing to use instead. Worth
understanding properly rather than dismissing.
**Decide:** adopt as a dependency or sidecar · emulate its symbol-level MCP tool surface · take
inspiration for tool granularity and naming · treat as complementary and integrate · decline. Note
particularly what its **tool granularity** teaches: how it splits capability across tools is a
design input for our own MCP surface.

---

## Track D — Engineering practice

Parallel and non-blocking for requirements, with one exception.

### D1 — Telemetry
**Fires:** early — this is the exception that touches requirements.
**Input:** the non-functional requirements; the concurrency and latency budgets.
**Output:** the telemetry plan: traces, metrics, logs, and what is emitted at which boundary.

**Why it is not purely practice:** several requirements are **unverifiable without it.** The
concurrency requirement ("reads scale with readers per replica"), the n95 latency budget, and index
staleness are all claims that need measurement to be testable. A requirement nobody can verify is a
wish — so the telemetry plan is part of how the SPEC's `## Verification` sections get filled in.

Decide: OpenTelemetry or otherwise; trace propagation across the surfaces from B5; what a span
boundary is; cardinality discipline for metrics; structured logging and its levels; whether telemetry
is optional in the CLI shape and mandatory in the service shape; and what a caller can see about its
own request.

### D2 — Testing strategy
**Fires:** parallel.
**Input:** the requirement set; the release gates.
**Output:** the testing levels, what each proves, and the release gates.

Kinds to decide on: unit · integration · **property-based** · snapshot · **mutation** (note the
repository's `.gitignore` already anticipates `cargo mutants`) · benchmark and regression-guard ·
end-to-end per deployment shape · **conformance tests per store backend** (essential, given six
swappable store kinds — one suite every backend must pass is what makes them genuinely swappable) ·
adversarial and fuzz for anything parsing untrusted input.

House precedent exists and should be read rather than reinvented: the estate carries a testing
**strategy** (coverage taxonomy, tool roster) and testing **policies** (property and regression,
standing policies), plus a spec-level vocabulary of levels, seeded fixtures and release gates.

Two specific obligations from the grounding: the inherited-negative requirements each need a
verification method, and **constraints must be executable rather than documentary** — a comment
saying "don't do this" does not satisfy a constraint.

### D3 — CI/CD and supply chain
**Fires:** parallel; before the first release.
**Input:** the branching model; the publishing target; the attestation requirements.
**Output:** the pipeline design, and one decision per item below.

Named by the requester: **git-cliff · release-please · PR automation · branching strategy · tagging ·
cosign · attestation · SLSA · OSSF · crates publishing.**

Points worth deciding rather than defaulting:

- **git-cliff and release-please overlap.** Both derive versions and changelogs from commit history.
  Pick one as authoritative; running both is how a changelog ends up generated twice with different
  content. Note the estate already uses **release-please** parsing Conventional Commits, which is
  house precedent.
- **Crates publishing is where forks break.** The grounding found the reference's publish flow
  authorises via registry-side OIDC bound to one specific org and repo, so a fork's publish fails
  **after the atomic tag push has already landed** — which is why its pipeline carries failure
  cleanup that deletes the tags. Whatever we build, decide what happens when publish fails after
  tagging.
- **Signing and provenance:** cosign keyless signing, provenance attestation, SBOM generation, and
  whether an admission policy consumes them. The reference has real prior art here worth copying — an
  admission policy that rejects any image not signed by the release workflow running from a version
  tag, with the registry-prefix loophole explicitly closed.
- **OSSF Scorecard** as a gate or a signal, and which checks are mandatory.
- **Branching and tagging:** trunk-based or otherwise; what a tag means; whether release commits are
  a PR.
- **Keep the org-portable core separate from the org-bound parts.** The grounding found that in the
  reference, the entire test-and-quality chain used zero secrets and zero repository variables, which
  is exactly why it was portable — and only six workflow files carried org bindings. Design for that
  split from the start.

### D4 — Context files, commits and changelog hygiene
**Fires:** parallel; ideally before much is committed.
**Input:** the estate's existing conventions.
**Output:** the deltas from house convention, and any repo-specific additions.

**Mostly already settled by house convention — this sync is about the deltas, not a blank page:**

- **Conventional Commits** for every commit subject and PR title, because release automation parses
  them.
- **Work-item IDs go in a commit footer (a trailer), never in the subject.** A bracketed prefix
  breaks Conventional Commits parsing and makes release tooling skip the commit; a parenthesised
  suffix leaks the ID into the changelog. `Refs:` survives squash-merge and is ignored by the release
  tool. Never use `BREAKING CHANGE:` as the ID token — it is reserved and forces a major bump.
- **Keep-a-Changelog bodies**, with the changelog generated from commits rather than hand-edited.
- **Context files:** `AGENTS.md` is per-directory and vendor-neutral (what this is, how to build and
  test it); `CLAUDE.md` is root-only and behavioural (how to work here); no per-crate `CLAUDE.md`.
  Root context files are read every session, so budget them — depth belongs in `.claude/plans/**` or
  `docs/`, referenced by path.
- **Rules go in `.claude/rules/**`** and auto-load; never `@`-import a rule from `CLAUDE.md`, because
  imports are eager and defeat `paths:` scoping. Every path-scoped rule leaves a one-line pointer in
  the rules README so a constraint is never invisible.

Decide: whether this repo needs its own `.claude/rules/`; the commit-scope vocabulary once crates are
named; whether changelog entries are per-crate or per-workspace; and how a multi-crate workspace
versions — together or independently.

---

## Ordering and dependencies

```text
A1 ──▶ A2 ──▶ A3
  │      │
  │      └──▶ B1 ──▶ B2 ──▶ B3 ──▶ B4
  │                   │
  │                   ├──▶ B5
  │                   └──▶ B6 ──▶ B7        B6 unblocks the engine name
  ├──▶ A4                                    (questions/0001)
  ├──▶ A5 ◀── C3                             C3 gates the diff-impact decision
  └──▶ A6                                    A6 gates SCHEDULING, not design

questions/0010 ──▶ EXT-9 screening ──▶ B7    the chain that ends in a rewrite
C1, C2, C4  ── parallel, feed B5 / A5 / the rename requirement
D1 ── early (requirements depend on it)
D2, D3, D4 ── parallel, non-blocking
```

**Hard gates, the ones that actually matter:**

1. **A2 before any SPEC prose.** Vocabulary drift compounds.
2. **C3 before A5.** A structural-diff decision changes impact's input contract.
3. **B7 during backend screening, never after.** Retrofitting async is a rewrite.
4. **B3 before any schema.** The evolution strategy is not retrofittable.
5. **D1 before the non-functional requirements are called done.** They are unverifiable without it.

## Amendments

- **2026-08-19** — Created with twenty syncs across four tracks. Supersedes the flat S1–S6 list
  previously inline in `PROMPT.md`; the mapping is A1←S1, A2←S2, B1←S3, A5←S4, B6←S5, B7←S6.
- **2026-08-20** — **Added `A6`, the feasibility prototype gate**, and a `## Status` section recording
  each sync's inputs after the requirements corpus was authored. A6 exists because the gap register's
  binding rule covers confidence in a *gap* and not feasibility of a *requirement*, and
  `analysis/0003` found seven capabilities with no precedent anywhere — so no proof they can be built.
  Nothing in the original twenty owned that. **A2 is satisfied on the requirements side** (the glossary
  was written before any SPEC prose and is used throughout) but its joint ratification with the
  architect is outstanding. **B7 is blocked** on an empty screening record; the chain
  `questions/0010` → `EXT-9` → `B7` is now drawn in the ordering diagram because it is the one path
  whose failure mode is a rewrite rather than a delay.
