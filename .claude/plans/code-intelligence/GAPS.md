# Capability gaps — process and register

- **Date:** 2026-08-20 · **Status:** living document
- **Purpose:** record what the product cannot yet do, or what our design does not yet cover, with
  enough structure that gaps become backlog items rather than folklore — and a cycle that returns to
  them.

## Why this needs a process at all

A gap noticed in a sync and not written down is indistinguishable from a gap nobody noticed. The
failure mode is not forgetting that gaps exist; it is **remembering them as vague unease** — "I think
there was something about YAML" — which is unactionable and unassignable.

The second failure mode is subtler and worse: **acting on an unverified gap.** Building for something
absent that turns out to have been present all along is pure waste, and it is easy, because a gap
feels like knowledge. The register exists to keep confidence attached to every claim.

## The two dimensions

The requester's terms — *known, accepted, discovered, inferred, presumed, hypothetical* — are two
different things mixed together, and separating them is what makes the register queryable.
**`accepted` is a disposition; the rest are statements of confidence.** A gap can be *known and
accepted*, or *known and scheduled*, or *hypothetical and open* — and "show me every high-confidence
gap we have not dispositioned" is the question the register has to be able to answer.

### Confidence — how do we know this is a gap?

| Value | Means | Verified? |
|---|---|---|
| `known` | Someone looked, and it is absent. Names what was checked. | ✅ |
| `discovered` | Surfaced unexpectedly during other work, and confirmed. | ✅ |
| `inferred` | Not directly observed, but follows necessarily from a requirement or another gap. | ⚠️ derived |
| `presumed` | Believed absent; nobody has checked. | ❌ |
| `hypothetical` | Speculative. May not be a gap, or may not be wanted. | ❌ |

**The binding rule: nothing unverified gets scheduled.** A `presumed` or `hypothetical` gap must be
promoted to `known` — or `refuted` — before any work is scheduled against it. `inferred` may be
scheduled only when the inference chain is written down and its premise is itself verified.

This rule exists because of a measured failure in the prior grounding: a capability whose *name*
matched a backlog item was repeatedly taken as evidence the item was done, and adversarial refutation
overturned three of four such verdicts. The same trap runs in reverse — a capability whose absence is
*assumed* is not a gap until someone looks.

### Disposition — what are we doing about it?

| Value | Means | Requires |
|---|---|---|
| `open` | Recorded, not yet triaged. | — |
| `scheduled` | Accepted as work; on the backlog. | verified confidence + a backlog link |
| `accepted` | **Deliberate WON'T.** A known hole we are living with. | a reason **and** a revisit trigger |
| `refuted` | Investigated; not actually a gap. | what was checked |
| `closed` | Filled. | where it landed |

**`accepted` is not `closed`.** An accepted gap is a documented, deliberate hole — and it needs a
**revisit trigger** (a condition, not a date) or it becomes permanent by default, which is how "we
decided not to" silently becomes "nobody remembers deciding".

### Kind — what sort of gap is it?

One register, not three, because separate registers guarantee one gets forgotten.

| Kind | Means |
|---|---|
| `capability` | The product should be able to do something it cannot. |
| `coverage` | A required capability exists but our design has no home for it. |
| `verification` | We cannot currently prove a requirement is met. |
| `knowledge` | We do not know something we need to know to decide. |

## Entry format

```markdown
### GAP-nnn — <short title>
- **kind:** capability | coverage | verification | knowledge
- **confidence:** known | discovered | inferred | presumed | hypothetical
- **disposition:** open | scheduled | accepted | refuted | closed
- **source:** which sync, document, or conversation surfaced it (and the date)
- **missing:** what the system cannot do, stated as behaviour
- **consequence:** what goes wrong if this stays open
- **verification:** how we would confirm this is genuinely a gap — **required** when confidence is
  presumed or hypothetical
- **revisit:** the condition that reopens this — **required** when disposition is accepted
- **relates:** blocks / blocked by / sync that owns it / backlog link
```

