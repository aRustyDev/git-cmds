# SPEC 04 — Interfaces and external systems

> **Aspirational.** Status markers record justification strength, not implementation status.
> Vocabulary as ratified in [`GLOSSARY.md`](../GLOSSARY.md).

- **Date:** 2026-08-20
- **Two halves.** `IF-*` specifies the surfaces callers arrive on. `EXT-*` specifies the external
  systems the platform depends on, including the six swappable store slots.
- **Product names appear only in this file**, and only as compatibility targets marked `presumed`.
  Requirements elsewhere name capability profiles, never products.

## Part 1 — Interface requirements

### The surfaces

| Surface | Consumers | May mutate? | Present in |
|---|---|---|---|
| **CLI** (`git-ctx`) | developer, admin, CI | yes | local shape; optionally service shape as a client |
| **API** | web UI, integrations, CI | yes | service shape |
| **MCP surface** | agents | yes, narrowly | both shapes |
| **Web UI** | developer, non-technical stakeholder | via the API | service shape |
| **TUI** | developer | undecided | **unspecified** — `GAP-001`, `questions/0009` |

### IF-1 — Every surface MUST project one internal contract. *(VERIFIED)* — **inherited-negative**

**MUST.** The surfaces are thin projections of a single internal contract. A surface MUST NOT
implement analysis behaviour of its own.

**Why this is evidenced:** in the reference implementation two entry points to nominally the same
functionality had **different authentication, different concurrency behaviour and different operation
inventories** — and, separately, its ranked-result fusion existed three times with the
highest-traffic surface using none of the shared implementations. Four surfaces over four hand-rolled
adapters is how a codebase acquires divergent behaviour per interface.

**Verification:** a differential suite issuing the same logical request through every surface and
asserting identical answers, identical three-state verdicts and identical rankings (`QA-9`, `COR-5`).
A surface that cannot express a request the internal contract supports is a gap in the projection and
must be recorded as one.

**Open (sync B5):** whether the MCP surface is a projection of the API or a first-class surface with
its own contract. It has its own conventions — tool inventories, session semantics, output budgets —
which is an argument for the latter; `IF-1` binds either way.

### IF-2 — Every surface MUST state, per operation, whether it reads or mutates. *(assumed)*

**MUST.** The read/write classification is part of the published contract, machine-readable, so a
deployment can restrict a surface to reads without enumerating operations by hand.

**Verification:** a read-only deployment mode rejects every mutating operation, derived from the
classification rather than from a hand-maintained list.

### IF-3 — Authentication MUST terminate in one place, and that place MUST be the same for every surface. *(VERIFIED)* — **inherited-negative**

**MUST.** See `SEC-1`–`SEC-3`. The interface statement: no surface may be reachable on terms different
from another. In particular, an operation reachable over one surface with authentication MUST NOT be
reachable over another without it.

**Why this is evidenced:** in the reference implementation one entry point required a bearer token,
enforced host checks and refused to start on a non-loopback bind without a credential, while a second
entry point to the same functionality mounted with **no authentication, no host checks, and no rate
limiting** — and started happily on any interface. The credential was validated at an edge proxy that
deliberately stripped it before the upstream hop, so the upstream had no identity to enforce or log.

**Verification:** an executable check enumerating every surface-to-operation route and asserting each
passes through the same authorisation point. Asserted structurally, not by testing routes one by one,
because the failure mode is the route nobody remembered to test.

### IF-4 — The advertised inventory MUST equal the callable inventory. *(VERIFIED)* — **inherited-negative**

**MUST.** Every operation a surface will execute MUST appear in what that surface advertises. There
MUST be no undeclared alias, no legacy name, and no operation reachable only by knowing its name.

**Why this is evidenced:** the reference implementation's agent surface advertised seventeen operations
and would execute twenty — three undeclared legacy aliases, explicitly permitted in read-only mode.
An allowlist built from the advertisement therefore silently missed three entries, which makes
governance of that surface impossible in principle.

