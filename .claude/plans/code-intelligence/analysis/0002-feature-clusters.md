# Analysis 0002 — Candidate feature clusterings

- **Date:** 2026-08-20 · **Status:** input to syncs **A1** and **B1**. **Nothing here is a proposal.**
- **Vocabulary:** [`GLOSSARY.md`](../GLOSSARY.md)

## What this document is, and is not

**It is not a module decomposition.** Module shapes, crate boundaries and the workspace layout are the
architect's deliverable (`CON-8`), and pre-empting them is the identified primary failure mode for
this requirements work.

**It is the evidence for making that decision.** Four candidate clusterings are set out, each with the
cohesion reason for every group, each with what it makes easy and what it makes hard, and each with the
**specific observation that would decide for or against it**. Where the evidence is genuinely
ambiguous the document says so rather than picking.

**The one thing stated as settled** is what any clustering must satisfy — the invariants in the last
section. Those come from requirements, not from taste.

## The four cohesion signals

Every grouping below states which signal it groups on. Naming the signal is what makes a clustering
arguable rather than aesthetic.

| Signal | Question it answers | Where the evidence is |
|---|---|---|
| **Shared state** | Do these capabilities read and write the same data? | `analysis/0001` store columns |
| **Shared dependency** | Do they need the same machinery — a parser, a traversal, a ranker? | requirement bodies in `specs/02` |
| **Same consumer** | Is the same persona the caller? | `analysis/0001` consumer columns |
| **Same change rate** | Would a change to one force a change to the others? | inference, and the weakest of the four |

**Change rate is the signal with the least evidence and the most predictive value**, which is an
uncomfortable combination. Nothing has been built, so every claim about co-change here is inference
from the requirements rather than from history.

## Clustering A — by pipeline stage

Groups on **shared dependency**, secondarily on shared state. The most conventional reading.

| Group | Capabilities | Cohesion reason |
|---|---|---|
| **A1 Acquisition** | CAP-045, CAP-046 | Only group that talks to a git remote or handles a credential. No overlap with anything else. |
| **A2 Ingestion** | CAP-001–CAP-008 | All depend on the parsing machinery and the per-language extraction contract. All write the graph and read nothing else. |
| **A3 Derivation** | CAP-009, CAP-010, CAP-016, CAP-017, CAP-018 | All are whole-graph or whole-corpus computations over a completed graph. All produce derived data. |
| **A4 Index lifecycle** | CAP-011–CAP-015, CAP-019, CAP-068, CAP-073 | All concern *when* and *how much* work is done, and all read and write index metadata rather than graph content. |
| **A5 Query** | CAP-020–CAP-039 | All read-only. All depend on the graph and on ranking. |
| **A6 Write-back** | CAP-050 | Sole source-mutating capability. |
| **A7 Registries** | CAP-040–CAP-044, CAP-047 | Repository and group identity, and the contract registry. Relational, not graph-shaped. |
| **A8 Platform** | CAP-060–CAP-067, CAP-069–CAP-072, CAP-074 | Cross-cutting machinery. **This group is a residue, which is the tell.** |

**Makes easy:** reasoning about the data flow; adding a language (A2 only); making derivation
incremental (A3 only).

**Makes hard:** the read path. A5 is 20 capabilities and would be the largest group by far, containing
capabilities as different as a raw graph query and a generated wiki. And **A8 is a leftover bin** —
grouping the residue is not cohesion, it is what happens when the primary signal does not cover
everything.

**What would decide for it:** if ingestion and query turn out to share almost no types beyond the
graph model itself, then the stage boundary is a real seam and A2/A5 should not be neighbours.

**What would decide against it:** if the read path's 20 capabilities split cleanly on some other axis —
which Clustering C suggests they might — then A5 is not a group, it is a category.

## Clustering B — by read/write asymmetry

Groups on **shared state** and its access mode. Motivated by the profile: up to ~10 000 predominantly
read-only agents against a handful of writers.

| Group | Capabilities | Cohesion reason |
|---|---|---|
| **B1 The model** | the node, edge, flow, cluster and identity definitions underlying everything | Shared by both planes. Changing it changes both, which is exactly why it is its own group. |
| **B2 Write plane** | CAP-001–CAP-019, CAP-044, CAP-045, CAP-046, CAP-050, CAP-068, CAP-073 | All mutate durable state. All are low-frequency, long-running, and tolerant of latency. All need durability and cancellation. |
| **B3 Read plane** | CAP-020–CAP-043, CAP-047, CAP-071, CAP-072 | All read-only. All are high-frequency, short-lived, latency-sensitive, and horizontally scalable. |
| **B4 Access plane** | CAP-060, CAP-064–CAP-067, CAP-069 | Identity, authorisation, audit, telemetry, store access. Serves both planes and belongs to neither. |
| **B5 Composition** | CAP-070, CAP-061–CAP-063, CAP-074 | Configuration and assembly. |