Numbering is sequential and never reused. Gaps are not renumbered when refuted — a refuted gap is
evidence, and its number stays.

## The cycle

Four rhythms, deliberately different in frequency.

### 1. File on sight — continuous
Anyone who notices a gap files it immediately with whatever confidence is honest, including
`hypothetical`. **A low-confidence entry is far better than a missing one**, because the register can
raise confidence later and cannot invent an entry nobody wrote.

### 2. Triage — at the start of every sync
New entries since the last sync get a `kind`, a `confidence` and a `disposition`. This is fast — a few
minutes — and its only job is that nothing sits `open` and unclassified for two syncs running.

### 3. Verification pass — before each track boundary
Every `presumed` and `hypothetical` entry either gets verified (→ `known` or `refuted`) or gets a dated
"still unverified" stamp. **An entry carrying three unverified stamps is escalated**: either someone
verifies it, or it is explicitly `accepted` with a revisit trigger. Drifting indefinitely is the one
outcome not allowed.

### 4. Sweep — at each track boundary (end of A, B, C, D)
Full register review:
- Re-check every `accepted` entry against its revisit trigger. Triggers fire silently; nothing else
  will notice.
- Re-check `inferred` entries whose premise has since changed — an inference is only as good as what
  it rested on.
- Escalate entries unchanged across two sweeps.
- Confirm every `scheduled` entry still has a live backlog link.

## Backlog integration

A `scheduled` gap becomes an item in the project's work register. **Which register that is has not been
decided** — see `questions/0002-where-does-the-backlog-live.md`. Whatever it turns out to be, it must
support:

- **A bidirectional link.** The gap names the item; the item names the gap. One-way links rot.
- **Confidence and disposition surviving the handoff.** A backlog item that has lost the fact it came
  from a `presumed` gap will get worked on faith.
- **A queryable revisit trigger**, so accepted gaps can be swept without reading every entry.

Until that is decided, `scheduled` entries carry their acceptance criteria inline here, so the
handoff is a copy rather than a reconstruction.

## Register

Seeded 2026-08-20 to demonstrate each confidence level. Not exhaustive — the A-track syncs will fill
it out substantially, and A4 exists specifically to generate `hypothetical` entries.

### GAP-001 — TUI surface is unspecified
- **kind:** capability · **confidence:** `discovered` · **disposition:** `open`
- **source:** requester instruction, 2026-08-20, adding a TUI to the named interface set
- **missing:** a terminal user interface. The original capability list names a web UI, a CLI and an
  agent protocol; a TUI appeared later and has no requirements at all.
- **consequence:** an interface with no requirements gets built to whatever the implementer assumed,
  or silently dropped. It also changes B5's answer — four surfaces over a shared contract is a
  different design from three.
- **relates:** owned by **B5**. Decide: specify it, or decline it explicitly.

### GAP-002 — The relational store has no home in the design
- **kind:** coverage · **confidence:** `known` · **disposition:** `open`
- **source:** review of the requester's module-seam sketch, 2026-08-19
- **missing:** the requirements demand a relational store that swaps between embedded and server
  deployments. The sketch's only SQL-shaped component is marked out of scope and described as an ORM
  for a different product, so the required store is unplaced.
- **consequence:** either a required capability is missing, or two unrelated concerns get merged into
  one component because they share the word "SQL".
- **relates:** owned by **B1**, then **B3** for placement. Blocks the placement table.

### GAP-003 — Change→symbol mapping may need a structural diff
- **kind:** capability · **confidence:** `inferred` · **disposition:** `open`
- **source:** inferred from the diff-impact accuracy requirement, `discussions/0001` axis 5
- **missing:** mapping a **line**-based diff onto symbols is lossy — a moved function reads as a large
  deletion and an unrelated insertion. Accurate diff impact plausibly needs a **syntax-aware** diff.
