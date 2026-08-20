# Glossary — ratified vocabulary

- **Date:** 2026-08-20 · **Status:** ratified for the requirements corpus; extend by dated amendment
- **Gate:** this document satisfies sync **A2**, and it was written **before** any SPEC prose. Every
  later document in this plan uses these terms and no synonyms.

## Why this is second, not last

A glossary written last summarises whatever vocabulary happened to emerge, which is why glossaries
are usually useless. One written second is a **constraint the SPEC must satisfy**. The hardest case
already existed before a line of the SPEC was drafted: *"impact analysis"* looks like one capability
and is a category containing four distinct terms (`discussions/0001`).

**Three renames are deliberate and load-bearing.** Where the requester's capability list uses a term
this glossary replaces, the original is recorded as an alias so nothing is lost in translation.

## Analysis vocabulary — the four terms that replace "impact analysis"

Adopted from `discussions/0001-what-impact-analysis-means.md`. **The phrase "impact analysis" appears
in no requirement in this corpus**, because it names a category rather than a capability.

| Term | Means | Input | Output |
|---|---|---|---|
| **Reachability** | Whether a path exists from A to B under a stated edge set. | Two symbols, an edge set, a depth bound | Yes/no plus a **witness path**, or *undetermined* |
| **Blast radius** | The set reachable *from* a change, walking **upstream** ("what might break"). | One or more symbols, an edge set, a depth bound | A set of affected elements per projection, or *undetermined* |
| **Dependence** | Statement-level control and data dependence, within and across procedures. A different index and a different question. | A statement, or a source and a sink | Dependence edges, or persisted source-to-sink findings |
| **Diff impact** | Blast radius whose **input is a change set** rather than a symbol. A projection over blast radius, **not a separate mechanism**. | A change set (see *change set input*) | The blast-radius output, projected |

**Downstream reachability** — "what do I reach, what must exist for this to work" — is the opposite
direction from blast radius and serves comprehension rather than change safety. Where direction
matters, requirements say **upstream** or **downstream** explicitly and never rely on "impact" to
imply one.

## The three-state result contract

Non-negotiable, and used by every analysis capability that walks the graph:

| State | Means | May be claimed when |
|---|---|---|
| **affected** | A positive result — here is the set. | Always, when the set is non-empty |
| **none affected** | A genuine negative. | **Only** where the walk was complete under the stated edge set and depth |
| **undetermined** | The walk was truncated, degraded, or met a construct it cannot follow. | Whenever completeness cannot be asserted |

- **Truncation** — the walk stopped because a budget was exhausted. There may be more. **This is not an answer.**
- **Completeness** — the walk exhausted the stated edge set within the stated depth. *"We assert nothing beyond depth N"* is a correctness statement; *"we stopped at N"* is a budget. They must be distinguishable in the output.
- **Witness** — the concrete path that justifies a positive reachability answer. A positive result without a witness is unverifiable by its consumer.

## Graph vocabulary

| Term | Means |
|---|---|
| **Repository** | One version-controlled source tree, identified by a stable **repository identity** independent of its filesystem location. |
| **Indexed repository** | A repository for which an index exists. Registered, discoverable, and addressable by identity. |
| **Repository group** | A named set of repositories analysed together so that cross-repository relationships can be established. |
| **Contract registry** | The record of declared interfaces between repositories in a group — the evidence from which **cross-repository edges** are inferred. |
| **Symbol** | A named code element the graph can address: a function, method, class, interface, type, constant, module, and so on. The authoritative list of symbol kinds is a data-model decision, not a glossary one. |
| **Node** | A vertex of the knowledge graph. A symbol is one kind of node; files, routes, declared contracts and **derived structures** are others. |
| **Edge** | A directed, typed relationship between two nodes, carrying at minimum its **edge class**, its direction, and its **evidence class**. |
| **Edge class** | The kind of relationship — call, import, inheritance, interface implementation, override, framework wiring, route-to-handler, data flow, test-to-subject, cross-repository contract link. Edge classes are selected per query; see **edge set**. |
| **Edge set** | The explicit set of edge classes admitted by a particular traversal. Every reachability, blast-radius and diff-impact result states the edge set it was computed under. |
| **Evidence class** | Whether an edge was **observed** in code or **inferred** from a declaration. A contract-inferred cross-repository edge is weaker evidence than a call read from a syntax tree, and a consumer must be able to tell which it received. |
| **Knowledge graph** | The whole node-and-edge structure for one repository or group. |
| **Index** | Everything persisted for a repository so that it can be queried without re-reading source: the graph, plus vectors, plus lexical indexes, plus derived structures. |
| **Index generation** | A monotonically increasing marker identifying one completed analysis run's output, so a consumer can tell whether two answers came from the same index. |
| **Staleness** | The relationship between an index and the current source. An index is **fresh** when it reflects the current commit and a clean working tree, and **stale** otherwise. Staleness is a first-class field of a response, not a log line. |
| **Torn read** | Observing a mixture of two index generations in one answer. Distinct from staleness: a stale answer is consistently old; a torn answer is internally inconsistent and is always a defect. |

