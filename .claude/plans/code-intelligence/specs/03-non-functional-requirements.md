# SPEC 03 — Non-functional requirements

> **Aspirational.** Status markers record justification strength, not implementation status.
> Vocabulary as ratified in [`GLOSSARY.md`](../GLOSSARY.md).

- **Date:** 2026-08-20
- **Structure** follows the house non-functional vocabulary: performance budgets · scale targets ·
  correctness · security and privacy · operability · reversibility. Security has its own file
  ([`05`](05-security-requirements.md)) because it is large enough to stand alone.
- **Every budget below is ours.** No constant is carried from prior art; each is derived from a stated
  premise, and the derivation is written down so it can be argued with.

## Performance budgets

Budgets are stated **per deployment shape**, because the shapes differ in whether a store access costs
a function call or a network round trip (`01-personas-and-flows.md` §D7). One shared number would
either be unachievable locally or trivially met in the service.

### The premises the budgets derive from

| Premise | Source | Consequence |
|---|---|---|
| Web-UI query time n95 under 1 s | **requester-supplied** | The ceiling everything interactive fits inside |
| ~20–50 humans, up to ~10 000 agents, predominantly read-only | **requester-supplied** | Concurrency is an agent-fleet property, not a human one |
| A UI interaction composes several reads plus render | inference | A single read must be well inside the 1 s ceiling |
| Agents are mostly idle between calls | inference | Steady-state in-flight concurrency is a small fraction of fleet size |

### PERF-1 — Concurrent reads MUST scale with the number of readers, per replica. *(VERIFIED)* — **inherited-negative**

**MUST.** On a single replica, N concurrent independent reads MUST complete in wall-clock materially
better than N times a single read. Reads MUST NOT serialise behind a process-wide lock, a single
shared store handle, or any other global chokepoint.

**Why this is evidenced:** the reference implementation funnelled every API read through one
process-wide mutex against a single open database handle. Twelve concurrent requests produced a
**monotone arithmetic latency staircase** — each request roughly a fixed increment slower than the
last — which is the signature of a FIFO queue rather than concurrency. The nominal speedup over a
serial loop was an artefact of client spawn cost, not parallelism.

**Verification — and this is the specific test, because the failure was specific:**

1. Issue N concurrent independent reads against one replica; record per-request latency.
2. **Assert the absence of a monotone latency staircase.** Sort completions by finish time; the
   per-request latency series MUST NOT be monotonically increasing with a near-constant increment.
3. Assert aggregate wall-clock is materially below N × single-read latency.
4. **Run a discriminating control:** the same N reads issued serially. If the concurrent and serial
   aggregates are indistinguishable, the concurrent run did not actually overlap and **the
   measurement is void, not passing.**

Requires telemetry (`OPS-2`); currently unverifiable (`GAP-004`).

**Applies to:** the service shape. In the local shape a single user makes it unobservable, but the
property must not be *designed away*, because it cannot be added back later.

### PERF-2 — A bounded interactive read MUST complete within n95 250 ms in the service shape. *(assumed)*

**MUST.** A bounded read is a symbol view, a hybrid search, a filtered graph query, an N-hop
neighbourhood at small N, or a count — at the `SCALE-1` target.

**Derivation, not a carried constant:** the requester's ceiling is 1 s n95 for a web-UI query. A UI
interaction typically composes two to three reads plus transport and render. 250 ms leaves room for
three sequential reads inside the ceiling with margin for the render. If the UI turns out to compose
more reads than that, this number is wrong and should be revised — not the ceiling.

**Verification:** a fixed query set at `SCALE-1`, n95 reported by telemetry, in a deployment with
networked stores. Interactive and batch budgets are tracked **separately**; conflating them misleads.

### PERF-3 — A bounded interactive read MUST complete within n95 100 ms in the local shape. *(assumed)*

**MUST.** Same query set, embedded stores, no network hop.

**Derivation:** the local shape removes three network round trips per composite read. A tighter budget
is therefore not generosity — it is the same work with the transport removed, and holding it prevents
in-process inefficiency hiding behind a budget sized for the network.