**Makes easy:** independent scaling — the read plane replicates and the write plane queues. It also puts
`PERF-1`, `SCALE-4` and `COR-4` inside one group, which is the group whose concurrency properties are
actually specified. And it makes a read-only deployment a *composition* rather than a feature flag.

**Makes hard:** the capabilities that are read-shaped but write-adjacent. **CAP-036 (wiki) is a read
that produces an artefact; CAP-011 (change detection) is a read whose only consumer is a write; CAP-050
(rename) is a write whose edit set is computed by a read.** Each has to be assigned, and each
assignment is arguable.

**What would decide for it:** if the read plane can be built against a read-only store contract with no
reference to write machinery, the seam is real and load-bearing. `discussions/0002` develops this.

**What would decide against it:** if the write plane's incrementality (`FR-011`) turns out to need the
same traversal machinery as blast radius — because deciding the compute set is itself a graph walk —
then B2 and B3 share their most complex dependency and the split cuts through it rather than around it.
**This is the most important open question about Clustering B**, and it is genuinely unresolved:
`FR-011`'s compute-set expansion rule does not exist yet, and whether it is a traversal is exactly what
nobody knows.

## Clustering C — by consumer

Groups on **same consumer**. Motivated by the observation that the consumer cross-tabulation in
`analysis/0001` is strikingly lopsided.

| Group | Capabilities | Cohesion reason |
|---|---|---|
| **C1 Agent-facing** | the 22 read capabilities agents consume, plus CAP-050 | One consumer, one set of non-functional needs: bounded output, stable identifiers, machine-readable state, attribution. |
| **C2 Human-facing** | the same reads, plus CAP-036, plus the layout and caching contract | Same capabilities, materially different presentation, latency and tolerance. |
| **C3 Admin-facing** | CAP-040–CAP-046, CAP-060–CAP-068, CAP-073 | 12 writes against 7 reads — the inverse profile of every other group. Different stores, different change rate. |
| **C4 Developer-facing** | CAP-001–CAP-008, CAP-060, CAP-069 | The extension contracts: language extraction, store slots, telemetry. |

**Makes easy:** getting the agent surface right, because its needs are grouped rather than scattered.
And **C3 is the cleanest boundary any of the four clusterings produces** — admin capabilities share
almost no state with read capabilities.

**Makes hard:** C1 and C2 overlap almost entirely. Grouping by consumer duplicates the same
capabilities into two groups, which is either a projection layer (fine) or two implementations
(catastrophic, and `IF-1` forbids it). **So Clustering C is only viable if C1 and C2 are explicitly
projections of one contract, not groups of their own.**

**What would decide for it:** if agent and human needs diverge in the *contract* rather than only in
presentation — different granularity, different identifiers, different error semantics — then they are
genuinely two consumers of one core and this clustering names that.

**What would decide against it:** if the only difference is serialisation and budgeting, C1 and C2
collapse into one and the clustering reduces to "reads, admin, extensions" — which is Clustering B with
worse names.

## Clustering D — by command surface (the requester's sketch)

The requester's module-seam sketch (Appendix B of `PROMPT.md`), recorded here as a candidate on equal
terms because that is what it was offered as — explicitly labelled not pressure-tested.

Groups on **same consumer**, at the granularity of a CLI verb: every node maps to a command.

**Makes easy:** discoverability. The tree is legible to a user, the CLI surface falls out of it
directly, and each node has an obvious owner.

**Makes hard, and these are factual observations rather than objections:**

1. **Shared machinery has no home.** Graph access, parsing, ranking and storage are needed by many
   nodes and owned by none. In a command-shaped tree such machinery ends up either duplicated per
   command or in one large module that every command depends on.
2. **Read and write are not separated.** Three nodes mutate; the rest read. Given the consumer profile,
   that is arguably the primary seam and this shape does not draw it.
3. **Two nodes may be one traversal.** Blast radius and diff impact appear as separate nodes;
   `discussions/0001` and `FR-026`'s verification require them to be one mechanism with projections.
   This is exactly the split that produced two incompatible mechanisms sharing one name in the prior
   art.
4. **The dependence work spans three nodes** — produce, report, interrogate. Reasonable as a write/read
   split, but the shared dependence model has no owner. Moot for v1 (`FR-037` is `WON'T`), and it
   returns with the capability.
