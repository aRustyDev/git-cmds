# SPEC 07 — User stories and use cases

> **Aspirational.** Vocabulary as ratified in [`GLOSSARY.md`](../GLOSSARY.md).

- **Date:** 2026-08-20
- **Minimums met:** admin **6** (≥5) · developer **12** (≥10) · agent **12** (≥10) ·
  non-technical **4** (≥3). Counts are asserted by the corpus audit, not by this sentence.
- **Form:** each story carries acceptance criteria that are testable, and the requirement IDs it
  exercises. A story with no requirement behind it is a feature request, and is filed in `GAPS.md`
  rather than written here.

## Admin stories

### US-A-1 — Bring a private internal repository under analysis

**As** a platform administrator, **I want** to point the platform at a repository on our internal git
host and supply a credential, **so that** it can be indexed without anyone copying source by hand.

**Acceptance:** the repository is acquired; the credential appears in no argument list, log, error or
response; a re-run is idempotent; a collision with a differently-originating repository of the same
name is an error, not a silent update. `FR-045`, `FR-046`, `SEC-12`, `EXT-12`

### US-A-2 — Index two repositories at once without one blocking the other

**As** an administrator, **I want** to submit a second repository for indexing while the first is
running, **so that** onboarding a team does not become a queue of one.

**Acceptance:** both submissions are admitted; neither is rejected; queue depth is observable; both
complete. `FR-068`, `SCALE-5`

### US-A-3 — Know why a run cost more than expected

**As** an administrator, **I want** a run that fell back to a full rebuild to tell me which condition
caused it, **so that** I can plan capacity instead of guessing.

**Acceptance:** each escalation condition is a named, documented value; the run reports which fired;
the value is countable as a metric. `FR-019`, `OPS-3`

### US-A-4 — Swap a store backend without a code change

**As** an administrator, **I want** to move the graph store from the embedded engine to our networked
one by configuration, **so that** growth does not require a rebuild of the platform.

**Acceptance:** the swap is configuration only; the same conformance suite passes against both; query
answers are equivalent before and after. `EXT-1`, `COR-6`, `REV-2`

### US-A-5 — Restrict who can point the platform at an AI provider

**As** an administrator, **I want** to disable runtime AI-provider configuration entirely, **so that**
nobody can redirect where our source text is sent from inside the UI.

**Acceptance:** with the restriction set, a direct request to the runtime-configuration operation is
denied at the authorisation point, not merely hidden; the attempt is audited. `IF-13`, `SEC-11`,
`SEC-6`

### US-A-6 — Answer "which agent did that?"

**As** an administrator, **I want** every mutating action attributed to one principal in a durable
record, **so that** an incident involving one of thousands of agents is investigable.

**Acceptance:** every mutating operation produces exactly one audit record naming its principal,
target, outcome, time and correlation identifier; removing attribution at any hop fails the request
rather than proceeding anonymously. `SEC-3`, `SEC-6`, `OPS-5`

## Developer stories

### US-D-1 — Find code I can only describe

**As** a developer, **I want** to search in plain language and get ranked results grouped by execution
path, **so that** I can find behaviour without knowing a symbol name.

**Acceptance:** results are fused from traversal, lexical and semantic lanes and state which lanes
contributed; when a lane is unavailable the answer says so rather than silently narrowing. `FR-021`

### US-D-2 — Understand one symbol completely

**As** a developer, **I want** callers, callees, implementors, overriders, tests and flow membership
for a symbol in one view, **so that** I do not assemble it from six searches.

**Acceptance:** each reference appears in the correct category; categories are named edge classes.
`FR-022`

### US-D-3 — Know what my uncommitted change reaches

**As** a developer, **I want** diff impact on my working tree, **so that** I learn what I have
affected before I open a pull request.

**Acceptance:** the answer is one of affected, none affected or undetermined; it states the edge set,
the depth bound and whether the bound is a correctness statement or a budget. `FR-026`, `COR-1`

### US-D-4 — Not be told "nothing" when the truth is "unknown"

**As** a developer, **I want** an inconclusive analysis to say so, **so that** I do not ship a change
believing it was checked.

**Acceptance:** a walk that truncated, degraded or left the scoped sub-directory returns
`undetermined` with a reason, never `none affected`. `COR-1`, `FR-032`, `PERF-5`

### US-D-5 — See why the tool thinks two things are connected

**As** a developer, **I want** a witness path for a positive reachability answer, **so that** I can
check the tool's reasoning rather than trust it.

**Acceptance:** every positive reachability answer carries the concrete path. `FR-023`

### US-D-6 — Compare two branches, not two working trees