**Verification:** as `PERF-2`, against the embedded backends.

### PERF-4 — The web-UI contract MUST satisfy n95 under 1 s for the UI's declared query set. *(assumed)*

**MUST.** Measured **at the contract boundary the UI consumes**, so the budget is an obligation on the
crates beneath it rather than on the frontend. The UI declares its query set; the platform meets the
budget for that set.

**Verification:** the declared query set is a committed artefact, and the budget is asserted against it
in a regression gate (`QA-8`). A query the UI issues that is not in the declared set is a defect in the
declaration, not an exemption from the budget.

### PERF-5 — A bounded blast-radius traversal MUST complete within n95 2 s, budgeted separately from interactive reads. *(assumed)*

**MUST.** Explicitly a different budget class. A depth-bounded upstream traversal over a large graph is
an expensive operation reachable by any caller, and hiding it inside the interactive number would
either make the interactive number unachievable or make this one invisible.

**Derivation:** it is not a keystroke-latency operation — a developer waits for a change-safety verdict
in a way they will not wait for a symbol lookup. 2 s is chosen as the longest wait that still reads as
"the tool is answering" rather than "the tool has stalled".

**MUST also:** exceeding the budget MUST produce `undetermined` with truncation reported, never a
partial result presented as complete. A budget overrun is a truncation, and truncation is not an answer.

**Verification:** a traversal fixture at `SCALE-1` with a known-large radius; assert both the budget and
that the overrun path returns `undetermined`.

### PERF-6 — An incremental index update MUST perform work proportional to the change, not to the repository. *(VERIFIED)* — **inherited-negative**

**MUST.** See `FR-011` and `FR-012` for the functional statement. The performance statement: for a
one-file change at `SCALE-1`, the counts of files parsed, nodes re-extracted and derivation passes run
MUST each be materially below the full-run figure.

**Verification:** counted by telemetry (`OPS-3`), **not** by wall-clock. Wall-clock can be flattered by
a cache while the compute remains unconditional — which is exactly the failure this requirement exists
to prevent.

### PERF-7 — A full index build MUST have a published baseline, and a regression against it MUST fail the release. *(operational)*

**MUST.** No absolute wall-clock target is set here, because none can be justified before anything is
built and an invented number would be worse than none. What is required is that a baseline exists, is
published, and is a gate.

**Verification:** a benchmark harness produces a baseline for a fixed corpus; the release gate
(`QA-10`) fails on a regression beyond a documented threshold. A baseline file containing only
placeholders does not satisfy this requirement.

**The consequence we dislike:** this permits v1 to ship with a slow full build, provided it is a
*measured* slow build. That is deliberate: a measured bad number is actionable and an unmeasured good
feeling is not.

## Scale targets

### SCALE-1 — The system MUST meet its budgets at one million nodes and three million edges per repository. *(assumed)*

**MUST.** The v1 target. Stretch: ten million nodes and thirty million edges.

**Derivation:** a large monorepo reaches single-digit millions of addressable symbols, and observed
code graphs carry a few edges per node. One million is chosen as a target that a substantial real
repository actually hits, rather than a round number nothing reaches.

| Dimension | v1 target | Stretch |
|---|---:|---:|
| Nodes per repository | 1,000,000 | 10,000,000 |
| Edges per repository | 3,000,000 | 30,000,000 |
| Files per repository | 50,000 | 250,000 |
| Repositories per deployment | 500 | 5,000 |
| Repository groups | 50 | 500 |
| Repositories per group | 25 | 100 |

**Verification:** a generated corpus at each target; budgets asserted at v1 targets and reported
(not asserted) at stretch.

### SCALE-2 — The service shape MUST serve 50 human principals and 10,000 agent principals. *(assumed)*

**MUST.** Requester-supplied population. Agents are predominantly read-only.

**MUST:** concurrency is stated **per replica** at `PERF-1`, so meeting this target is a horizontal
scaling decision rather than a correctness one. A design in which the population target can only be
met by a single large replica fails this requirement.