- **consequence:** if this is real and unaddressed, diff impact is inaccurate in exactly the case it
  is most wanted: a refactor that moved code.
- **verification:** the inference rests on the premise that line-diff→symbol mapping loses accuracy on
  moves and reformatting. Confirm with a worked example before scheduling.
- **relates:** owned by **C3**; gates **A5**.

### GAP-004 — Several non-functional requirements are unverifiable
- **kind:** verification · **confidence:** `known` · **disposition:** `open`
- **source:** requirements-coverage review, 2026-08-19
- **missing:** no telemetry. The read-concurrency property, the n95 latency budget and index staleness
  are all requirements with no means of measurement.
- **consequence:** unverifiable requirements are wishes. They also cannot appear under
  `### What is proven` in any SPEC verification section, which makes the SPEC dishonest by omission.
- **relates:** owned by **D1**. This is why D1 is the one Track-D sync that is not merely practice.

### GAP-005 — Declarative infrastructure configuration is not analysable
- **kind:** capability · **confidence:** `known` · **disposition:** `open`
- **source:** grounding of the prior art, 2026-08-19
- **missing:** analysis of declarative infrastructure and configuration formats — infrastructure-as-code
  and container-orchestration manifests. No surveyed prior art covers these well, and they are a large
  share of what agents in this environment actually work on.
- **consequence:** the graph is blind to a substantial fraction of the target corpus, so impact and
  search answers are confidently incomplete for it.
- **relates:** owned by **C1**. Note these formats are declarative, so most of a
  general-purpose language-extraction contract is meaningless for them — a lighter path may be the
  right shape.

### GAP-006 — The write side is barely explored
- **kind:** capability · **confidence:** `hypothetical` · **disposition:** `open`
- **source:** A4 framing, 2026-08-20
- **missing:** beyond a single rename operation, the surveyed prior art is overwhelmingly read-only.
  Codemods, mechanical migrations and multi-step refactors guided by the graph may be a significant
  opportunity — or may be out of scope entirely.
- **consequence:** if it is an opportunity, we will not notice while specifying a read-only product.
- **verification:** **speculative — do not schedule.** A4 should develop or kill it. Promote only with
  a concrete named capability and a consumer who wants it.
- **relates:** owned by **A4**.

### GAP-007 — Derived graph structures may need stable identities across runs
- **kind:** capability · **confidence:** `inferred` · **disposition:** `open`
- **source:** inferred from the grounding, 2026-08-19
- **missing:** structures derived by whole-graph algorithms — clusters and derived flows — are
  recomputed wholesale. If their identifiers are also part of the query surface, then recomputation
  changes answers rather than merely costing time, and any stored reference to them breaks.
- **consequence:** cached results, saved views, agent-held references and cross-run comparison all
  become unreliable, silently.
- **verification:** confirm that derived identifiers are (or will be) externally visible. If they are
  purely internal, this is refuted.
- **relates:** owned by **B3**; interacts with **A5** and the incrementality requirements.

### GAP-008 — No confidence model for contract-inferred cross-repository edges
- **kind:** knowledge · **confidence:** `presumed` · **disposition:** `open`
- **source:** cross-repository requirements review, 2026-08-19
- **missing:** an edge inferred from a declared contract between repositories is weaker evidence than
  a call observed in code, and we presume no surveyed prior art offers a usable confidence model for
  the distinction.
- **consequence:** cross-repo impact answers mix observed and inferred edges at equal weight, which
  either overstates blast radius or hides real reach — and the caller cannot tell which.
- **verification:** **unverified.** Nobody has surveyed prior art for cross-repo edge confidence.
  Check before treating this as a gap.
- **relates:** owned by **B4**; interacts with **A5** axis 3 (edge admissibility).

