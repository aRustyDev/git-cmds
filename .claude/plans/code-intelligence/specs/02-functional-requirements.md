# SPEC 02 — Functional requirements

> **Aspirational.** Status markers record the strength of a requirement's justification, not
> implementation status — see [`00-overview.md`](00-overview.md), *How to read a requirement*.
> Vocabulary as ratified in [`GLOSSARY.md`](../GLOSSARY.md).

- **Date:** 2026-08-20
- **Traceability:** `FR-0nn` carries capability `CAP-0nn` from `analysis/0001-capabilities.md`.
- **Component naming:** requirements say **the system**, **the ingestion stage**, **the serving
  stage**, `git-ctx` or `<ENGINE>`. They never name a crate or a module, deliberately.

## A. Ingestion and index construction

### FR-001 — The ingestion stage MUST determine which files are in scope, and their language, before parsing. *(assumed)*

**MUST.** Scope is derived from the repository contents plus caller-supplied include and exclude
rules. A file whose language has no extraction support MUST be recorded as *out of extraction scope*
rather than silently ignored, so that coverage is reportable.

**Verification:** for a fixture repository containing supported, unsupported and excluded files, the
reported in-scope set, out-of-extraction-scope set and excluded set partition the repository exactly.

### FR-002 — The ingestion stage MUST parse a supported language's source into a syntax tree. *(assumed)*

**MUST.** Parsing MUST be resilient: a file that fails to parse MUST be recorded as a parse failure
with its reason, and MUST NOT abort the run.

**Verification:** a fixture containing deliberately malformed files completes indexing, and each
malformed file appears in the run's parse-failure report.

### FR-003 — The ingestion stage MUST extract nodes and edges to a declared extraction depth per language. *(assumed)*

**MUST.** *"Supports language X"* is not a specifiable claim — it conflates detection, parsing and
extraction. Each language MUST therefore declare which node kinds and which **edge classes** it
extracts, and that declaration MUST be machine-readable and reportable.

**Verification:** each supported language has a published extraction-depth declaration, and a
conformance fixture per language demonstrates every declared kind and class is actually produced
(`QA-6`).

### FR-004 — The system MUST allow a language to be added without modifying existing language support. *(assumed)*

**MUST.** A new language is added by implementing the extraction contract and registering it. Adding
one MUST NOT require editing any other language's extraction code, and MUST NOT require a fork.

**SHOULD:** support a **lighter contract for declarative languages.** Infrastructure and
configuration formats have no inheritance, no method resolution and no call graph, so a
general-purpose extraction contract is largely meaningless for them; requiring the full contract is
how support for them never gets built.

**Verification:** a new language is added in a test, exercising only the extension path, with no diff
to any existing language's extraction code. The declarative path is exercised by at least one
configuration-format fixture.

**Open (sync C1):** whether a second, language-server-backed analysis path exists at all. It is not a
flag — an extraction contract shaped around syntax-tree access cannot be satisfied by a language
server, so it is a second architecture.

### FR-005 — The ingestion stage SHOULD analyse declarative infrastructure and configuration formats. *(VERIFIED)*

**SHOULD.** Infrastructure-as-code and container-orchestration manifests are a large share of what
agents in this environment work on, and **no surveyed prior art covers them well** — which is why
this is evidenced rather than assumed. Absent it, the graph is blind to a substantial fraction of the
corpus and every answer over that fraction is confidently incomplete.

**Verification:** a fixture containing infrastructure and orchestration manifests yields nodes and
edges connecting declared resources to the code that references them. Coverage is reported as an
extraction depth per `FR-003`, not as a boolean.

**Amended 2026-08-20 — one class of declarative format is not optional.** The target corpus is a Rust
workspace (`analysis/0007`), and **workspace membership, inter-crate dependency edges and feature
declarations exist only in package manifests** — no source file contains them. So manifest extraction is
a MUST even though the surrounding requirement is a SHOULD, because without it the graph has no notion of
the corpus's own module decomposition. Broader infrastructure-and-configuration coverage remains a
SHOULD.

**Related:** `GAP-005`, `analysis/0007`, sync **C1**.

### FR-006 — The ingestion stage MUST resolve references that span files. *(assumed)*

**MUST.** Imports, inheritance, interface implementation and method override MUST be resolved across
file boundaries. Framework wiring MAY be resolved, and where it is, those edges MUST carry a distinct
**edge class** so a caller can include or exclude them.

**Verification:** a multi-file fixture in which every cross-file relationship kind appears exactly
once; each is present in the graph with the correct class and direction.

### FR-007 — The ingestion stage MUST extract route-to-handler mappings. *(assumed)*

**MUST.** For each supported web framework, the mapping from an externally-addressable route to the
code that handles it MUST be a first-class edge, not an inference left to the caller.

**Verification:** a fixture per supported framework; every declared route resolves to exactly one
handler node, and unresolvable routes are reported rather than dropped.