**Verification:** a load profile at the stated population against a multi-replica deployment, with
per-replica concurrency at `SCALE-4`.

### SCALE-3 — The number of simultaneously-served repositories MUST be bounded by capacity, not by a constant. *(VERIFIED)* — **inherited-negative**

**MUST.** There MUST be no fixed low ceiling on resident repositories. Where a residency limit exists
for resource reasons it MUST be derived from available resources, MUST be observable, and its
eviction cost MUST NOT be a full store reopen.

**Why this is evidenced:** the reference implementation capped resident repositories at a small
integer with LRU eviction where eviction cost a full database reopen — converting steady-state
multi-repository serving into open-and-close thrash the moment the working set exceeded the cap.

**Verification:** register substantially more repositories than any internal residency figure and
round-robin reads across all of them. Assert no latency cliff attributable to eviction, and assert the
eviction rate is reported by telemetry. A cliff that appears at a suspiciously round number is the
failure this requirement names.

### SCALE-4 — One replica MUST sustain 64 concurrent in-flight reads within the `PERF-2` budget. *(assumed)*

**MUST.**

**Derivation:** 10,000 agents, predominantly idle between calls. Assuming roughly half a percent are
in-flight at any moment gives ~50 concurrent reads across the deployment. 64 is the next power of two
above that, chosen so that a single replica covers the implied steady state and horizontal scaling
covers bursts. **If the in-flight fraction is higher than assumed, this number is wrong** — and it is
the assumption most worth measuring early, because it sizes everything.

**Verification:** 64 concurrent readers against one replica, `PERF-2` budget held, with the `PERF-1`
staircase control.

### SCALE-5 — Indexing MUST accept concurrent submissions for distinct repositories. *(VERIFIED)* — **inherited-negative**

**MUST.** See `FR-068`. The scale statement: the queue depth MUST be bounded by configuration rather
than by one, and the bound MUST be reportable.

**Verification:** submit more repositories than the configured concurrency; all are admitted, none
rejected, and queue depth is observable throughout.

## Correctness

### COR-1 — Every graph-walking answer MUST use the three-state result contract. *(assumed)*

**MUST.** `affected` · `none affected` · `undetermined`. `none affected` MUST be claimable **only**
where the walk was complete under the stated edge set and depth. The three states MUST be
machine-readable and MUST NOT be collapsible into a numeric score.

**Verification:** a property test over generated graphs and queries asserting that no truncated,
degraded or scope-exiting walk ever returns `none affected`. This is the single most important
correctness property in the system and it is stated as a property, not as a per-capability test.

### COR-2 — An incremental update MUST produce an index identical to a full rebuild. *(assumed)*

**MUST.** Equality against a full rebuild of the same source is the only honest test of an incremental
path.

**Verification:** for a corpus of change sequences — additions, deletions, modifications, renames,
moves — assert the incrementally-maintained index equals a from-empty rebuild. Property-based, with
the change sequence generated.

### COR-3 — Derived structure identities MUST behave as `questions/0004` decides, and the decision MUST be tested. *(assumed)*

**MUST.** Either identities are stable across runs — in which case stability is a property test — or
they are not, in which case **no consumer may hold one across generations** and that constraint is
itself tested at the surface.

**Verification:** whichever branch is chosen, a test asserts it. The unacceptable outcome is neither:
identities that happen to be stable, relied upon informally, and churning at a bad moment.

### COR-4 — A reader MUST NOT observe a torn read. *(assumed)*

**MUST.** A reader sees one **index generation**, consistently. It may see an old one; it may be told
the index is being rebuilt; it MUST NOT see a mixture.

**Verification:** hold a read while a full rebuild runs to completion, repeatedly, asserting every
answer is internally consistent with exactly one generation. A reader that does not *block* may still
observe a torn graph, so "reads are not blocked" does not satisfy this.

### COR-5 — Ranked results MUST be identical across every surface. *(VERIFIED)* — **inherited-negative**

**MUST.** See `FR-071`. The correctness statement: a differential test asserts the same query returns
the same ranking through the CLI, the API and the agent surface.

**Verification:** differential test across surfaces, as a release gate (`QA-11`).