### GAP-009 — There is no rule for deciding the compute set before the expensive work
- **kind:** capability · **confidence:** `known` · **disposition:** `open`
- **source:** requirements authoring, 2026-08-20, while writing `FR-011`
- **missing:** `FR-011` requires the incremental-versus-full decision to be taken **before** the
  expensive work, and to determine the **compute** set rather than only the write set. No rule for
  computing that set exists. Cross-file resolution needs data from files that did not change, so a
  correct compute set is strictly larger than the change set — and how much larger is the unknown.
- **consequence:** without it, `FR-011` is unimplementable and the honest fallback is what prior art
  did: run everything, then decide. `analysis/0003` marks this `elevated` — no precedent anywhere — and
  `PERF-6`, `FR-012` and `COR-2` all depend on it.
- **verification:** the gap is verified: the rule does not exist and nothing was found that has one.
  What needs verifying is any *candidate* rule. Note the grounding recorded that the obvious approach —
  following import edges — is insufficient for inheritance and type resolution, and degrades unsafely
  when it fails, so a candidate must be checked against those cases specifically.
- **relates:** blocks `FR-011`; entangled with `GAP-007`; decides `discussions/0002` axis 4. **This and
  `GAP-007` are one risk.** Prototype before scheduling.

### GAP-010 — The per-slot store product list is unknown
- **kind:** knowledge · **confidence:** `known` · **disposition:** `open`
- **source:** `PROMPT.md` Appendix A, read 2026-08-20 — it records that the requester named products per
  slot, and the list did not survive into the prompt
- **missing:** which products are the compatibility targets for the six store slots. Only the slot names
  were carried.
- **consequence:** `EXT-9`'s async screening record is empty, so `questions/0003` cannot be answered —
  and that question must be answered during screening, never after, because retrofitting async through
  a synchronous trait is a rewrite.
- **relates:** owned by `questions/0010`. Mitigated: `specs/04` specifies capability profiles with
  `presumed` candidates, so this is an inconvenience rather than a blocker by design.

### GAP-011 — Two required store slots have no consuming capability
- **kind:** coverage · **confidence:** `known` · **disposition:** `open`
- **source:** `analysis/0001` store cross-tabulation, 2026-08-20
- **missing:** the capability list requires a swappable **search index** and **key-value store**. Counting
  the capability inventory, **no capability reads or writes either.**
- **consequence:** an abstraction with no consumer cannot be validated, and its conformance suite tests an
  interface nobody calls. Building both is speculative work; dropping them silently contradicts the
  capability list.
- **relates:** `EXT-4`, `EXT-6` specify them as optional and flag this. Owned by **B2**. Note
  `questions/0011` could give the search slot a consumer if the wiki persists documents.

### GAP-012 — The permissive-alternative precedent column is unverified
- **kind:** knowledge · **confidence:** `presumed` · **disposition:** `open`
- **source:** `analysis/0003`, 2026-08-20
- **missing:** every ✓ in that matrix's permissive column is a capability **claim** from a survey. No
  permissive tool was installed, run or read.
- **consequence:** the matrix is used to decide which capabilities carry proof of feasibility. If a claim
  is wrong, a capability moves from `routine` to `elevated` and should have been prototyped.
- **verification:** **unverified, and the grounding records exactly this trap** — a capability whose
  *name* matched was repeatedly taken as evidence it existed, and adversarial refutation overturned
  three of four such verdicts. Track **C** exists to convert claims into verified precedent. Until then
  treat the column as `presumed` throughout.
- **relates:** owned by Track **C**. Bears on `FR-005` (declarative formats) and `FR-026` (diff impact)
  most, since both rest on a single unverified claim.

### GAP-013 — No detection or response for a misbehaving agent
- **kind:** capability · **confidence:** `discovered` · **disposition:** `open`
- **source:** `analysis/0006-threat-model.md`, 2026-08-20 — surfaced while enumerating adversaries
- **missing:** with up to ~10 000 agent principals acting autonomously, one behaving badly with a
  **legitimate** credential is a routine expectation. The corpus records the action (`SEC-6`) and bounds
  it (`SEC-9`) and offers nothing for detecting or responding to it: no anomaly signal, no revocation
  requirement beyond credential expiry, and no policy for what happens after a limit is hit repeatedly.