**Verification:** an executable check asserting set equality between the advertised inventory and the
dispatch table. A deprecated operation is either advertised as deprecated or removed; it is never
hidden and live.

### IF-5 — An advertised input schema MUST be validated, not merely published. *(assumed)*

**MUST.** Publishing a schema that the surface does not enforce means the schema is a hint and the
real contract is undocumented.

**Verification:** for each operation, a request violating the published schema is rejected with a
schema error.

### IF-6 — The MCP surface MUST bound its output, and MUST report truncation as a field. *(assumed)*

**MUST.** Agents consume under a token budget. Output MUST be bounded, and where bounding removed
content the response MUST say so **in a field** — not by ellipsis, not in prose. An agent cannot read
a caveat.

**Verification:** a request whose full answer exceeds the budget returns a truncation field set, and
the retained content is a valid prefix or a valid subset rather than malformed.

### IF-7 — The MCP surface MUST require an explicit repository on every operation. *(assumed)*

**MUST.** There is no ambient current repository in the service shape (`FR-041`). Where more than one
repository is visible, the repository parameter is required, and its absence is an error rather than a
default.

**Verification:** with two repositories visible, an operation omitting the repository is rejected.
With one visible, the behaviour is documented and consistent.

### IF-8 — A session identifier MUST NOT be treated as an identity. *(VERIFIED)* — **inherited-negative**

**MUST.** Session state carries protocol state. The **principal** is established by authentication
(`SEC-1`) and MUST be carried independently of any session identifier.

**Why this is evidenced:** in the reference implementation a session was a protocol object with no
principal, no tenant and no credential attached — a routing key. Combined with a single shared static
token, that made per-caller attribution impossible in principle rather than merely unimplemented.

**Verification:** a session's record carries a principal reference; an operation on a session whose
principal is absent or expired is rejected.

### IF-9 — Repository visibility and read-only mode MUST be resolvable per request, not only per process. *(VERIFIED)* — **inherited-negative**

**MUST.** Which repositories a caller may see, and whether it may mutate, are properties of the
**principal** and the request — not of the serving process's configuration.

**Why this is evidenced:** in the reference implementation both were process-wide environment
configuration, never per-request or per-session, so one process could not serve two callers with
different repository visibility. The workaround is one process per audience, which does not scale to
10,000 agents with differing entitlements.

**Verification:** two principals with disjoint repository entitlements, served concurrently by one
replica, each see only their own.

### IF-10 — The CLI MUST be usable without any service, and MUST NOT be the only way to reach any capability. *(assumed)*

**MUST.** `git-ctx` in the local shape is self-sufficient. Conversely, no capability may exist only in
the CLI — that would make the service shape a subset rather than a peer.

**Verification:** the capability inventory is fully reachable from both the CLI and the API; asserted
as a coverage check over `analysis/0001`.

### IF-11 — The web UI MUST be specified by contract, with its implementation technology unchosen. *(operational)*

**MUST.** The platform's obligation is the contract and the budget (`PERF-4`); the frontend's
technology is deliberately not specified here. The contract MUST include:

1. **A declared query set** the UI issues, committed as an artefact, against which `PERF-4` is measured.
2. **Runtime backend discovery** — the UI MUST NOT have its backend address fixed at build time,
   because that makes one build per deployment.
3. **A graph payload contract** supporting force-directed, sequential and radial layouts, and a
   locally cached graph object on the client.
4. **A bounded-payload path** for graphs too large to send whole, with the bound and the fact of
   bounding both visible to the UI.
5. **Freshness and index generation** on every response (`FR-039`), so the UI can show what it is
   looking at.

**Verification:** the declared query set exists and is versioned; the budget gate runs against it; a
graph exceeding the payload bound is served by the bounded path with the bound reported.

**The consequence we dislike:** a declared query set is a coupling — the UI cannot add a query without
the platform accepting a new budget obligation. That friction is the point: an undeclared query is an
unbudgeted one, and `PERF-4` would otherwise be unenforceable.

### IF-12 — The AI provider MUST be configurable from deployment configuration, and MAY be configurable at runtime from the web UI. *(assumed)*