### FR-008 — The ingestion stage MUST extract remote-procedure and tool-definition mappings. *(assumed)*

**MUST.** Where a repository declares an RPC service, a schema-defined procedure, or an agent tool
definition, the mapping from the declaration to its implementation MUST be extracted on the same
terms as `FR-007`.

**Verification:** as `FR-007`, per supported declaration format.

**Amended 2026-08-20 — this is a primary capability, not a peripheral one.** In the target corpus the
deployable units communicate over gRPC/HTTP (`analysis/0007`), so an RPC service definition **is** the
boundary between them. A graph that does not cross it cannot answer any question that spans two binaries,
which is most of the interesting ones.

### FR-009 — The derivation stage MUST derive flows from the graph. *(assumed)*

**MUST.** A **flow** is an ordered chain of symbols representing one end-to-end execution path. Flows
are derived, not declared, and each MUST carry a **derived identity** addressable by the query
surface.

**Verification:** for a fixture with known execution paths, the derived flow set contains each of them
and its ordering is correct.

### FR-010 — The derivation stage MUST derive clusters by whole-graph partitioning. *(assumed)*

**MUST.** Clusters name cohesive areas of a codebase. The partitioning algorithm is **not specified
here** — it is a data-model and cost decision for sync **B3**. What is specified is that clusters
exist, carry identities, and are addressable.

**Verification:** a fixture with deliberately separable areas partitions into clusters that respect
those boundaries, asserted as a property (no node in two clusters; every node in one).

### FR-011 — The system MUST decide incremental versus full work BEFORE performing the expensive work. *(VERIFIED)* — **inherited-negative**

**MUST.** Change detection MUST run first and MUST determine the **compute** set, not merely the write
set. The system MUST state the granularity at which change is detected — at minimum per file, and per
file is sufficient only if the compute set can be expanded to whatever cross-file resolution requires.

**Why this is evidenced:** in the reference implementation the full parse-and-analyse pipeline always
ran to completion, and the incremental-versus-full decision was taken **after** it. Only the database
write was incremental, so 100% of the compute was unconditional. A design that skips only the write
has an incrementality feature that does not reduce the cost.

**The consequence we dislike:** cross-file resolution genuinely needs data from files that did not
change, so a correct compute set is larger than the change set and is not free to compute. This
requirement therefore forbids the easy answer (parse everything, write selectively) without making
the hard answer cheap. Expect the compute-set expansion rule to be the most-revised part of the
design.

**Verification:** instrument what was skipped. For a one-file change in a repository at the `SCALE-1`
target, the count of files parsed, the count of nodes re-extracted and the count of derivation passes
run MUST each be materially below the full-run figure, reported by telemetry (`OPS-3`). Wall-clock
alone is not acceptable evidence, because a cache can flatter it.

### FR-012 — The system MUST update an index incrementally at the stated granularity. *(VERIFIED)* — **inherited-negative**

**MUST.** Work is proportional to what changed. Deletion is part of this: a symbol removed from
source MUST lose its node, its edges, its embedding, its lexical entries and its membership of every
derived structure.

**Verification:** a three-step fixture — index, modify one file, index again — asserting that the
graph after step 3 is **identical** to a full rebuild of the modified source. Equality against a full
rebuild is the only honest test of an incremental path.

### FR-013 — The system MUST support a full rebuild on request. *(operational)*

**MUST.** An operator MUST be able to discard and rebuild an index deliberately. A full rebuild MUST
be a request, never an unannounced consequence of something else — see `FR-019`.

**Verification:** a full rebuild produces an index equal to one built from empty state.

### FR-014 — The system MUST index a repository, or update a stale index, on request. *(assumed)*

**MUST.** The caller names a repository by identity. The system determines whether the index is
absent, stale or fresh, and does the least work that makes it fresh.

**Verification:** three calls — absent, stale and fresh — produce a build, an update and a no-op
respectively, distinguishable in the job record.

### FR-015 — The system MUST report index status and freshness for a repository. *(assumed)*

**MUST.** Status includes the **index generation**, whether it is fresh or stale, what it was built
from, and when. In the local shape `git-ctx` MAY resolve "the current repository" from the working
directory as a convenience; in the service shape **no ambient current repository exists** and the
request MUST name one.

**Verification:** status is correct across a fresh index, a modified working tree, and a moved commit.

### FR-016 — The derivation stage MUST generate embeddings for embeddable nodes. *(assumed)*

**MUST.** Which node kinds are embeddable MUST be declared. Embedding MUST be resumable: an
interrupted run MUST NOT restart from zero.

**Verification:** an interrupted embedding run, resumed, produces the same vector set as an
uninterrupted one, and performs materially fewer provider calls than a restart.

### FR-017 — The derivation stage MUST maintain a lexical index over indexed text. *(assumed)*

**MUST.** Whether it is held in the graph store or in a dedicated text-search slot is an `EXT-5`
placement decision; that it exists and is queryable is a requirement.