- **consequence:** the likeliest incident class is the least mitigated. And `OPS-6` forbids per-principal
  metric labels for cardinality reasons — correctly — which removes the obvious detection surface, so
  this is a design tension rather than an oversight.
- **relates:** owned by **D1** (telemetry) jointly with security. Adversary T3.

### GAP-014 — `git-ctx` is unavailable on crates.io, and the incumbent has colliding semantics
- **kind:** knowledge · **confidence:** `known` · **disposition:** `open`
- **source:** registry check, 2026-08-20 — `questions/0001`'s own outstanding verification item
- **missing:** a publishable name for the CLI. A live MIT crate named exactly `git-ctx` (0.1.1, published
  2022, not yanked) is *"a git custom command to list and switch most recent branches"*.
- **consequence:** two problems. The registry name cannot be used; and the `-ctx`-signals-context-switching
  risk that `questions/0001` recorded as an acceptable residual is now a **live conflict with a published
  tool that does exactly that**. Both are cheaper to settle before anything ships than after.
- **relates:** owned by the requester, via `questions/0001`. Not blocking — nothing is published.
  Mitigating facts: 13 recent downloads, no repository URL, untouched since March 2022.

### GAP-015 — MUST-level requirements are not prioritised among themselves
- **kind:** coverage · **confidence:** `known` · **disposition:** `open`
- **source:** self-assessment against the external SRS reference's quality criteria, `specs/09`, 2026-08-20
- **missing:** 58 features and ~140 requirements are MUST, with no ordering. Nobody has said which MUST is
  allowed to slip if a date pressures the scope.
- **consequence:** under time pressure a capability gets dropped by whoever is closest to it, and is later
  described as never having been in scope. That is the failure the house convention of naming out-of-scope
  items **by name** exists to prevent, applied one level up.
- **relates:** arguably the architect's sequencing rather than a requirements concern. `questions/0006`
  holds the open residual and names the natural answer if one is wanted: the `GAP-007`/`GAP-009` cluster
  is the deepest dependency and cannot be deferred without deferring the product.

### GAP-016 — The wiki's prose half can only be verified by a person
- **kind:** verification · **confidence:** `known` · **disposition:** `open`
- **source:** requirements authoring, 2026-08-20 · **narrowed the same day**
- **missing:** narrative quality is not automatically assertable. `FR-036`'s **structure** is fully
  testable — one page per derived cluster plus an overview, cross-references resolving to graph
  identities, index generation per page, stability across runs. Its **prose** is not, and its verification
  names a reviewer.
- **consequence:** one requirement in the corpus has a human in its verification loop. That is a genuine
  limit rather than a defect, and the risk is that it quietly becomes untested rather than
  human-tested.
- **⚠️ This entry was filed wrong and is corrected here.** As originally written it claimed `FR-036` had
  **no** verification method because the wiki had no output contract. **That was false.** The prior art
  ships this capability and its **public documentation** describes the contract — which the clean-room
  protocol explicitly permits reading. The requirements author asserted an absence without looking in the
  one place that was both permitted and obvious. **This is the register's own failure mode, from its own
  opening section: acting on an unverified gap, where a gap felt like knowledge.** Recorded rather than
  edited away, because a refuted claim is evidence about the process.
- **relates:** `questions/0011`, now narrowed to three residuals — whether prose is wanted in v1 (a
  security-surface decision), whether cluster-shaped modules read well, and where the document set goes.

### GAP-017 — Streaming and cancellation of a read may be latent in the contract but are unspecified
- **kind:** coverage · **confidence:** `inferred` · **disposition:** `open`
- **source:** `questions/0009`, 2026-08-20, while assessing what a terminal surface would need
- **missing:** no surface specifies streaming or cancellation of a read. But three requirements are
  adjacent to it: `IF-6` bounds output and reports truncation as a field (a partial answer by another
  name); `PERF-5` requires a traversal to return `undetermined` on budget exhaustion (so the traversal is
  already cancellable internally); and `US-G-3`/`US-G-4` describe an agent branching on partial and
  inconclusive results.