**MUST** for deployment configuration. **MAY** for the runtime path, subject to `IF-13`.

**Verification:** provider configuration takes effect without a rebuild; a runtime change is recorded
in the audit trail (`SEC-6`) with the principal that made it.

### IF-13 — Runtime AI-provider configuration MUST be restrictable, and when restricted the path MUST be absent. *(assumed)*

**MUST.** An administrator can disable runtime configuration. When disabled, the capability is **not
present** — not merely hidden from the UI. A hidden-but-reachable control is not a restriction.

**Verification:** with the restriction set, a direct request to the runtime-configuration operation is
rejected at the authorisation point, not filtered by the UI.

**Related:** `SEC-11`. Provider configuration usually carries a credential, which is why this is both
an interface and a security requirement.

### IF-14 — A TUI is not specified. *(satisfied by design)*

**WON'T (v1), pending `questions/0009`.** A terminal interface was named after the capability list was
written and has no requirements. It is recorded here as an explicit absence so it cannot be built to
whatever an implementer assumed, and cannot be silently dropped either.

**Verification:** none — this is a recorded non-requirement. `GAP-001` holds it; sync **B5** decides.

## Part 2 — External systems

### The store slots

Each slot is specified as a **capability profile**: the contract business logic depends on. Candidate
products are compatibility targets, and every one is marked `presumed` because the requester's
original per-slot product list did not survive into the trigger prompt (`questions/0010`, `GAP-010`).

### EXT-1 — The graph slot MUST be swappable between an embedded and a networked openCypher-speaking implementation. *(assumed)*

**MUST.** Capability profile:

- Store typed, directed edges between typed nodes, with properties on both.
- Answer openCypher-shaped read queries, including variable-length paths with a bound.
- Filter by node type and edge class in the query, not after it.
- Bulk-load a large node and edge set efficiently.
- Support read-only access concurrent with a write, or provide generation isolation that makes
  `COR-4` satisfiable.
- Delete a subgraph by identity, for `FR-012`.

**Candidate targets, `presumed`:** an embedded property-graph engine speaking openCypher; a networked
openCypher-speaking engine.

**The portability trap to design for, and it is the sharpest one in this file:** openCypher
implementations agree on read-side `MATCH` traversal and disagree on almost everything else —
schema definition, bulk load, index creation, full-text and vector extensions, and even the return type
of standard functions. A design whose graph-store contract is expressed as "we send openCypher strings"
is **not** portable, because the non-`MATCH` statements are the ones that differ. The profile above is
therefore stated as operations, not as a dialect.

**A second trap, and it changes the data model:** some engines index by **relationship type** while
others can carry edge kind as a property on a single relationship type. If edge class is modelled as a
property, engines that index by type cannot use their primary index for the most common filter in the
system. This is a `B3` decision with portability consequences, and it must be taken before any schema.

**Verification:** `COR-6` conformance suite, run against two implementations, one of each kind.

### EXT-2 — The vector slot MUST be swappable between an embedded and a networked implementation. *(assumed)*

**MUST.** Capability profile: store fixed-width float vectors keyed by node identity; nearest-neighbour
search by cosine distance with a result limit and a distance threshold; delete by key; report count.

**Candidate targets, `presumed`:** an in-process vector index; **Qdrant** (Apache-2.0) as the networked
target, which this estate already runs.

**Vector width is frozen at creation** and is a property of the embedding provider, so changing
provider is a migration event rather than a configuration change (`questions/0008`).

**Verification:** `COR-6`. Recall is asserted against a brute-force oracle on a small fixture, because
an approximate index that silently returns nothing is indistinguishable from an empty store.

### EXT-3 — The relational slot MUST be swappable between an embedded and a server implementation. *(assumed)*

**MUST.** Capability profile: transactional reads and writes over relational tables; unique and foreign
key constraints; ordered pagination; append-only insert for audit records; and a durable, queryable job
record for `FR-068`.