### COR-6 — Every store backend MUST pass one conformance suite per slot. *(assumed)*

**MUST.** The suite defines the slot. A backend failing one case is not usable; the case is not
optional.

**Verification:** the suite is externally runnable (`QA-7`) and is run against every backend in CI.
Cross-backend differential testing MUST also run where two backends exist for a slot — and note that
agreement is not proof the harness works, so the harness needs its own discriminating control.

### COR-7 — Parsing and analysis MUST be resilient to hostile and malformed input. *(operational)*

**MUST.** Source is untrusted input. A malformed, adversarial or pathologically large file MUST NOT
crash a run, exhaust memory unboundedly, or abort indexing of unrelated files.

**Verification:** fuzzing over the parse and extract path, plus fixtures for deeply-nested, extremely
long-line and cyclic-import cases.

## Operability

### OPS-1 — The system MUST emit telemetry sufficient to verify every budget in this file. *(VERIFIED)*

**MUST.** Traces, metrics and logs. This is not general observability hygiene: `PERF-1`, `PERF-2`,
`PERF-6`, `SCALE-3`, `SCALE-4` and index staleness are **unverifiable without it**, and an unverifiable
requirement is a wish.

**Why this is evidenced:** recorded as `GAP-004` — a requirements-coverage review established that
these requirements currently have no means of measurement at all.

**Verification:** each budget in this file names the signal that measures it, and every named signal
exists. Checkable as a cross-reference.

**Applies to:** required in the service shape; optional and off by default in the local shape, where
there is no operator to consume it.

### OPS-2 — Concurrency behaviour MUST be observable per replica. *(operational)*

**MUST.** In-flight read count, queue depth if any, and per-request latency, attributable to a replica.

**Verification:** the `PERF-1` staircase test is expressible entirely from emitted signals, without
external instrumentation.

### OPS-3 — Indexing MUST report what it skipped, not only what it did. *(VERIFIED)* — **inherited-negative**

**MUST.** Files parsed versus files in scope; nodes re-extracted versus total; derivation passes run
versus available; and **every escalation condition that fired** (`FR-019`).

**Why this is evidenced:** in the reference implementation ten conditions silently escalated an
incremental run to a full rebuild. Without skip-reporting, incrementality that does not work is
indistinguishable from incrementality that does.

**Verification:** `PERF-6` is asserted from these counters alone.

### OPS-4 — Index staleness MUST be observable per repository, without a request. *(operational)*

**MUST.** An operator MUST be able to see which indexes are stale and how stale, as a metric, rather
than by asking each one.

**Verification:** a stale index appears in the staleness metric within one detection interval, and
the interval is configurable and documented.

### OPS-5 — A caller MUST be able to correlate its own request with the system's record of it. *(operational)*

**MUST.** Every response carries a correlation identifier that appears in logs, traces and audit
records. With up to 10,000 agents, "which request was that?" is otherwise unanswerable.

**Verification:** a request's identifier is present in its response and locatable in each signal.

### OPS-6 — Metric cardinality MUST be bounded by design. *(operational)*

**MUST.** No metric may be labelled by principal, by symbol, by file path or by query text. 10,000
principals across 500 repositories makes an unbounded label a self-inflicted outage.

**Verification:** an executable check over metric definitions rejecting unbounded label sources. A
convention documented but unenforced does not satisfy this.

### OPS-7 — A store failure MUST degrade explicitly, never silently. *(operational)*

**MUST.** When an optional store is unavailable, the affected capability MUST report the absence
(`FR-021`). When a required store is unavailable, the request MUST fail. Neither may return a
plausible answer computed from what remained.

**Verification:** fault-injection per slot; assert the reported degradation matches the injected fault.

## Reversibility

### REV-1 — No concrete datastore type MUST appear in `<ENGINE>`'s public API. *(assumed)*

**MUST.** House precedent, cited as precedent and adopted here because the store slots make it
load-bearing rather than stylistic: a datastore type in the public API makes the backend a
compile-time commitment for every consumer.

**Verification:** an executable check over the public API surface. Not a review item.