5. **One node is unlabelled.** Its purpose is unstated, so it cannot be assessed.
6. **The relational store has no home.** The sketch's only SQL-shaped node is marked out of scope and
   described as serving a different product, while the requirements need a relational store that swaps
   between embedded and server — and that store holds all the authoritative data (`EXT-3`). This is
   `GAP-002`.
7. **Ten required capabilities have no node at all** — ingestion and parsing, the storage abstraction,
   embedding and provider selection, ranking and fusion, the service surfaces, identity and audit,
   durable queued indexing, repository acquisition, configuration and assembly, observability. Listed
   in Appendix B of `PROMPT.md`; each is specified in `specs/**` and each needs a home.

**What would decide for it:** if the surface decomposition and the module decomposition genuinely
coincide — which happens when each command is thin and the shared machinery is small. Worth testing
rather than assuming false.

**What would decide against it:** if the shared machinery turns out to be the majority of the code,
which the ten unplaced capabilities suggest it might be.

**The distinction worth preserving from D regardless of the outcome:** it is an excellent *surface*
decomposition. Whatever the module shape, the CLI verbs it implies are a good CLI.

### What the sketch actually is — established 2026-08-20

**Clustering D is a transcription of the reference implementation's public command surface.** Five of the
sketch's node descriptions appear **verbatim** in the reference's public documentation, checked against
both:

> *"Blast radius analysis with depth grouping and confidence"* · *"Shortest directed path between two
> symbols"* · *"Pre-change impact report for an API route handler"* · *"Read-only structural checks
> against the indexed graph"* · *"Validate API response shapes against consumers' property accesses"*

Nothing improper happened — a public command surface is public, the requester supplied the sketch
explicitly labelled *"not pressure tested or reviewed"*, and knowing what the prior art exposes is
permitted and useful. But it changes what the sketch is **evidence of**, in three ways.

**1. It explains the ten unplaced capabilities, and the explanation is better than "an oversight".**
Ingestion, the storage abstraction, embedding provision, ranking, the service surfaces, identity and
audit, job execution, repository acquisition, configuration, and observability are absent from the sketch
because **a command surface structurally cannot contain them.** None of them is a verb a user types.
Appendix B's own framing — that these are *"factual gaps in coverage"* — is right, and the reason is now
known: they were never candidates for inclusion, so their absence carries no information about whether the
requester wants them.

**2. It converts one of this document's judgement calls into an evidenced one.** The concern raised above
— that blast radius and diff impact appear as two nodes when `discussions/0001` requires one mechanism with
projections — is no longer an inference about a hypothetical decomposition. **The sketch reproduces the
organisation of a system in which those two capabilities were measured to be two incompatible mechanisms
sharing one name**, chained only by prose instructions to a calling model. Adopting the sketch's shape
would reproduce that split by construction. That is the strongest single argument against Clustering D and
it did not exist before this check.

**3. It creates a naming hazard that lands on the architect, not here.** The clean-room protocol's MUST NOT
list explicitly covers **tool names**. Several of the sketch's node names correspond to the reference's
tool names, so **naming crates after the sketch's nodes would reproduce them.** The sketch is safe to
reason from and unsafe to name from. Filed as `GAP-020`.

**What does not change:** the sketch remains legitimate input, and the observation above still holds — it
is a good *surface* decomposition, and its verbs are a good CLI. It is simply a good CLI that already
exists elsewhere, which is a weaker basis for a *module* decomposition than an independently-derived one.

## Where the evidence is genuinely ambiguous

Stated plainly, because an analysis that resolves every ambiguity has invented evidence.

1. **Whether change detection is a read or part of the write plane.** Turns on whether the compute-set
   expansion rule is a graph traversal. **Unknown** — the rule does not exist. Decides between B and A.
2. **Whether the agent and human contracts differ beyond presentation.** **Unknown** — no UI and no
   agent integration exists. Decides whether C is a clustering or a projection layer.
3. **Whether the read path splits.** 20 read capabilities is too many for one group and they do not
   obviously separate. Candidate axes: by cost (cheap lookups versus bounded traversals); by store
   (graph-only versus multi-store); by whether they rank. **No evidence favours any of the three.**
4. **Where the wiki belongs.** A read that produces an artefact, consumed by the persona least like
   the others. Fits nowhere cleanly in any of the four.
5. **Whether the six store slots are one abstraction or six.** One trait with six implementations
   shares nothing but a name; six unrelated traits share no conformance machinery. **This is `B2`'s
   question and it is not answerable from requirements alone.**