**Candidate targets, `presumed`:** an embedded single-file SQL engine; a networked SQL server. This
estate runs both a networked SQL server and a version-controlled SQL engine.

**This slot holds all of the authoritative data** — repository registry, group registry, job state,
audit records (`01-personas-and-flows.md` §D4). It is therefore the slot whose backup and migration
story matters most, and the one where "drop and rebuild" is not an available recovery.

**Verification:** `COR-6`, plus a durability test asserting job state and audit records survive a
process restart and a backend restart.

### EXT-4 — The search slot MUST provide lexical ranking. *(assumed)*

**MUST** *(amended 2026-08-20 — was a SHOULD with no consumer)*. Capability profile: index documents
with fields; **tokenise and rank by lexical relevance of the BM25 family**; **update, replace and delete
a single document without rebuilding the index**; query with filters; report ranked results with scores.

**Candidate target, `presumed`:** **OpenSearch** (Apache-2.0).

**Why this changed.** The requester dropped the separate text-search slot on 2026-08-20 and placed
lexical ranking here. That does three things:

1. **It gives this slot the consumer it lacked.** `FR-017` requires a lexical index and `FR-021` has a
   lexical lane; both are now served here. `GAP-011` is closed for this slot.
2. **It resolves a hazard rather than inheriting one.** The per-document-update clause above was
   mandatory in the retired text-search slot because the grounding measured an engine offering only
   whole-index create, drop and query — so every run re-tokenised the corpus, contradicting `PERF-6`.
   A general-purpose search engine satisfies per-document update natively, so relocating here **removes**
   that risk instead of moving it onto the graph slot.
3. **It widens the graph candidate set**, because lexical ranking is no longer a graph-engine
   requirement (`EXT-1`, `analysis/0008`).

**The cost, stated because it is real.** The lexical lane now crosses a network hop in the service shape,
and the embedded half of this slot is **unnamed** — there is no embedded OpenSearch, so `REV-2`'s
two-implementation rule needs a pure-Rust lexical index that the candidate list does not contain
(`GAP-021`). Until it does, this slot has one implementation and is therefore not yet a proven seam.

**Verification:** `COR-6`, including an incremental case asserting that updating one document does not
re-tokenise the corpus.

### EXT-5 — The system WON'T provide a separate text-search slot. *(satisfied by design)*

**WON'T** *(decided 2026-08-20)*. The slot is removed; its capability profile moved into `EXT-4`, which
is now required rather than optional.

**What this does not do:** it does not remove `FR-017`. A lexical index is still required — it is placed
in the search slot rather than in a slot of its own. Dropping the slot without relocating the requirement
would have silently removed a lane from `FR-021`, and that would have been a capability reduction
disguised as a simplification.

**Revisit trigger:** if the search slot's embedded half (`GAP-021`) turns out to be best served by a
dedicated lexical engine rather than a general-purpose search engine, this slot returns — as the embedded
half of `EXT-4` rather than as a seventh slot.

**Verification:** none — a recorded non-requirement.

### EXT-5 — The text-search slot MAY be provided by an external lexical index. *(assumed)*

**SHOULD.** Optional. Capability profile: tokenise and index text per document; rank by lexical
relevance of the BM25 family; support a stemming or normalisation policy; delete by document identity.

**Candidate targets, `presumed`:** a lexical index embedded in the graph engine; an external
trigram-based code search service such as **Zoekt** (Apache-2.0); or the `EXT-4` engine.

**This slot has a real consumer only if the graph store cannot rank lexically.** `FR-017` requires a
lexical index; where it lives is a `B3` placement decision. That makes `EXT-5` conditionally required
rather than optional, and it is the one slot whose optionality depends on another decision.

**A specific portability hazard to specify around:** an engine that offers only whole-index create,
drop and query — with no per-document update — forces a full re-tokenisation on every index run, which
directly contradicts `PERF-6`. **The capability profile therefore requires per-document update**, and a
candidate lacking it must be screened out rather than adopted and worked around.

**Verification:** `COR-6`, including an incremental case asserting that updating one document does not
re-tokenise the corpus.