- **consequence:** if the requirement is latent and never made explicit, it gets implemented per surface —
  which is `IF-1`'s divergence failure. And retrofitting streaming through a request/response contract has
  the same character as retrofitting async.
- **verification:** the inference rests on the premise that `IF-6`'s truncation and `PERF-5`'s budget
  exhaustion are the same mechanism as incremental delivery. Confirm by drafting the internal contract's
  read signature and seeing whether one shape serves all three.
- **relates:** owned by **B5**. Interacts with `questions/0009`, whose recommendation turns on this.

### GAP-018 — Edges are conditional on a build configuration, and no requirement can express that
- **kind:** capability · **confidence:** `known` · **disposition:** `open`
- **source:** `analysis/0007-target-corpus-implications.md`, 2026-08-20, derived from the target-corpus answer
- **missing:** the target corpus uses conditional compilation, and `CON-7` **mandates** per-backend feature
  flags — at the store seam `EXT-1`–`EXT-6` describe. So an edge may exist only under some feature sets.
  `FR-024` states its edge set and depth bound and has **no way to state a build configuration**.
- **consequence:** a blast radius computed under one feature set is wrong under another. A symbol reachable
  only when a feature is enabled is either included — overstating reach for a deployment that disables it —
  or excluded, understating it for one that enables it. **Both are wrong answers presented as answers**,
  which is exactly what `COR-1`'s three-state contract exists to prevent, one level lower.
- **verification:** the gap is derived, and every step is checkable in this corpus: `CON-7` mandates
  feature flags; feature flags make edges conditional; `FR-024`'s response schema has no field for a
  feature set. No measurement needed.
- **relates:** owned by **B3** — it is a data-model question before a query one, so it must be settled
  **before any schema**. `FR-024` carries a dated open note. Interacts with `FR-026`–`FR-028`, since diff
  impact inherits the same defect.

### GAP-019 — The scale target is uncalibrated against the primary corpus
- **kind:** verification · **confidence:** `inferred` · **disposition:** `open`
- **source:** `analysis/0007`, 2026-08-20
- **missing:** `SCALE-1` targets one million nodes per repository, derived from what a large polyglot
  monorepo reaches. The primary corpus is a Rust crate workspace, which is very unlikely to reach it. So
  the budgets in `specs/03` are validated against a generated corpus and may be met trivially on the
  corpus that actually matters.
- **consequence:** two opposite risks. Budgets that look comfortably met because the real corpus is small;
  and correctness work calibrated on a corpus too small to expose the problems `SCALE-1` was written for.
- **verification:** the inference rests on the premise that a crate workspace is well under a million
  nodes. **Nobody has counted.** A crude symbol count over the target workspace would settle the order of
  magnitude today, without the platform existing.
- **relates:** `SCALE-1` carries a dated amendment. Resolution is two corpora, not a changed target.

### GAP-020 — Crate names taken from the module-seam sketch would reproduce reference tool names
- **kind:** knowledge · **confidence:** `known` · **disposition:** `open`
- **source:** re-check of the sketch against the reference's public documentation, 2026-08-20
- **missing:** an instruction to the architect not to name crates after the sketch's nodes. The sketch is
  a **transcription of the reference's public command surface** — five of its node descriptions match the
  public documentation verbatim (`analysis/0002`) — and the clean-room protocol's MUST NOT list explicitly
  covers **tool names**. So the sketch is safe to reason from and **unsafe to name from**.
- **consequence:** a crate layout named after the sketch would carry reference tool names into a published
  AGPL artefact, which is the one class of laundering failure that is externally visible. `CON-8` keeps this
  corpus clean of crate names; nothing currently protects the architect's deliverable, which is where the
  names will actually be chosen.