## Invariants any clustering must satisfy

Not preferences — these follow from requirements, and a clustering that violates one is wrong
regardless of how good its cohesion looks.

| # | Invariant | Source |
|---|---|---|
| 1 | **Exactly one implementation of rank fusion**, reachable from every ranking consumer. So ranking cannot be duplicated into a per-group utility. | `FR-071`, `COR-5` |
| 2 | **One traversal serving blast radius, diff impact and the route pre-change report**, with the projections as projections. Their verification asserts equality. | `FR-024`, `FR-026`, `FR-035` |
| 3 | **One internal contract behind every surface.** Surfaces are projections and contain no analysis behaviour. | `IF-1` |
| 4 | **No concrete datastore type in the public API** of whatever the engine turns out to be. | `REV-1` |
| 5 | **The storage seam is crossable by configuration**, per slot, with no business-logic change. | `EXT-1`–`EXT-6`, `CAP-060` |
| 6 | **Authorisation terminates in exactly one place**, shared by all surfaces. | `IF-3`, `SEC-4` |
| 7 | **The deployment shape is a composition, not a fork**, and no analysis code branches on it. | `CON-2`, `CON-6` |
| 8 | **Authoritative and derived data are separable**, because upgrade migrates one and may rebuild the other. | `FR-073`, `REV-4` |
| 9 | **The local shape must be assemblable without the job queue, the network listener, or identity.** So those cannot be dependencies of the analysis path. | `01-personas-and-flows.md` §E1, `CON-6` |
| 10 | **A store backend must be implementable from outside the repository**, against a published contract and conformance suite. | `QA-7`, `QA-17` |

**Invariant 9 is the one most easily violated by accident**, because the natural way to build the
service shape makes identity and job management ambient, and then the local binary inherits them.

## What the AGPL split adds

`CON-4` makes the library/SDK/binary boundary partly a **licence** decision: anything linking the
engine forms an AGPL combined work, so a differently-licensed internal consumer must reach the
capability across a process boundary instead.

**Consequence for clustering:** a group that a non-AGPL consumer needs is a group that must be reachable
without linking. That is an argument for a well-defined service boundary at whatever the read plane
turns out to be — and `CON-5` attaches a source-offer obligation to that same boundary if it is ever
exposed externally. The two pull in opposite directions and the tension is `B6`'s to resolve
(`questions/0005`).

## Verification

### What is proven

- **Four clusterings are offered, none preferred.** Each states its cohesion signal, what it makes
  easy, what it makes hard, and the specific observation that would decide it.
- **Five ambiguities are named as unresolved**, with what would resolve each, rather than being settled
  by preference.
- **The ten invariants each cite a requirement.** None is a stylistic preference, and each is
  falsifiable against the SPEC.
- **The requester's sketch is assessed on equal terms** with three alternatives, and its seven factual
  coverage observations are separated from the two judgement calls about shape.

### What is NOT proven

- **The change-rate signal is inference throughout.** Nothing has been built, so no co-change history
  exists, and change rate is simultaneously the most predictive signal and the one with no evidence.
- **The capability-to-group assignments are the requirements author's reading.** Several capabilities
  could sit in two groups in the same clustering, and no assignment here has been tested against a
  design.
- **Clustering A's group A8 is a residue and is presented as one.** That is a finding about the
  clustering, not a group.
- **No clustering has been costed.** Which produces fewer dependency edges, smaller public surfaces or
  a better build graph is unknown, and those are the criteria that usually decide.
- **Invariant 5 assumes one storage seam is achievable across embedded and networked implementations.**
  That is the central bet of the storage abstraction and it is unverified — `EXT-1`'s dialect hazard is
  the specific reason to doubt it.

## Amendments

- **2026-08-20 (same day, second pass)** — Established that **Clustering D is a transcription of the
  reference implementation's public command surface**, by matching five of its node descriptions verbatim
  against the public documentation. This explains the ten unplaced capabilities (a command surface cannot
  contain them), converts the blast-radius/diff-impact objection from judgement into evidence, and creates
  a crate-naming hazard for the architect (`GAP-020`). Clustering D's standing as a *surface* decomposition
  is unchanged.
- **2026-08-20** — Created.

## Related

- `analysis/0001-capabilities.md` — the capability rows and cross-tabulations these clusterings group.
- `discussions/0002-read-write-asymmetry.md` — Clustering B's central claim, developed.
- `discussions/0001-what-impact-analysis-means.md` — invariant 2's origin.
- `SYNCS.md` — sync **B1** (seam pressure test) and **B2** (abstractions) consume this.