**As** a developer, **I want** diff impact for `base...head`, **so that** the answer is about the
branch and not about whatever I have locally.

**Acceptance:** the same two refs give the same answer regardless of the working tree's state,
including when it is dirty. `FR-027`

### US-D-7 — Rename a symbol across files without breaking strings

**As** a developer, **I want** rename to change only true references and to leave comments and string
literals alone, **so that** I do not review a diff full of collateral edits.

**Acceptance:** on a fixture where the name also appears in a comment, a string literal and another
scope, only true references change; the index reflects the rename immediately afterwards; a preview is
the default. `FR-050`

### US-D-8 — Trust that the index matches my checkout

**As** a developer, **I want** every answer to tell me what it was computed against, **so that** I can
tell a stale answer from a current one.

**Acceptance:** every analysis response carries the index generation and freshness. `FR-039`, `FR-015`

### US-D-9 — Narrow a huge graph to the part I care about

**As** a developer, **I want** to scope queries to a sub-directory and filter by node type and edge
class, **so that** results are about my area.

**Acceptance:** filtering is a query parameter, not post-processing; a traversal whose only path exits
the scope returns `undetermined` rather than `none`. `FR-029`, `FR-032`

### US-D-10 — Explore outward from something I found

**As** a developer, **I want** the nodes within N hops of a selection, with N my choice, **so that** I
can widen a view gradually.

**Acceptance:** N is caller-supplied; a request above the documented maximum is rejected with an error
naming the maximum, never silently clamped. `FR-030`

### US-D-11 — Find what depends on an API route before I change it

**As** a developer, **I want** a pre-change report for a route handler, **so that** I see its
consumers, its contract and its blast radius together.

**Acceptance:** the report's blast-radius section is identical to invoking blast radius directly on
that handler. `FR-035`, `FR-007`

### US-D-12 — Catch a consumer reading a field my response does not have

**As** a developer, **I want** response-shape conformance checked against consumers' property
accesses, **so that** a contract break is found before it ships.

**Acceptance:** a consumer accessing an absent or wrongly-shaped property is reported; findings
distinguish declared shapes from inferred ones. `FR-034`

## Agent stories

### US-G-1 — Authenticate as myself

**As** an agent, **I want** my own credential with a subject and an expiry, **so that** my actions are
distinguishable from those of the other agents in the fleet.

**Acceptance:** a request bearing principal A's credential is attributed to A; an expired credential is
rejected; no shared deployment secret grants access. `SEC-1`, `SEC-2`

### US-G-2 — Discover exactly what I may call

**As** an agent, **I want** the advertised operation inventory to be the complete callable set, **so
that** an allowlist I build from it is actually complete.

**Acceptance:** the advertised inventory equals the dispatch table, asserted as set equality; no
undeclared alias is reachable. `IF-4`

### US-G-3 — Get answers that fit my budget

**As** an agent, **I want** output bounded and truncation reported in a field, **so that** I never
mistake a partial answer for a whole one.

**Acceptance:** an over-budget answer sets a truncation field; retained content is a valid subset, not
malformed. `IF-6`

### US-G-4 — Branch correctly on an inconclusive result

**As** an agent, **I want** `undetermined` to be a distinct machine-readable state, **so that** I can
escalate to a human instead of concluding the change is safe.

**Acceptance:** the three states are distinct values in the response; no numeric score can substitute
for them. `COR-1`, `FR-024`

### US-G-5 — Analyse a pull request for a repository nobody checked out

**As** an agent, **I want** to submit a patch and receive diff impact, **so that** I can review a pull
request without a working tree.

**Acceptance:** a patch for an indexed repository with no working tree on the host returns a
diff-impact answer; the response reports the index generation it was computed against. `FR-028`

### US-G-6 — Hold an identifier between calls

**As** an agent, **I want** identifiers I receive to still mean the same thing on my next call, **so
that** a multi-step task does not silently change subject.

**Acceptance:** whichever branch `questions/0004` takes is tested — either derived identities are
stable, or the surface prevents holding them across generations. `COR-3`, `FR-018`

### US-G-7 — Name my repository explicitly

**As** an agent, **I want** to state my repository on every call rather than rely on ambient state,
**so that** a concurrent caller's switch cannot change my results.

**Acceptance:** two concurrent sessions on one replica addressing different repositories each get their
own; an omitted repository with several visible is an error. `IF-7`, `FR-041`

### US-G-8 — Not be slowed down by the rest of the fleet

**As** an agent, **I want** concurrent reads to overlap, **so that** my latency does not grow with the
number of agents working.

**Acceptance:** N concurrent reads show no monotone latency staircase and complete materially faster
than N sequential reads, with a discriminating control. `PERF-1`, `SCALE-4`