### REV-2 — Each of the graph, vector and relational slots MUST have at least two implementations before v1. *(assumed)*

**MUST.** One embedded, one networked. Two implementations is what proves a seam is real; one makes it
a wrapper.

**Verification:** counted, and both pass `COR-6`.

### REV-3 — An index MUST be exportable to a portable format. *(operational)*

**MUST.** Data must never be trapped in a backend. Export MUST include the authoritative data
identified in `01-personas-and-flows.md` §D4 — the repository and group registries, job state and
audit records — because those cannot be reconstructed by reindexing.

**Verification:** export, then import into a different backend for the same slot, then assert query
equivalence.

### REV-4 — Derived data MUST be reconstructible from authoritative data and source. *(assumed)*

**MUST.** Every derived store may be dropped and rebuilt. Nothing derived may be the only copy of
anything.

**Verification:** drop each derived store in turn, rebuild, and assert query equivalence with the
pre-drop state — modulo derived identities, whose behaviour `COR-3` governs.

### REV-5 — The deployment shape MUST be a composition decision, not a code fork. *(assumed)*

**MUST.** See `CON-2` and `CON-6`. The reversibility statement: it MUST be possible to add a third
shape without modifying analysis behaviour.

**Verification:** both shapes pass one behavioural conformance suite (`QA-9`).

## Quality assurance

Testing levels, per-backend conformance and release gates are specified in
[`08-testing-and-documentation.md`](08-testing-and-documentation.md). Two properties belong here
because they are non-functional requirements rather than test policy:

### QA-0 — Every constraint in this SPEC that can be executable MUST be executable. *(operational)*

**MUST.** A comment saying "do not do this" does not satisfy a constraint. `FR-071` (one fusion path),
`REV-1` (no datastore type in the public API), `OPS-6` (metric cardinality) and the clean-room
laundering check are all stated as executable checks for this reason.

**Verification:** each such requirement names its check, and the check runs in CI.

## Verification

### What is proven

- **Every budget derives from a stated premise**, and the premises are separated into
  requester-supplied and inferred. No number is inherited from prior art.
- **`PERF-1` carries a discriminating control**, and states that an indistinguishable concurrent and
  serial aggregate voids the measurement rather than passing it. The estate has measured that a
  control which cannot fail makes a positive result meaningless.
- **All inherited negatives in this file are tagged and evidenced:** `PERF-1`, `PERF-6`, `SCALE-3`,
  `SCALE-5`, `COR-5`, `OPS-3`.
- **Interactive and batch budgets are separated**, as are the two deployment shapes, so no single
  number has to be true of both.

### What is NOT proven

- **Nothing in this file is currently measurable.** There is no telemetry and nothing to instrument
  (`GAP-004`). Every budget here is a target with a named measurement method and no measurement.
- **`SCALE-4`'s in-flight fraction is an assumption that sizes everything.** Half a percent of 10,000
  agents is a guess. It is the single most valuable early measurement, and if it is wrong by an order
  of magnitude, the concurrency target and the replica count both change.
- **`PERF-2`'s derivation assumes the UI composes two to three reads per interaction.** Nobody has
  designed the UI, so this is inference from how UIs usually work.
- **`SCALE-1` is not calibrated against a real target repository.** No repository in this estate has
  been measured for node and edge counts, because nothing exists to measure it with.
- **`PERF-7` deliberately sets no absolute number**, so v1 could ship with a full build slow enough to
  be operationally painful while satisfying this file.
- **`COR-2` and `COR-6` describe suites that do not exist.** They are the two most load-bearing test
  artefacts in the corpus and neither has been written.

## Amendments

- **2026-08-20** — Created.

## Related

- [`02-functional-requirements.md`](02-functional-requirements.md) — the functional statements these budgets qualify.
- [`08-testing-and-documentation.md`](08-testing-and-documentation.md) — the suites and gates named here.
- `analysis/0005-deployment-shape-contrast.md` — per-requirement applicability across shapes.
- `GAPS.md` `GAP-004` — why nothing here is currently verifiable.