## Derived structures

| Term | Means | Alias it replaces |
|---|---|---|
| **Flow** (execution flow) | An ordered chain of symbols representing one end-to-end path of execution, derived from the graph rather than declared in source. | The capability list's **"process"** |
| **Cluster** | A group of nodes derived by a whole-graph partitioning algorithm, intended to name a cohesive area of the codebase. | "community", "functional area" |
| **Derived structure** | Any node or edge produced by computation over the whole graph rather than extracted from a single file. Flows and clusters are the two required kinds. | — |
| **Derived identity** | The identifier of a derived structure. Whether these must be **stable across runs** is an open decision (`questions/0004`) — and it is a correctness question, not a performance one, because a derived identifier that is part of the query surface changes *answers* when it churns. | — |

**Why "flow" and not "process".** This corpus specifies two deployment shapes, concurrency
properties, and job execution. In that document, "process" already means an operating-system
process, and a reader cannot tell which sense is meant from context. The rename is not cosmetic: it
removes a genuine ambiguity from the requirements that a reader would otherwise have to resolve by
guessing.

## Data ownership vocabulary

| Term | Means |
|---|---|
| **Authoritative data** | Data that cannot be reconstructed from source and must therefore be migrated across version upgrades. |
| **Derived data** | Data rebuildable from source or from authoritative data. May be dropped and recomputed; must never be the only copy of anything. |
| **System of record** | The store whose contents win when two stores disagree. Naming it is a B4 decision; requirements here only insist that exactly one exists and that it is named. |
| **Placement** | Which store owns a given kind of data, and why. |

## Search and ranking vocabulary

| Term | Means |
|---|---|
| **Lexical ranking** | Ranking by term match, of the BM25 family. |
| **Semantic ranking** | Ranking by vector similarity between an embedded query and embedded code. |
| **Rank fusion** | Combining two or more ranked lists into one. Its parameters and its **join key** are part of the contract, and there must be exactly one implementation of it in the system. |
| **Join key** | The identity on which two ranked lists are merged. Two fusion implementations using different join keys produce different answers to the same query — which is why the join key is specified rather than assumed. |
| **Hybrid search** | A query answered by combining graph traversal, lexical ranking and semantic ranking through rank fusion, with results grouped by **flow**. |
| **Embedding** | A vector representation of a unit of code. |
| **Vector width** | The dimensionality of an embedding. A property of the **embedding provider**, frozen into the vector store at creation, and therefore a migration event when it changes (`questions/0008`). |
| **Embedding provider** | The service or local runtime that turns text into vectors. Selectable by configuration, and — where an administrator permits it — at runtime. |

## Store slots

Six store kinds, each of which must be swappable between an **embedded** and a **networked**
implementation without changing business logic. The slot is the requirement; the product is a
compatibility target (`specs/04`, `analysis/0004`).

| Slot | Holds |
|---|---|
| **Graph store** | Nodes and edges; serves traversal and openCypher-style queries. |
| **Vector store** | Embeddings; serves nearest-neighbour search. |
| **Relational store** | Registries, metadata, job state, audit records — anything relational. |
| **Search index** | Optional external general-purpose search. |
| **Text-search index** | Optional external lexical/full-text ranking. |
| **Key-value store** | Optional; ephemeral and derived data, caches, coordination. |

**Embedded** means in-process, single-host, no network hop, no separate operator. **Networked** means
a separate service reached over the network, with its own lifecycle and its own failure modes.

## Deployment shapes

| Term | Means |
|---|---|
| **Local shape** | A single binary on a developer's machine. Embedded stores, one user, no authentication, no network exposure. |
| **Service shape** | A Kubernetes-native deployment. External stores, authenticated per principal, serving roughly 20–50 humans and up to about 10 000 predominantly read-only agents. |
| **Deployment duality** | The requirement that these are **two points a single design must reach**, not two configurations of one design. Which requirements apply to which shape is stated per requirement (`analysis/0005`). |
| **Replica** | One serving instance in the service shape. Concurrency requirements are stated **per replica**, so that horizontal scaling is a capacity decision rather than a correctness one. |