**Verification:** lexical ranking returns known matches for a fixture corpus, and the index reflects
the current generation after an incremental update.

### FR-018 — The system MUST persist derived structures with identities the query surface can address. *(VERIFIED)* — **inherited-negative**

**MUST.** Flows and clusters are addressable. Whether those identities MUST be **stable across
runs** is an open decision (`questions/0004`) and it changes the character of this requirement: if
they must be stable, this is a **correctness** requirement; if not, it is a cost requirement.

**Why this is evidenced:** in the reference implementation, whole-graph partitioning and derived-flow
extraction were recomputed wholesale on every run while their identifiers were primary keys of the
query surface. So recomputation changed **answers**, not merely cost — and any stored reference to a
derived structure silently broke.

**Verification:** two consecutive runs over unchanged source produce identical derived identities.
Two runs over source differing by one unrelated file produce derived identities whose churn is
reported. A run whose churn is unreported fails this requirement even if the churn is small.

### FR-019 — The system MUST enumerate and report every condition that escalated an incremental run to a full rebuild. *(VERIFIED)* — **inherited-negative**

**MUST.** Escalation conditions MUST be a closed, documented set. When one fires, the run MUST report
which one, in a form an operator can read and a metric can count.

**Why this is evidenced:** the reference implementation had ten distinct internal conditions that
silently escalated to a full rebuild. From the outside this is indistinguishable from incrementality
that does not work, and it makes capacity planning impossible.

**Verification:** provoke each documented escalation condition in a test; each is reported by name.
A condition that can fire but is not in the documented set is a defect.

## B. Query and analysis

### FR-020 — The serving stage MUST execute a caller-supplied read-only graph query. *(assumed)*

**MUST.** The query language is openCypher-shaped. **Write operations MUST be rejected**, and
rejection MUST be by the query surface's own guarantee rather than by a store's read-only mode alone,
so the guarantee does not depend on which backend is configured.

**Verification:** a corpus of write-shaped queries is rejected against every configured backend,
including an embedded one opened read-write. Rejection is asserted at the surface, not the store.

### FR-021 — The serving stage MUST answer hybrid search combining traversal, lexical and semantic ranking, grouped by flow. *(assumed)*

**MUST.** The three lanes are fused by the single rank-fusion implementation required by `FR-071`.
Results are grouped by **flow**. Each result MUST state which lanes contributed to it.

**MUST:** when a lane is unavailable — no embedding provider configured, no lexical index built — the
answer MUST degrade to the remaining lanes **and say which lanes were absent**. Silently returning
single-lane results as though they were hybrid is a wrong answer.

**Verification:** a fixture with known ground truth; the fused ranking is asserted, and each
lane-unavailable case is asserted to report the absence.

### FR-022 — The serving stage MUST return a 360-degree view of a symbol. *(assumed)*

**MUST.** Categorised references — callers, callees, implementors, overriders, tests — plus the flows
the symbol participates in. Categories are named **edge classes**, not a bag of "references".

**Verification:** a fixture symbol with one reference of every category returns each in the correct
category.

### FR-023 — The serving stage MUST answer reachability between two symbols, with a witness path. *(assumed)*

**MUST.** A positive answer MUST include the concrete path that justifies it. A positive result
without a witness is unverifiable by its consumer, which makes it useless for change safety.

**MUST:** the answer is one of the **three states**. An exhausted budget is `undetermined`, never
"not reachable".

**Verification:** a fixture with a known path returns it; a fixture with no path under the stated edge
set returns `none`; a fixture whose path exceeds the depth bound returns `undetermined`.

### FR-024 — The serving stage MUST answer blast radius: upstream, transitive, depth-bounded, per projection. *(assumed)*

**MUST.** Input is one or more symbols. The traversal is **upstream** — what reaches the input. It is
**transitive**, with a depth bound, and the response MUST state:

- the **edge set** it was computed under;
- the **depth bound**, and whether that bound is a **correctness statement** ("nothing is asserted
  beyond depth N") or a **budget** ("the walk stopped at N and there may be more");
- the **three-state result**;
- the projections requested. Required projections: affected **symbols**, **files**, **flows**,
  **routes**, **tests** and **downstream repositories**.

**MUST NOT:** collapse the result into a single risk number. A score can read *low* while the walk was
truncated, and the prior art demonstrated exactly that failure — a verdict derived purely from how
many precomputed groupings were touched, so a changed symbol belonging to none reported zero affected
and low risk however many direct callers it had.

**Verification:** per projection, a fixture with known ground truth. Separately, a truncation fixture
asserting that `undetermined` is returned and that no projection reports a clean count.

**Open (sync A5):** the default edge set, whether named profiles exist, and whether the projections
share one traversal. The last is a module seam and is the architect's.

**Open, added 2026-08-20 — the response has no way to state a build configuration, and it needs one.**
The target corpus uses conditional compilation, and `CON-7` mandates per-backend feature flags, so
**edges are conditional on a feature set** (`analysis/0007`, `GAP-018`). A blast radius computed under one
feature set is wrong under another: a symbol reachable only when a feature is enabled is either included,
overstating reach for a deployment that disables it, or excluded, understating it for one that enables it.
Whichever way this is resolved, **the feature set the answer was computed under MUST appear in the
response alongside the edge set and the depth bound** — it is a correctness statement of exactly the same
kind. Owned by **B3**, because it is a data-model question before it is a query one.

### FR-025 — The serving stage MUST answer downstream reachability from a symbol. *(assumed)*

**MUST.** The opposite direction from `FR-024` — what the symbol reaches. Same contract: stated edge
set, stated bound, three-state result.

**Verification:** as `FR-024`, with direction reversed on the same fixtures.

### FR-026 — The serving stage MUST answer diff impact for a working tree. *(assumed)*

**MUST.** The change set is the uncommitted state of a local working tree. Diff impact is **blast
radius with a change-set input** — a projection over `FR-024`, not a separate mechanism.

**Verification:** a fixture repository with staged, unstaged and mixed changes; the affected set
equals blast radius computed from the same symbols directly. **Equality with `FR-024` is the test** —
divergence means two mechanisms exist.

### FR-027 — The serving stage MUST answer diff impact for a `base...head` ref pair. *(VERIFIED)* — **inherited-negative**

**MUST.** Two named refs, compared to each other — not a ref compared against the working tree.

**Why this is evidenced:** the reference implementation's comparison mode diffed a ref against the
local working tree and required a checkout, so a pull request's `base...head` was **not expressible**.

**Verification:** the same two refs produce the same answer regardless of what the working tree
contains, including when it is dirty.

### FR-028 — The serving stage MUST answer diff impact for a supplied patch, with no checkout. *(VERIFIED)* — **inherited-negative**

**MUST.** A caller supplies a patch for a repository the system has **never checked out**. No working
tree is involved. This is what a pull-request integration requires, and the requester made it a v1
MUST on 2026-08-20.

**Applies to:** the service shape. In the local shape it is permitted but not required.

**Verification:** a patch is submitted for an indexed repository with no working tree present on the
host; a correct diff-impact answer is returned. Then the same patch is submitted for a repository at a
different **index generation**, and the response's freshness field reflects the older generation
rather than silently answering against it.

**The consequence we dislike:** this forces the change-set input to be decoupled from repository
acquisition, which means the system must map patch context lines onto indexed symbols without being
able to read the post-change file. That mapping is lossy, and `GAP-003` records the inference that it
may require a syntax-aware diff rather than a line diff (sync **C3**).

### FR-029 — The serving stage MUST allow any graph result to be filtered by node type and edge class. *(assumed)*

**MUST.** Filtering is a parameter of the query, not a post-processing step the caller performs, so
that a filtered query can be cheaper than an unfiltered one.

**Verification:** filtered and unfiltered results are consistent (the filtered set is a subset), and
the filtered query's reported work is lower.

### FR-030 — The serving stage MUST return nodes within N hops of a selection, N caller-configurable. *(assumed)*

**MUST.** N is supplied by the caller. A maximum MUST exist and MUST be documented; a request above it
MUST be **rejected with an error naming the maximum**, never silently clamped — a clamped result looks
complete and is not.

**Verification:** N of 1, 2 and the maximum return correct sets; the maximum plus one is rejected with
an error that states the maximum.

### FR-031 — The serving stage MUST report node and edge counts, in total and by type. *(assumed)*

**MUST.** Counts MUST name the **index generation** they were taken at, so two counts can be
compared meaningfully.

**Verification:** counts on a fixture match a known census; counts taken across an incremental update
differ by exactly the expected delta.

### FR-032 — The serving stage MUST scope or filter the graph to a sub-directory of a repository. *(assumed)*

**MUST.** Scoping applies to search, symbol views, counts and traversal. A traversal scoped to a
sub-directory MUST report when a path left the scope, rather than silently truncating there —
otherwise scoping produces a false `none affected`.

**Verification:** a traversal whose only path exits the scoped sub-directory returns `undetermined`
with the reason, not `none`.

### FR-033 — The serving stage MUST run read-only structural checks against the indexed graph. *(assumed)*

**MUST.** A check is a named, read-only assertion over the graph — for example, that no node of one
kind reaches a node of another kind. Checks MUST be enumerable, individually runnable, and MUST report
per-finding locations.

**MUST NOT:** modify anything. This is a read capability with a rule-shaped input.

**Verification:** a fixture violating each shipped check reports exactly the expected findings; a clean
fixture reports none.

### FR-034 — The serving stage MUST check response-shape conformance against consumers' property accesses. *(assumed)*

**MUST.** Given a declared or inferred response shape at a producer, and the property accesses
observed at its consumers, report accesses that the shape does not satisfy. Requested by the requester
on 2026-08-20 as part of the web/API group.

**Verification:** a fixture with a producer and three consumers — one conforming, one accessing an
absent property, one accessing a property of the wrong shape — reports exactly the two violations.

**Honest limitation to state in the output:** where a shape is inferred rather than declared, a
finding is evidence, not proof. This capability MUST distinguish declared from inferred shapes in its
findings, on the same principle as **evidence class**.

**Amended 2026-08-20 — the declared case dominates in the target corpus, which materially de-risks this.**
gRPC and HTTP schema definitions are authoritative contracts, so conformance becomes "compare a **declared**
schema against observed consumer field accesses" rather than "infer a producer's shape from its return
statements". `analysis/0003` had marked this capability the one whose correctness was least well-defined;
that judgement stands for ad-hoc handlers and no longer holds for the primary corpus (`analysis/0007`).

### FR-035 — The serving stage MUST produce a pre-change report for a named route handler. *(assumed)*

**MUST.** Given a route handler, report what depends on it: its consumers, its declared contract, the
flows it participates in, and its blast radius under the stated edge set. This is a **projection over
existing capabilities**, not a new traversal.

**Verification:** the report's blast-radius section is byte-identical to `FR-024` invoked directly on
the same handler. Divergence means a second traversal was written.

### FR-036 — The system MUST generate a repository wiki as a structured document set derived from the graph. *(assumed)*

**MUST.** The output is a **document set**, not a rendering: a collection of addressable pages with a
declared structure, which a surface may render and a caller may write to disk.

Required structure:

1. **One page per module**, where a module is a **derived cluster** (`FR-010`) — not a grouping computed
   separately for the wiki. Two groupings of the same codebase that disagree is a defect, and the
   clusters already exist.
2. **One overview page** linking every module page.
3. **Cross-references that resolve.** Every reference from a page to a symbol, flow or cluster MUST be
   a resolvable graph identity, not a text match.
4. **The index generation** it was derived from, on every page (`FR-039`).
5. **Navigable without graph vocabulary** — the non-technical persona is a primary consumer.

**Prose is a separate, optional stage.** Page *structure* and its cross-references MUST be derived
deterministically from the graph. Narrative text MAY additionally be generated by a configured AI
provider, and where it is:

- it MUST be attributed as generated, per page, distinguishably from derived structure;
- it MUST be reachable only through the provider path governed by `IF-12`, restrictable to absence by
  `IF-13`, and enumerable as a code-egress path under `SEC-13`;
- its absence MUST leave a usable document set. A wiki that is empty without an AI provider has made
  prose the product.

**Verification:** in two parts, because the halves are not testable the same way.

- **Structure — automated.** For a fixture repository with known clusters: one page per cluster plus an
  overview; every cross-reference resolves to an existing graph node; every page states the index
  generation; the page set is stable across two runs over unchanged source. Additionally, with no AI
  provider configured, the document set is still produced and still navigable.
- **Prose — human judgement, and stated as such.** Narrative quality is not automatically assertable.
  A named reviewer judges a fixture repository's output acceptable, and that judgement is recorded.
  This is the only requirement in this corpus whose verification is a person, and pretending otherwise
  would be worse than admitting it.

**The alternative this rejects, recorded because the precedent takes it.** The reference implementation
groups files into modules **using the language model**, then generates a page per module. That is a
legitimate design and this requirement deliberately does not follow it: grouping by derived cluster is
deterministic, testable, reuses a capability that must exist anyway, and confines the provider to prose.
The cost is that clusters are optimised for graph cohesion rather than for readability, so the module
boundaries may be less intuitive than an LLM's would be. **If reviewers find cluster-shaped modules
unreadable, that is the signal to revisit** — see `questions/0011`.

**Residual open question:** whether prose is wanted at all in v1, which is a security-surface decision
before it is a product one, because it turns a documentation feature into a code-egress path
(`questions/0011`).

### FR-037 — The system WON'T answer statement-level dependence queries in v1. *(satisfied by design)*

**WON'T (v1).** Statement-level control and data dependence is a different index, a different cost
class and an interprocedural analysis. Deferred by the requester on 2026-08-20.

**What v1 MUST nonetheless do:** name the seam. The analysis contract MUST admit a
statement-granularity unit of analysis without redefining the existing symbol-granularity contract, so
that dependence inserts rather than forcing a redesign. Concretely: the unit of analysis MUST be an
explicit parameter of an analysis request, with `symbol` the only value accepted in v1.

**Verification:** the request contract accepts a unit-of-analysis parameter; supplying `statement`
returns an explicit *not supported in this version* error rather than a validation failure or a wrong
answer.

**Revisit trigger:** a consumer asks for source-to-sink reasoning that blast radius cannot answer.

### FR-038 — The system WON'T persist or explain taint findings in v1. *(satisfied by design)*

**WON'T (v1).** Depends on `FR-037`. Deferred by the same decision.

**Verification:** as `FR-037` — the capability is absent and its absence is explicit, not an error.

**Revisit trigger:** as `FR-037`, or a security-review consumer requiring source-to-sink findings.

### FR-039 — The serving stage MUST return the index generation and freshness with every analysis answer. *(assumed)*

**MUST.** Freshness is a **field of the answer**, not a log line and not a separate call. An analysis
computed against a stale index is confidently wrong, which is worse than unavailable.

**MUST:** where an index is stale, the answer MUST say so. Whether staleness degrades an answer to
`undetermined` or merely annotates it is an open decision (sync **A5**); this requirement fixes only
that the caller can tell.

**Verification:** every analysis response schema carries generation and freshness; asserted
structurally across the whole surface, not per capability. A capability that can answer without them
fails this requirement.

## C. Repositories, groups and acquisition

### FR-040 — The system MUST discover all indexed repositories, paginated by limit and offset. *(assumed)*

**MUST.** A maximum page size MUST exist and be documented. A request above it MUST be **rejected with
an error naming the maximum**, not clamped.

**Verification:** pagination across a fixture set returns each repository exactly once with no gaps or
duplicates; an over-maximum limit is rejected with the maximum in the message.

### FR-041 — The system MUST allow the active repository to be changed. *(assumed)*

**MUST.** In the local shape, switching is a session or invocation concern. In the service shape, every
request names its repository and "switching" is therefore a client-side notion — the server MUST NOT
hold ambient per-connection repository state, because that is how one caller's switch becomes
another's wrong answer.

**Verification:** two concurrent sessions addressing different repositories on one replica each
receive answers for their own repository. Asserted under concurrency, not sequentially.

### FR-042 — The system MUST serve more than one repository simultaneously. *(VERIFIED)* — **inherited-negative**

**MUST.** Cross-repository analysis requires two or more repositories readable at once. The number
simultaneously served MUST be bounded by available capacity, not by a constant — see `SCALE-3`.

**Why this is evidenced:** the reference implementation capped resident repositories at a small
integer with LRU eviction, where eviction cost a full database reopen — so exceeding the cap converted
steady-state serving into open-and-close thrash.

**Verification:** with more repositories registered than any internal residency figure, a round-robin
read across all of them shows no latency cliff attributable to eviction. Reported per repository by
telemetry.

### FR-043 — The system MUST list configured repository groups. *(assumed)*

**MUST.** A group is a named set of **deployable units** analysed together.

**Amended 2026-08-20 — the member unit is a deployable unit, not a repository.** The original wording
assumed cross-service contracts are cross-*repository*. In the target corpus they are **intra**-repository:
one workspace contains many libraries and many binaries, and the binaries communicate over gRPC/HTTP
(`analysis/0007`). A group whose members must be repositories cannot express that at all.

So a member is a unit that is separately deployed and separately addressable — in the target corpus, a
workspace member producing a binary. A group MAY span repositories, and MUST NOT require it.

**Verification:** the listed groups match configuration, including an empty result when none exist, and a
group whose members are two deployable units **within one repository** is expressible and produces
cross-member edges (`FR-044`).

### FR-044 — The system MUST rebuild a group's contract registry and cross-repository links. *(assumed)*

**MUST.** Rebuilding extracts declared interfaces from each member and links a consumer's calls to a
provider's handlers.

**Verification:** a two-member fixture with one declared contract produces exactly one cross-member
edge, and removing the declaration removes it. Asserted for members in **two repositories** and for
members **within one repository**, since `FR-043` requires both to be expressible.

### FR-045 — The system MUST acquire a repository from a remote and update one already acquired. *(assumed)*

**MUST.** Applies to the service shape. Acquisition MUST be separable from analysis: `FR-028` requires
diff impact for a repository never checked out, which is only coherent if acquisition and analysis
input are distinct concerns.

**MUST:** acquisition MUST verify that an existing local copy corresponds to the requested remote
before updating it. Two remotes whose paths collide MUST produce an error, never a silent update
against the wrong origin.

**Verification:** a collision fixture — two distinct remotes whose names collide — produces an error.
Re-acquisition of the same remote is idempotent.

### FR-046 — The system MUST authenticate to a private remote without exposing the credential. *(VERIFIED)*

**MUST.** The credential MUST NOT appear in a process argument list, in a log, in an error message, or
in any response. It MUST be scoped to the host it is for. Credential-bearing diagnostics MUST be
suppressed rather than captured.

**Why this is evidenced:** the estate has measured that argument lists are visible to any local
process, and the grounding recorded a prior-art design that specifically scrubbed transport-trace
variables because inheriting them dumps request headers — including an injected credential — into
captured stderr. The failure mode is known, not hypothetical.

**Verification:** a test acquires from an authenticating fixture remote and asserts the credential
appears in no argument list, no log line and no error path. Asserted by scanning captured output for
the secret, with a positive control proving the scan would find it.

### FR-047 — The serving stage MUST distinguish observed from inferred edges in cross-repository answers. *(assumed)*

**MUST.** An edge inferred from a declared contract is weaker evidence than a call read from a syntax
tree. Every cross-repository answer MUST carry the **evidence class** per edge, and MUST NOT weigh the
two identically in any ranking or count without saying so.

**Verification:** a fixture containing one observed and one inferred cross-repository edge returns
both, each correctly classified; a blast-radius answer over them reports the two classes separately.

**Related:** `GAP-008`, which records that no prior art has been surveyed for a usable confidence
model here — so the *representation* is required, and the *weighting* is deliberately unspecified.

## D. Write operations against source

### FR-050 — The system MUST perform coordinated multi-file rename AST-accurately, and MUST update the index in the same operation. *(VERIFIED)* — **inherited-negative**

**MUST.** All of the following, and each of them is a separate clause because each corresponds to a
measured failure:

1. The edit set MUST be determined from the graph, **AST-accurately**. Text matching MUST NOT
   determine the edit set, and MUST NOT be used to widen it.
2. Comments and string literals MUST NOT be rewritten unless they are themselves references the
   extraction contract recognises.
3. The index MUST be updated as part of the operation. A rename that leaves the index stale is a
   failed rename.
4. A preview mode MUST exist and MUST be the default.
5. Every failure — of the search, of a write, of the index update — MUST surface. A swallowed failure
   is a defect, not a degradation.
6. The set of file types the operation covers MUST equal the set of languages with extraction support.
   A language the graph knows about but rename cannot edit MUST be **rejected explicitly**, not
   skipped.

**Why this is evidenced:** the reference implementation's rename was a whole-file word-boundary regex
that rewrote comments and string literals, wrote nothing back to the graph so the index was stale the
instant it succeeded, silently swallowed its search tool's failure, and omitted several languages the
graph supported. It also contradicted its own project's written guidance against renaming by
find-and-replace.

**Verification:** a fixture where the symbol name also appears in a comment, in a string literal, and
as a different symbol in another scope. The rename changes exactly the true references. A subsequent
query for the old name returns nothing and for the new name returns the full reference set — which
proves clause 3. Then a fault-injection test fails the index update and asserts the operation reports
failure.

**The consequence we dislike:** clause 6 means adding a language to the graph without adding rename
support for it makes rename *reject* that language rather than silently do nothing. That is a worse
demo and a better guarantee.

## E. Platform capabilities

### FR-068 — The system MUST treat indexing as durable, queued, cancellable work. *(VERIFIED)* — **inherited-negative**

**MUST.** Specifically:

1. Submitting a second repository while one is indexing MUST **queue** it, not reject it. A status
   value meaning "queued" MUST correspond to a real backlog.
2. Job state MUST be durable — it MUST survive a restart of the serving process.
3. A job MUST be cancellable, and cancellation MUST leave the index in a valid state, either the prior
   generation or a complete new one.
4. Job status MUST be observable, with progress.

**Why this is evidenced:** in the reference implementation one repository's index run rejected every
other repository's, in memory, with no queue and no durable job state — so one tenant blocked all
others, and a restart lost every job's existence.

**Verification:** submit two repositories concurrently; both complete. Submit one, restart the process,
and query the job — it is still known. Cancel a running job and assert the index is readable and
consistent afterwards.

### FR-071 — The system MUST have exactly one implementation of rank fusion, with one documented join key. *(VERIFIED)* — **inherited-negative**

**MUST.** Every surface that fuses ranked lists — hybrid search, the symbol view, any ranked blast-radius
projection — MUST use the same implementation, the same parameters and the same **join key**.

**Why this is evidenced:** the reference implementation had three separate fusion implementations with
divergent effective constants and different join keys, and the highest-traffic surface used none of the
others. The same query therefore answered differently depending on which surface asked.

**Any numeric parameter MUST be defined in exactly one place and MUST be documented with a reason.**
No parameter is inherited from prior art; every one is ours and justified.

**Verification:** an executable check asserting exactly one fusion code path exists and that every
ranking consumer reaches it. Plus a differential test: the same query through every surface returns the
same ranking. This is a **release gate** (`QA-11`), not a review item — a comment saying "use the shared
fusion" does not satisfy this requirement.

### FR-073 — The system MUST carry an index across a version upgrade without a full reindex. *(VERIFIED)* — **inherited-negative**

**MUST.** An upgrade MUST migrate. Specifically:

1. A change to the persisted model MUST NOT, by itself, invalidate an index.
2. Caches MUST NOT be keyed on the software's release version.
3. Unknown fields MUST be tolerated on read, so a newer index is readable by a slightly older reader
   where the model permits.
4. **Derived** data MAY be dropped and rebuilt. **Authoritative** data MUST be migrated — with
   `analysis/0001` and `specs/01` §D4 recording that job state and audit records are authoritative and
   unrecoverable by any amount of reindexing.

**Why this is evidenced:** in the reference implementation a schema-fingerprint change disabled
incrementality entirely, and the parse cache was keyed on the package version — so **every release
reindexed everything**.

**Verification:** build an index on version N, upgrade to N+1 across a deliberate model change, and
assert the index is served without a rebuild. This is a release gate (`QA-12`).

## Requirements the capability list did not contain

Recorded explicitly so the additions are visible rather than smuggled in: `FR-019` (escalation
reporting), `FR-039` (freshness on every answer), `FR-047` (evidence class), and the seam clauses of
`FR-037`. Each is filed in `GAPS.md` with its confidence.

## Verification

### What is proven

- **Every entry in the requester's Appendix A has a requirement**, and the mapping is recorded in
  `analysis/0003-feature-gaps.md`.
- **All eleven inherited negatives appear**, each tagged **inherited-negative**, each `(VERIFIED)`,
  each with a verification method: `FR-011`, `FR-012`, `FR-018`, `FR-019`, `FR-027`, `FR-028`,
  `FR-042`, `FR-050`, `FR-068`, `FR-071`, `FR-073`, plus `PERF-1`, `SCALE-3`, `SEC-1`, `SEC-3`,
  `SEC-7` and `IF-4` in the sibling files.
- **`FR-026`, `FR-035` and `FR-024` are specified as one mechanism with projections**, and each
  verification asserts *equality* with `FR-024` rather than mere correctness. That is what makes
  "one traversal, N projections" testable rather than aspirational.
- **Every MUST here has a verification method.** Counted: no requirement in this file lacks one.

### What is NOT proven

- **`FR-036`'s prose half is verifiable only by a person.** Its structural half is automatically
  assertable and is specified as such; narrative quality is not. That is a genuine limit, not a gap in
  the specification, and it is the only requirement in this corpus whose verification names a human.
  *(Amended 2026-08-20 — an earlier draft of this file called `FR-036` unimplementable because no
  output contract existed. That was wrong: the prior art demonstrably does this, and its public
  documentation describes the contract. The requirement now has one, and `questions/0011` is narrowed
  to the residual.)*
- **`FR-005`'s extraction depth is unspecified.** "Analyse declarative formats" is evidenced as a
  need; what depth is useful is not known, and picking one now would be invention. Sync **C1**.
- **`FR-011`'s compute-set expansion rule does not exist.** The requirement says the compute set must
  be decidable before the work; it does not say how, because nobody knows yet, and the grounding
  records that the obvious approach — following import edges — is insufficient for inheritance and
  type resolution and degrades unsafely when it fails.
- **`FR-024`'s default edge set is unspecified**, and it is the highest-leverage single decision in
  the analysis surface. Sync **A5**.
- **`FR-028`'s patch-to-symbol mapping accuracy is unknown**, and `GAP-003` records the inference that
  a line-based diff loses accuracy exactly on moves and reformatting. Sync **C3** gates it.
- **`FR-047` requires representing evidence class but not weighing it.** Deliberate — no surveyed prior
  art offers a confidence model, and `GAP-008` records that nobody has looked.
- **No requirement here has been reviewed by the requester.** Sync **A1** and **A3**.

## Amendments

- **2026-08-20 (same day, second pass)** — **The target corpus was answered** — a Rust workspace of
  library and binary crates, potentially several binaries over gRPC/HTTP — and the implications are
  derived in `analysis/0007-target-corpus-implications.md`. Amendments landed on `FR-005` (manifest
  extraction is a MUST inside a SHOULD), `FR-008` (promoted to primary), `FR-024` (needs a feature-set
  predicate it does not have — `GAP-018`), `FR-034` (materially de-risked, because the declared case now
  dominates) and `FR-043`/`FR-044` (the member unit is a **deployable unit**, not a repository).
- **2026-08-20 (same day)** — **`FR-036` corrected.** An earlier draft called it unimplementable for want
  of an output contract. That was wrong — the prior art ships the capability and its public documentation
  describes the contract. `FR-036` now specifies a structured document set with optional, separately-gated
  prose, and a two-part verification. `questions/0011` is narrowed to the residuals.
- **2026-08-20** — Created. `FR-037` and `FR-038` recorded as `WON'T (v1)` per the requester's decision
  of the same date, with the seam clause added so the deferral is not a dead end. `FR-027`, `FR-028`,
  `FR-034`, `FR-035`, `FR-023`, `FR-024` and `FR-050` reflect the same date's decision that all
  previously-omitted capabilities are wanted.

## Related

- `analysis/0001-capabilities.md` — the `CAP-0nn` rows these requirements carry.
- [`03-non-functional-requirements.md`](03-non-functional-requirements.md) — `PERF-1`, `SCALE-3` and the rest of the inherited negatives.
- `discussions/0001-what-impact-analysis-means.md` — the seven axes behind `FR-023`–`FR-028`.
- [`../FEATURES.md`](../FEATURES.md) — the two-way traceability index.