### EXT-6 — The key-value slot MAY be provided by an external key-value store. *(assumed)*

**SHOULD.** Optional. Capability profile: get, set with expiry, delete, and a compare-and-set primitive
if it is used for coordination.

**Candidate targets, `presumed`:** an in-process map; a networked key-value server.

**No required capability consumes this slot** (`GAP-011`). If it is used for coordination rather than
caching, the compare-and-set requirement becomes load-bearing and the slot stops being optional.

**Verification:** if implemented, `COR-6`.

### EXT-7 — The embedding provider MUST be selectable, and MUST be reachable in a restricted network. *(VERIFIED)*

**MUST.** Capability profile: accept a batch of texts, return fixed-width vectors, report its model
identity and vector width.

**MUST also:**

1. **Provider identity MUST be recorded with the vectors.** Two providers' vectors are not
   comparable, and mixing them silently degrades every semantic result.
2. **A private certificate authority MUST be supportable.** An internal inference endpoint behind a
   private CA is the expected deployment here.
3. **No model artefact may be fetched from a public network at first use** in a deployment that
   declares itself restricted. A provider whose weights download on demand is unusable in that
   posture.
4. **A misconfiguration MUST fail loudly.** Where a provider is configured but unusable, semantic
   ranking MUST report itself absent (`FR-021`), never return zero results silently.

**Why this is evidenced:** the grounding recorded, in prior art, a remote-provider client with no
private-CA story at all, a model downloaded from a public host at runtime with no vendored weights,
and a configuration error path that **swallowed** the resulting failure so semantic search returned
zero results with no diagnostic. Each of the four clauses above corresponds to one of those.

**Verification:** a provider fixture behind a private CA; a restricted-network test asserting no
outbound fetch to any host other than the configured provider; and a fault-injection test asserting the
loud-failure path.

### EXT-8 — Every external system's licence MUST permit internal commercial use, and a copyleft store MUST be reached at arm's length. *(VERIFIED)*

**MUST.** This requirement is the reason the project exists, so it is enforced rather than assumed.

1. No dependency may restrict internal commercial use. A licence enumerating permitted purposes that
   exclude a for-profit organisation is disqualifying — that is precisely the constraint that blocked
   the reference implementation.
2. A store under a network-triggered or strong copyleft licence MUST be reached **over its network
   protocol as a separate process**, never linked. Several credible graph and search engines are
   copyleft or source-available; arm's-length separation is the normal and defensible posture, and
   linking one would be a different question entirely.
3. Source-available licences with an internal-use grant MUST be assessed per grant, not by category.
   Several bar offering the product to third parties while permitting internal production use, and
   at least one bars feeding the product's output to AI systems — which would disqualify it for this
   use case specifically, whatever its other terms say.

**Verification:** a licence inventory is generated and gated in CI (`QA-14`). A new dependency with an
unreviewed licence fails the build. This is not a one-time review, because the failure mode is a
transitive dependency added later.

### EXT-9 — Every candidate backend MUST be screened for an async-only client before adoption. *(operational)*

**MUST.** House rule: if any candidate backend is async-only, the store trait is async and everything
above it inherits that. **Resolve during screening, never after** — retrofitting async through a
synchronous trait is a rewrite.

**Verification:** the screening record for each slot states, per candidate, whether its client is
synchronous, asynchronous, or both. `analysis/0004-store-capability-matrix.md` holds the record;
`questions/0003` holds the decision; sync **B7** owns it.

### EXT-10 — Identity MUST be obtainable from an external provider. *(assumed)*

**MUST.** OAuth2 or JWT, per the capability list. See `SEC-1`, `SEC-2`.

**Verification:** an identity-provider fixture; tokens are validated including expiry, audience and
issuer, and a rejected token yields a denial rather than an anonymous success.

### EXT-11 — Authorisation MAY be delegated to an external decision point. *(assumed)*

**SHOULD.** RBAC, ABAC or ReBAC, per the capability list. See `SEC-4`, `SEC-5`.