- **verification:** verified — the description match was checked against both documents.
- **relates:** owned by **B1**/**B6** (whoever fixes the layout). `CON-1` carries a clause; `CON-9`'s
  placeholder discipline is the adjacent rule. **The laundering denylist in `scripts/audit-corpus.py` will
  not catch this**, because it audits this corpus and not the future workspace.

## Triage and verification pass — 2026-08-20

The A-track requirements work is the first substantial pass over the register, so both the **triage**
rhythm (classify new entries) and the **verification pass** rhythm (every `presumed` and `hypothetical`
entry gets verified or stamped) are recorded here rather than deferred.

**Twelve new entries filed** (`GAP-009`–`GAP-020`), all triaged on filing. Register size: 8 → 20.
`GAP-018` and `GAP-019` arrived in a second pass from the requester's answer on the target corpus;
`GAP-020` from re-checking the module-seam sketch against the reference's public documentation.

### Verification pass over the seeded eight

| Gap | Confidence before | After | What this session established |
|---|---|---|---|
| **GAP-001** TUI | `discovered` | `discovered`, unchanged | Now owned by `questions/0009` and recorded in the SPEC as an **explicit absence** (`IF-14`), so it can no longer be silently dropped. `GAP-017` surfaced from assessing it, and is arguably the more important half. |
| **GAP-002** relational store has no home | `known` | `known`, unchanged | The **requirement** now exists (`EXT-3`) and is where all authoritative data lives. What remains unplaced is the *design* home, which is `B1`/`B3`. The gap is narrower than filed but not closed. |
| **GAP-003** change→symbol mapping may need a structural diff | `inferred` | `inferred`, **stamped unverified (1)** | Sharpened rather than resolved: `FR-028` makes patch-without-checkout a v1 MUST, so this inference now gates a MUST rather than a nicety. Its verification — a worked example on a moved function — is still not done. |
| **GAP-004** several NFRs are unverifiable | `known` | `known`, unchanged | `specs/03` now names the measuring signal per budget, and `OPS-1` states that these requirements are unverifiable without telemetry. So the gap is fully specified and entirely unclosed. **D1 remains the blocker for calling the non-functional requirements done.** |
| **GAP-005** declarative config not analysable | `known` | `known`, **partially challenged** | `analysis/0003` found a **claimed** permissive precedent for infrastructure indexing. The claim is unverified (`GAP-012`), so this stays `known` — but the original wording *"no surveyed prior art covers these well"* should be read as *no prior art was verified to*. `FR-005` now exists as a SHOULD. |
| **GAP-006** the write side is barely explored | `hypothetical` | `hypothetical`, **stamped unverified (1)** | Partially superseded: `FR-050` specifies coordinated rename, so one write capability is now real. The speculative remainder — codemods, mechanical migrations — is untouched and still must not be scheduled. **A4 should develop or kill it.** |
| **GAP-007** derived identities may need stability | `inferred` | `inferred`, unchanged — **and now has a named cheap check** | `questions/0004` states the verification explicitly: confirm whether derived identifiers are externally visible. If they are internal-only, **this is refuted and the hardest algorithmic requirement in the corpus disappears.** Highest-value verification in the register. |
| **GAP-008** no confidence model for inferred cross-repo edges | `presumed` | `presumed`, **stamped unverified (1)** | `FR-047` now requires the **representation** (evidence class per edge) while deliberately leaving the **weighting** unspecified, precisely because nobody has surveyed prior art. So the gap is correctly scoped and still unverified. |

**No entry has three unverified stamps**, so nothing is escalated this pass. Four entries now carry one
stamp: `GAP-003`, `GAP-006`, `GAP-008`, and (as of filing) `GAP-012`.

### The register's shape after this pass

| Confidence | Count | Entries |
|---|---:|---|
| `known` | 11 | 002, 004, 005, 009, 010, 011, 014, 015, 016, 018, 020 |
| `discovered` | 2 | 001, 013 |
| `inferred` | 4 | 003, 007, 017, 019 |
| `presumed` | 2 | 008, 012 |
| `hypothetical` | 1 | 006 |

All 20 are `open`. **Nothing is `scheduled`**, which is correct — there is no backlog (`questions/0002`),
and several of the highest-value entries are unverified and therefore ineligible under the binding rule.

**Two entries to act on first, both cheap and both capable of deleting work:**

- **`GAP-007`** — one check of whether derived identifiers are externally visible. Best outcome is
  refutation, which removes the hardest algorithmic requirement in the corpus.
- **`GAP-019`** — a crude symbol count over the target workspace settles the order of magnitude today,
  with no platform needed, and tells us whether `SCALE-1` is calibrated against anything real.

**And one to act on early because it is upstream of a schema:** `GAP-018`. It is `known`, it is derived
rather than speculated, and `B3` cannot write a data model without settling it.

### A note on this pass's own failure

`GAP-016` was filed asserting that a requirement had **no** verification method because no output
contract existed. The contract existed, in a public document the clean-room protocol explicitly permitted
reading. The register's opening section names this exactly — *"acting on an unverified gap… it is easy,
because a gap feels like knowledge"* — and it happened to the person writing the register, in the same
session. **The lesson is not "check harder"; it is that an asserted absence is a claim needing the same
verification as an asserted presence**, and the `confidence` axis exists to force that. `GAP-016` should
have been filed `presumed`, not `known`.

## How we will know this process failed

- A sync produces a gap that never reaches the register.
- An entry sits `open` and unclassified across two syncs.
- Work gets scheduled against a `presumed` or `hypothetical` entry.
- An `accepted` entry has no revisit trigger, or has one that has fired unnoticed.
- The register and the backlog disagree about what is scheduled.
- Somebody asks "did we ever decide about X?" and the answer requires reading old transcripts.

## Amendments

- **2026-08-20** — Created. Split the requester's six-term taxonomy into orthogonal `confidence` and
  `disposition` axes, added `kind`, and seeded eight entries covering every confidence level.
- **2026-08-20 (same day, third pass)** — **`GAP-020` filed.** Re-checking rows 034 and 035 against the
  reference's public documentation left both dispositions unchanged — the docs state an *intent*, not a
  contract — but established that the requester's module-seam sketch is a **transcription of the
  reference's public command surface**, which makes it unsafe to derive crate names from. Also recorded, in
  `analysis/0003` note 19: **this reference's public descriptions overstate its measured behaviour**, so
  they are evidence of contract and never of mechanism, and where they conflict with the grounding the
  grounding wins.
- **2026-08-20 (same day, second pass)** — **`GAP-018` and `GAP-019` filed** from the requester's answer
  on the target corpus: edges are conditional on a build configuration and no requirement can express
  that, and the scale target is uncalibrated against the primary corpus. **`GAP-016` corrected** — it had
  asserted an absence that a permitted public document refuted, which is the register's own documented
  failure mode occurring inside the register. It should have been `presumed`, not `known`; the correction
  is recorded in place rather than edited away.
- **2026-08-20 (same day, during the A-track requirements authoring)** — **Nine entries filed
  (`GAP-009`–`GAP-017`) and a triage plus verification pass run over the seeded eight.** Register 8 → 17.
  Four entries now carry one unverified stamp; none is escalated. `GAP-005`'s premise is partially
  challenged — a *claimed* permissive precedent for declarative-format analysis exists, and the claim is
  itself unverified (`GAP-012`), so the original wording should be read as "no prior art was **verified**
  to cover these well". `GAP-006` is partially superseded by `FR-050`. **`GAP-009` and `GAP-007` are one
  risk, not two**, and `GAP-007`'s verification is the cheapest high-value action in the register because
  its best outcome is refutation.