### US-G-9 — Never read a half-rebuilt graph

**As** an agent, **I want** a read during an index run either to succeed against one generation or to
fail, **so that** I never act on an internally inconsistent answer.

**Acceptance:** reads held across a full rebuild are each consistent with exactly one generation.
`COR-4`

### US-G-10 — Get the same answer whichever surface I use

**As** an agent, **I want** identical answers and rankings to the CLI and the API, **so that** results
I compare across surfaces are comparable.

**Acceptance:** a differential suite asserts identical answers, verdicts and rankings across surfaces.
`IF-1`, `COR-5`, `FR-071`

### US-G-11 — Know how strong an edge is

**As** an agent, **I want** cross-repository edges labelled observed or inferred, **so that** I can
weigh a contract-derived reach differently from an observed call.

**Acceptance:** every cross-repository answer carries an evidence class per edge, and counts report the
classes separately. `FR-047`

### US-G-12 — Rename safely and leave the index correct

**As** an agent, **I want** rename to be AST-accurate and to update the index in the same operation,
**so that** my next query does not contradict my last edit.

**Acceptance:** after a rename, the old name returns nothing and the new name returns the full
reference set; a failed index update reports failure rather than partial success. `FR-050`

## Non-technical stories

### US-N-1 — Read the codebase as a document

**As** a product or programme lead, **I want** a generated wiki of the repository, **so that** I can
understand what the system does without reading code.

**Acceptance:** the wiki is derived from the graph, navigable without graph vocabulary, and states the
index generation it was generated from. `FR-036`

**Note:** currently blocked on `questions/0011` — the wiki has no output contract, so this story is
not yet implementable and is recorded as such rather than given a plausible test.

### US-N-2 — See which areas of the system a change touches

**As** an engineering manager, **I want** the affected areas of a change named in ordinary language,
**so that** I know which teams to involve.

**Acceptance:** cluster and flow projections are presented without requiring a query; an inconclusive
result is shown as inconclusive rather than as "no areas affected". `FR-024`, `FR-010`, `COR-1`

### US-N-3 — See the shape of the system

**As** a non-technical stakeholder, **I want** a picture of the codebase's areas and their
relationships, **so that** I have a mental model to hang conversations on.

**Acceptance:** the web UI offers force-directed, sequential and radial layouts over a locally cached
graph object, and a bounded path exists for graphs too large to send whole. `IF-11`

### US-N-4 — Get a number I can put in a report

**As** a programme lead, **I want** node and edge counts by type over time, **so that** I can describe
growth without an engineer generating it.

**Acceptance:** counts name the index generation they were taken at, so two are comparable. `FR-031`

## Use cases

Stepped scenarios where the interaction is more than one call. Each names its actor, precondition,
steps, and — where the interesting behaviour is a failure — the alternative path.

### UC-1 — Onboard a repository into the service shape

**Actor:** administrator. **Precondition:** the platform is deployed and identity is configured.

1. Administrator supplies a repository location and, if private, a credential.
2. Platform validates the location against the operator-configured allowlist. *Alternative: not
   allowlisted → refused, with the reason. The administrator adds it to the allowlist; a caller-supplied
   override does not exist.*
3. Platform acquires the repository. *Alternative: the local path already holds a differently-originating
   repository → error, not an update.*
4. Administrator submits it for indexing; a job is created and returned with an identity.
5. Administrator observes progress. *Alternative: cancels → the index is left at the prior generation or
   at a complete new one, never in between.*
6. Job completes. Index status reports the new generation as fresh.
7. **Restart the platform.** The job record is still present.

**Exercises:** `FR-045`, `FR-046`, `FR-068`, `FR-014`, `FR-015`, `EXT-12`, `SEC-10`

### UC-2 — A developer decides whether to ship a change

**Actor:** developer. **Precondition:** a fresh index and uncommitted local work.

1. Developer requests diff impact on the working tree.
2. Platform maps the change set to symbols, then walks blast radius upstream under the default edge set
   and depth bound.
3. Platform returns `affected` with projections: symbols, files, flows, routes, tests, downstream
   repositories.
4. Developer asks for a witness path for one surprising reach.
5. Developer widens the depth bound and repeats. *Alternative: the widened walk exceeds the traversal
   budget → `undetermined` with truncation reported, and no projection reports a clean count.*

**Exercises:** `FR-026`, `FR-024`, `FR-023`, `COR-1`, `PERF-5`

### UC-3 — An agent reviews a pull request it cannot check out

**Actor:** agent. **Precondition:** the repository is indexed; no working tree exists on the host.