**MUST:** when the external decision point is unreachable, the request is **denied** (`SEC-7`). A
policy engine timing out MUST NOT become an allow.

**Verification:** fault-injection against the decision point asserts denial, with a positive control
proving the same request is allowed when it is reachable.

### EXT-12 — Repository remotes MUST be reachable over the transports the organisation uses. *(assumed)*

**MUST.** Applies to the service shape. Requirements that fall out of `FR-045` and `FR-046`:

1. **Internal hosts MUST be reachable by hostname.** A guard that admits only public hosts makes the
   service useless here.
2. **That admission is also an outbound-request risk**, since a caller-supplied location becomes a
   server-side fetch. Admission MUST be by an operator-configured allowlist, never by a caller-supplied
   flag, and the allowlist MUST be a fixed server-side set.
3. **Credential conventions differ per host type.** The username half of a basic credential is not
   universal, so the credential format MUST be configurable per allowlisted host rather than hardcoded.
4. **A transport the organisation requires but the platform lacks MUST be recorded as a gap**, not
   worked around by weakening (1) or (2).

**Verification:** an allowlist fixture with an internal hostname; a non-allowlisted host is refused;
a caller-supplied parameter cannot extend the allowlist. Asserted, since the failure is a bypass.

### EXT-13 — Telemetry MUST be exportable to an external collector. *(operational)*

**MUST.** In the service shape. See `OPS-1`. The protocol is a `D1` decision; that it is exportable
rather than only local is the requirement.

**Verification:** signals arrive at a collector fixture.

## Verification

### What is proven

- **All six store slots from the capability list are specified**, each as a capability profile with
  candidate targets marked `presumed`.
- **Product names are confined to this file.** No requirement in any other SPEC file names a product;
  checkable by grep.
- **Six inherited negatives are carried by the interface half** — `IF-1`, `IF-3`, `IF-4`, `IF-8`,
  `IF-9`, plus `EXT-7` — each tagged and each with the measured failure named.
- **`EXT-1`, `EXT-5` and `EXT-7` each specify around a measured portability or deployment hazard**
  rather than only naming the slot: dialect divergence beyond `MATCH`, absence of per-document
  lexical update, and runtime model fetching.
- **Two slots are flagged as having no consumer** (`EXT-4`, `EXT-6`), consistent with
  `analysis/0001`'s store cross-tabulation.

### What is NOT proven

- **The candidate products are `presumed`, not confirmed.** The requester's original per-slot list did
  not survive into the trigger prompt (`questions/0010`). Every product named here is the requirements
  author's inference from this estate and from a licence-screened survey.
- **No candidate has been screened for async**, so `EXT-9` is currently a procedure with no results and
  `questions/0003` cannot be answered from this file.
- **`EXT-1`'s capability profile has not been checked against any real engine.** In particular, whether
  a single contract can span an embedded engine and a networked one without leaking either is the
  central bet of the whole storage abstraction, and it is unverified.
- **`EXT-5`'s optionality is unresolved.** It is optional if the graph store ranks lexically and
  required if it does not, and that is a `B3` placement decision.
- **The web-UI contract has no counterpart.** No UI exists, so the declared query set in `IF-11` has
  nobody to declare it. Until it does, `PERF-4` is unenforceable.
- **`IF-14` is a recorded absence, not a decision.** If the TUI is wanted, this file is currently
  wrong rather than incomplete.

## Amendments

- **2026-08-20** — Created. Candidate store products recorded as `presumed` per the requester's
  decision of the same date.

## Related

- `analysis/0004-store-capability-matrix.md` — the slots as a comparison matrix, plus the async screening record.
- [`05-security-requirements.md`](05-security-requirements.md) — `SEC-*`, which `IF-3`, `IF-8`, `IF-9`, `IF-13` and `EXT-10`–`EXT-12` depend on.
- `questions/0003-the-async-decision.md` · `questions/0008-embedding-provider-and-vector-width.md` · `questions/0009-is-a-tui-wanted.md` · `questions/0010-store-compatibility-targets.md`