## Identity vocabulary

| Term | Means |
|---|---|
| **Principal** | The authenticated identity on whose behalf a request is made. A human, or one agent — never a group, and never a shared secret's bearer. |
| **Attribution** | The property that every request can be traced to exactly one principal. Requires per-principal identity to survive every hop, not merely to be checked at one. |
| **Audit record** | A durable record of a security-relevant or mutating action, naming its principal, its target, its outcome and its time. |
| **Agent** | A non-human automated consumer. Distinguished from a human principal because its request profile, budget sensitivity and error tolerance all differ. |
| **Fail closed** | On any failure to establish authorisation, the request is denied. The opposite — unset configuration authorising everything — is specified against. |

## Surfaces

| Term | Means |
|---|---|
| **CLI** | The `git-ctx` command-line surface. `git-ctx` is a decided name, not a placeholder. |
| **API** | The programmatic network interface of the service shape. |
| **MCP surface** | The agent-facing protocol surface: a tool inventory, session semantics and output budgeting. |
| **Web UI** | The browser surface. **A downstream consumer specified by contract**; its implementation technology is deliberately unchosen. |
| **TUI** | A terminal user interface. Arrived after the capability list and is unspecified — see `GAP-001` and `questions/0009`. |
| **Advertised inventory** | The set of tools or endpoints a surface declares. A surface whose **callable** set exceeds its advertised set cannot be governed by an allowlist built from the advertisement, so the two must be identical. |

## Work vocabulary

| Term | Means |
|---|---|
| **Analysis run** | One end-to-end execution that produces or updates an index. |
| **Indexing job** | A durable, addressable, cancellable unit of work representing an analysis run, with observable status. |
| **Queue** | An ordered backlog of admitted jobs. Distinct from a **slot**, which admits one and rejects the rest — a status value of "queued" that never corresponds to a backlog is a mislabelled rejection. |
| **Incrementality** | Doing work proportional to what changed rather than to the size of the repository. Its granularity, and the point at which the incremental-versus-full decision is taken, are both specified. |
| **Change detection** | Determining what changed, **before** committing to the expensive work. |
| **Change set input** | How a change is supplied: a working tree, a pair of refs (`base...head`), or a **supplied patch** for a repository the system has never checked out. The last is what a pull-request integration requires. |
| **Escalation** | Abandoning the incremental path for a full rebuild. Every escalation condition must be enumerable and observable, because a silent escalation reads as an incrementality feature that does not work. |

## Naming placeholders

| Written | Means |
|---|---|
| `git-ctx` | The CLI. **Decided** (`questions/0001`); write it literally. |
| `<ENGINE>` | The reusable engine library, **deliberately unnamed** until sync B6 has mapped what is inside it. Left visibly unresolved on purpose; a document that has silently adopted a guessed engine name in half its sections is a defect. |
| **the reference implementation** | The prior-art tool this corpus is a clean-room replacement for. Named only where licence provenance requires it (`specs/06-constraints.md`); never inside a requirement. |

## Terms deliberately not used

| Avoided | Because | Use instead |
|---|---|---|
| "impact analysis" | A category, not a capability. Its use is what let two incompatible mechanisms share one name in the prior art. | reachability · blast radius · dependence · diff impact |
| "process" (for a derived execution chain) | Collides with operating-system process in a document that specifies deployment and concurrency. | **flow** |
| "risk score" | A single number that can read *low* while the underlying walk was truncated. | the three-state result, plus per-projection counts |
| "already indexed" | Ambiguous between *exists* and *fresh*. | **fresh** / **stale**, plus the index generation |
| "supports language X" | Ambiguous between detection, parsing and extraction depth. | state the **extraction depth** achieved for that language |

## Amendments

- **2026-08-20** — Created, satisfying the A2 gate before any SPEC prose. Adopted the four analysis
  terms from `discussions/0001`; renamed the capability list's "process" to **flow** and recorded the
  alias; introduced **evidence class**, **index generation**, **torn read**, **advertised inventory**
  and **change set input** as terms the capability list needed but did not have.

## Related

- `discussions/0001-what-impact-analysis-means.md` — where the four analysis terms come from, and the seven axes behind them.
- `questions/0001-product-and-crate-naming.md` — why `git-ctx` is literal and `<ENGINE>` is not.
- `SYNCS.md` — sync A2, which this document satisfies.