1. Agent authenticates with its own credential.
2. Agent retrieves the advertised inventory and selects the diff-impact operation.
3. Agent submits a patch, naming the repository explicitly.
4. Platform maps patch context onto indexed symbols and computes diff impact.
5. Platform returns the three-state result, the index generation, and a truncation field if bounded.
6. Agent branches: `affected` → report; `none affected` → approve; `undetermined` → escalate to a human.

**Alternative at step 4:** the patch's context cannot be mapped confidently — for instance the change is
a large move — and the result is `undetermined` with the reason. **This is the expected path for a
refactor, not an edge case**, and `GAP-003` records why.

**Exercises:** `FR-028`, `SEC-1`, `IF-4`, `IF-6`, `IF-7`, `COR-1`, `FR-039`

### UC-4 — A rename that fails halfway

**Actor:** developer. **Precondition:** a fresh index.

1. Developer requests a rename preview. Preview is the default.
2. Platform determines the edit set from the graph, AST-accurately.
3. Developer confirms.
4. Platform applies the edits and updates the index **as one operation**.
5. **Fault:** the index update fails.
6. Platform reports failure, naming what was written and what was not. The operation does not report
   success.

**Exercises:** `FR-050` clauses 3 and 5

**Why this use case exists:** the measured prior-art failure was not that rename was hard — it was that
it reported success while leaving the index stale and swallowing an intermediate failure. The failure
path is the requirement.

### UC-5 — Cross-repository reach through a declared contract

**Actor:** developer or agent. **Precondition:** two repositories in one group; the group's contract
registry is built.

1. Actor requests blast radius for a symbol in the provider repository.
2. Platform walks upstream, crossing into the consumer repository via a contract-inferred edge.
3. Result reports affected elements in both repositories, **each edge labelled observed or inferred**.
4. Counts report the two evidence classes separately.

**Alternative at step 2:** the group's contract registry is stale relative to either member's index →
the response reports the staleness rather than answering as though fresh.

**Exercises:** `FR-044`, `FR-047`, `FR-042`, `FR-039`

**Deliberately unspecified:** how the two evidence classes are *weighed*. `GAP-008` records that no
prior art has been surveyed for a usable confidence model, so the representation is required and the
weighting is not.

### UC-6 — A store becomes unavailable mid-service

**Actor:** any reader. **Precondition:** the service shape with networked stores.

1. Reader issues a hybrid search.
2. The vector store is unreachable.
3. Platform answers from the remaining lanes **and reports that the semantic lane was absent**.
4. Reader issues a graph query.
5. The graph store is unreachable.
6. Platform fails the request. It does not answer from a cache and present it as current.

**Exercises:** `FR-021`, `OPS-7`, `EXT-2`

**The distinction this use case is for:** an optional lane degrades and says so; a required store fails
loudly. Neither returns a plausible answer computed from what remained.

## Verification

### What is proven

- **The story minimums are exceeded** — 6 admin, 12 developer, 12 agent, 4 non-technical — and the
  counts are asserted by an executable per-prefix count in the corpus audit, not by this claim.
- **Every story names the requirements it exercises**, so the set of stories is a traceability input
  rather than prose.
- **Every requirement referenced here exists** in `02`–`06`. Checked by extracting the referenced IDs
  and diffing against the declared set.
- **Three use cases specify the failure path as the requirement** — UC-4 step 5, UC-3's alternative at
  step 4, UC-6's two halves. Each corresponds to a measured prior-art failure where the happy path
  worked and the failure path lied.

### What is NOT proven

- **`US-N-1` is not implementable.** The wiki has no output contract (`questions/0011`), and the story
  is recorded with that stated rather than given a test it cannot have.
- **The non-technical stories are the least grounded.** No non-technical stakeholder has been consulted;
  all four are inferred from the capability list's web-UI and wiki items.
- **`US-G-6` is conditional on an undecided question.** Its acceptance criterion is "whichever branch is
  chosen is tested", which is honest but is not yet a test.
- **No story covers a compromised or misbehaving agent**, and with 10,000 agent principals that is the
  likeliest incident. `05-security-requirements.md` records the same gap.
- **UC-2's "default edge set" does not exist yet** (sync **A5**), so the use case is currently
  unrunnable at step 2.
- **No story has been reviewed by any of its actors.** Sync **A1** and **A3**.

## Amendments

- **2026-08-20** — Created.

## Related

- [`01-personas-and-flows.md`](01-personas-and-flows.md) — the personas these stories belong to, and the five flows they instantiate.
- [`02-functional-requirements.md`](02-functional-requirements.md) — the requirements each story exercises.
- [`../FEATURES.md`](../FEATURES.md) — two-way traceability.
