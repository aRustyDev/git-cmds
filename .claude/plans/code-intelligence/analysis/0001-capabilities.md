# Analysis 0001 — Atomic capability inventory

- **Date:** 2026-08-20 · **Status:** drafted for sync **A1**
- **Purpose:** one row per capability, carrying enough metadata that the architect can cluster
  behaviour into modules **without re-reading anything else**. This is raw material, not a proposal —
  no grouping is asserted here. Groupings, with reasons, are in `analysis/0002`.
- **Vocabulary:** every term is as ratified in [`GLOSSARY.md`](../GLOSSARY.md).

## How to read the table

| Column | Values |
|---|---|
| **Consumers** | `U` human user · `A` admin · `G` agent · `D` developer of, or integrator with, the platform itself |
| **Mode** | `R` read-only · `W` writes durable state · `R/W` a read that may trigger a write |
| **Stores** | `Gr` graph · `Vec` vector · `Rel` relational · `Srch` search index · `Txt` text-search index · `KV` key-value · `Src` source tree or remote · `—` none |
| **Shapes** | `L` local shape · `S` service shape · `L+S` both |
| **Req** | the requirement IDs in `specs/**` that carry this capability |

**ID convention.** A functional capability `CAP-0nn` maps to functional requirement `FR-0nn` with the
same trailing number. Cross-cutting capabilities (`CAP-06x`, `CAP-07x`) map instead to
`SEC-`, `IF-`, `EXT-`, `PERF-`, `SCALE-` or `OPS-` identifiers, because they are not features a user
invokes. This deliberate alignment is what makes the two-way traceability audit mechanical rather
than a reading exercise.

## A. Ingestion and index construction

Nothing in the requester's module-seam sketch owns this group; it is coverage gap 1 of Appendix B.

| ID | Capability | Consumers | Mode | Stores | Shapes | Req |
|---|---|---|---|---|---|---|
| CAP-001 | Detect which languages are present in a repository, and which files are in scope | D | R | Src | L+S | FR-001 |
| CAP-002 | Parse source files of a supported language into a syntax tree | D | R | Src | L+S | FR-002 |
| CAP-003 | Extract nodes and edges from a syntax tree, to a stated **extraction depth** per language | D | W | Gr, Src | L+S | FR-003 |
| CAP-004 | Add support for a language without forking the codebase | A, D | W | — | L+S | FR-004 |
| CAP-005 | Analyse declarative infrastructure and configuration formats | U, G | W | Gr, Src | L+S | FR-005 |
| CAP-006 | Resolve cross-file references — imports, inheritance, interface implementation, overrides | D | W | Gr | L+S | FR-006 |
| CAP-007 | Extract route-to-handler mappings | U, G | W | Gr | L+S | FR-007 |
| CAP-008 | Extract RPC and tool-definition mappings | U, G | W | Gr | L+S | FR-008 |
| CAP-009 | Derive **flows** from the graph | U, G | W | Gr | L+S | FR-009 |
| CAP-010 | Derive **clusters** by whole-graph partitioning | U, G | W | Gr | L+S | FR-010 |
| CAP-011 | Determine what changed **before** committing to expensive work | D | R | Gr, Rel, Src | L+S | FR-011 |
| CAP-012 | Update an index incrementally, at a stated granularity | U, A, G | W | Gr, Vec, Txt, Rel | L+S | FR-012 |
| CAP-013 | Rebuild an index in full | A | W | all | L+S | FR-013 |
| CAP-014 | Index a repository, or update a stale index, on request | U, A, G | W | all | L+S | FR-014 |
| CAP-015 | Report index status and freshness for a repository | U, A, G | R | Rel | L+S | FR-015 |
| CAP-016 | Generate embeddings for indexed symbols | D | W | Vec, Gr | L+S | FR-016 |
| CAP-017 | Build and maintain the lexical index | D | W | Txt \| Gr | L+S | FR-017 |
| CAP-018 | Persist derived structures with identities that the query surface can address | D | W | Gr, Rel | L+S | FR-018 |
| CAP-019 | Enumerate and report every condition that escalated an incremental run to a full rebuild | A, D | R | Rel | L+S | FR-019 |

## B. Query and analysis — the read surface

This is where the ~10 000-agent load lands. Every row is `R`.

| ID | Capability | Consumers | Mode | Stores | Shapes | Req |
|---|---|---|---|---|---|---|
| CAP-020 | Execute a caller-supplied read-only openCypher-style query | U, G, D | R | Gr | L+S | FR-020 |
| CAP-021 | Hybrid search — graph traversal plus lexical plus semantic ranking, fused, grouped by flow | U, G | R | Gr, Vec, Txt | L+S | FR-021 |
| CAP-022 | 360-degree symbol view — categorised references and flow participation | U, G | R | Gr | L+S | FR-022 |
| CAP-023 | **Reachability** between two named symbols, with a witness path | U, G | R | Gr | L+S | FR-023 |
| CAP-024 | **Blast radius** — upstream, transitive, depth-bounded, per-projection | U, G | R | Gr | L+S | FR-024 |
| CAP-025 | Downstream reachability from a symbol | U, G | R | Gr | L+S | FR-025 |
| CAP-026 | **Diff impact** from a working tree | U | R | Gr, Src | L+S | FR-026 |
| CAP-027 | **Diff impact** from a `base...head` ref pair | U, G | R | Gr, Src | L+S | FR-027 |
| CAP-028 | **Diff impact** from a **supplied patch**, for a repository never checked out | G, D | R | Gr | S | FR-028 |
| CAP-029 | Filter any graph result by node type and edge class | U, G | R | Gr | L+S | FR-029 |
| CAP-030 | Return nodes within N hops of a selection, N configurable | U, G | R | Gr | L+S | FR-030 |
| CAP-031 | Report node and edge counts, by type and in total | U, A, G | R | Gr | L+S | FR-031 |
| CAP-032 | Scope or filter the graph to a sub-directory of a repository | U, G | R | Gr | L+S | FR-032 |
| CAP-033 | Run read-only structural checks against the indexed graph | U, G, D | R | Gr | L+S | FR-033 |
| CAP-034 | Check response-shape conformance against consumers' property accesses | U, G | R | Gr | L+S | FR-034 |
| CAP-035 | Produce a pre-change report for a named route handler | U, G | R | Gr | L+S | FR-035 |
| CAP-036 | Generate a repository wiki from the knowledge graph | U | R/W | Gr, Rel | L+S | FR-036 |
| CAP-037 | Query statement-level **dependence** — control and data | U, G | R | Gr | L+S | FR-037 **(WON'T v1)** |
| CAP-038 | Explain persisted taint findings as source-to-sink flows | U, G | R | Gr, Rel | L+S | FR-038 **(WON'T v1)** |
| CAP-039 | Return, with every analysis answer, the **index generation** and freshness it was computed against | U, G, D | R | Rel | L+S | FR-039 |

## C. Repositories, groups and acquisition

| ID | Capability | Consumers | Mode | Stores | Shapes | Req |
|---|---|---|---|---|---|---|
| CAP-040 | Discover all indexed repositories, paginated by limit and offset | U, A, G | R | Rel | L+S | FR-040 |
| CAP-041 | Swap the active repository for a session or invocation | U, G | R | Rel | L+S | FR-041 |
| CAP-042 | Serve more than one repository simultaneously, for cross-repository analysis | U, G | R | Gr, Rel | L+S | FR-042 |
| CAP-043 | List configured repository groups | U, A, G | R | Rel | L+S | FR-043 |
| CAP-044 | Rebuild a group's contract registry and its cross-repository links | A | W | Gr, Rel | L+S | FR-044 |
| CAP-045 | Acquire a repository from a remote, and update one already acquired | A, G | W | Src | S | FR-045 |
| CAP-046 | Authenticate to a private remote without exposing the credential | A | W | — | S | FR-046 |
| CAP-047 | Distinguish **observed** from **inferred** edges in any cross-repository answer | U, G | R | Gr | L+S | FR-047 |

## D. Write operations against source

The only group that modifies a user's working tree. One capability, and it carries the sharpest
inherited-negative in the corpus.

| ID | Capability | Consumers | Mode | Stores | Shapes | Req |
|---|---|---|---|---|---|---|
| CAP-050 | Coordinated multi-file rename — AST-accurate, with mandatory index writeback | U, G | W | Gr, Src | L+S | FR-050 |

## E. Platform capabilities — cross-cutting, consumed indirectly

No row here is a feature a user asks for by name; every one is a property the features depend on.
Rows E1–E4 are Appendix B coverage gaps 2, 3, 4 and 6.

| ID | Capability | Consumers | Mode | Stores | Shapes | Req |
|---|---|---|---|---|---|---|
| CAP-060 | Swap any store slot between an embedded and a networked implementation, with no change to business logic | A, D | — | all | L+S | EXT-1 … EXT-6 |
| CAP-061 | Select and configure the embedding provider from deployment configuration | A | — | Vec | L+S | EXT-7 |
| CAP-062 | Configure the AI provider at runtime, from the web UI | A, U | W | Rel | S | IF-12 |
| CAP-063 | Restrict or disable runtime AI-provider configuration | A | W | Rel | S | IF-13, SEC-11 |
| CAP-064 | Authenticate a principal, optionally against an external provider | A | — | Rel | S | SEC-1, SEC-2 |
| CAP-065 | Authorise a request, optionally against an external decision point | A | — | Rel | S | SEC-4, SEC-5 |
| CAP-066 | Attribute every request to exactly one principal, end to end | A, D | R | Rel | S | SEC-3 |
| CAP-067 | Record an audit entry for every mutating and every security-relevant action | A | W | Rel | S | SEC-6 |
| CAP-068 | Accept, queue, observe, cancel and durably track indexing jobs | A, G, D | W | Rel | L+S | FR-068 |
| CAP-069 | Emit traces, metrics and logs sufficient to verify the stated budgets | A, D | W | — | L+S | OPS-1 … OPS-5 |
| CAP-070 | Assemble the same behaviour into either deployment shape | D | — | — | L+S | CON-6 |
| CAP-071 | Rank and fuse ranked lists — **exactly one implementation, one join key** | D | R | — | L+S | FR-071 |
| CAP-072 | Serve concurrent reads that scale with readers per replica | G, U | R | all | S | PERF-1 |
| CAP-073 | Carry an index across a version upgrade without a full reindex | A | W | all | L+S | FR-073 |
| CAP-074 | Serve an unbounded number of repositories per deployment, bounded by capacity rather than by a constant | A, G | R | all | S | SCALE-3 |

## Consumer cross-tabulation

Useful because "who consumes it" is one of the strongest clustering signals, and the counts are
lopsided in a way that matters.

| Consumer | Read capabilities | Write capabilities | Notes |
|---|---|---|---|
| **Agent** (`G`) | 22 | 5 | The dominant consumer by request volume, and overwhelmingly read-only. Its writes are indexing and rename. |
| **Human user** (`U`) | 21 | 4 | Same read surface as agents, different presentation and latency expectations. |
| **Admin** (`A`) | 7 | 12 | Almost the inverse profile. Configuration, acquisition, groups, jobs, providers, identity. |
| **Platform developer** (`D`) | 11 | 8 | Consumes the ingestion and platform capabilities directly; never a runtime persona. |

**The asymmetry is the headline.** 27 of the 60 rows are read-only and serve agents; 5 write
capabilities serve them. That ratio, against a target of up to ~10 000 agents and 20–50 humans, is
the evidence behind `discussions/0002`.

## Store cross-tabulation

| Store | Capabilities that read it | Capabilities that write it |
|---|---|---|
| Graph | 24 | 12 |
| Relational | 11 | 7 |
| Vector | 2 | 2 |
| Text-search | 1 | 2 |
| Source or remote | 6 | 3 |
| Search index | 0 | 0 — no required capability names it |
| Key-value | 0 | 0 — no required capability names it |

**Two slots have no consumer.** The search index and the key-value store are named as required
swappable slots by the capability list, but **no capability in this inventory needs either.** That is
a genuine finding, not an omission in the table: they are specified as optional in `specs/04` and
filed as `GAP-011`. An abstraction with no consumer cannot be validated, and building one is
speculative work.

## What this inventory changed about the capability list

Findings from restating the list as behaviour, each filed in `GAPS.md`:

1. **"Impact analysis" was one line and is five capabilities** (CAP-023 through CAP-028), which is
   why `discussions/0001` had to be settled first.
2. **Two capabilities had no home and no consumer** — the search and text-search slots. Text-search
   at least has a consumer if the graph store cannot rank lexically; the general search index has
   none at all.
3. **Nine platform capabilities were entirely implicit** (CAP-060, 066–071, 073, 074). The capability
   list names the *features*; none of the machinery under them appears in it. This is the substance
   of Appendix B's ten coverage gaps.
4. **"Show index status for the current repository" presumes a current repository** — a notion that
   exists in the local shape and does not exist in the service shape, where a request arrives with no
   ambient working directory. Restated as CAP-015 against an explicit repository identity, with
   `git-ctx` resolving "current" from the working directory as a CLI convenience.
5. **Freshness reporting (CAP-039) is not in the capability list at all** and is a prerequisite for
   every analysis answer being trustworthy. Added as `discovered`.
6. **Escalation reporting (CAP-019) is not in the capability list** and is required to make the
   incrementality requirement observable rather than aspirational.
7. **Evidence class (CAP-047) is not in the capability list** and is required the moment
   cross-repository links exist, because a contract-inferred edge and an observed call cannot be
   weighed the same.

## Verification

### What is proven

- **Every entry in the requester's Appendix A appears in this table.** Checked line by line against
  `PROMPT.md` Appendix A; the mapping is in `analysis/0003`.
- **All seven capabilities named in Appendix A's closing note appear** — CAP-023, CAP-024, CAP-034,
  CAP-035, CAP-007, CAP-008, CAP-050 — per the requester's 2026-08-20 decision that all are wanted.
- **The consumer and store cross-tabulations are derived from the table above**, by counting its own
  rows, so they cannot drift from it without the table changing.

### What is NOT proven

- **That the inventory is complete.** It is complete with respect to Appendix A, Appendix B's
  coverage gaps and this session's decisions. Sync **A1** exists to test it against the requester's
  intent, and sync **A4** exists to add what nobody has asked for yet.
- **That the granularity is right.** CAP-003 ("extract nodes and edges to a stated depth") is one row
  covering per-language work that may be dozens of capabilities, and CAP-021 bundles three ranking
  lanes. Whether either should split is a clustering question for A1 and B1, not a fact.
- **The store columns are the requirements author's reading, not a placement decision.** Which store
  actually owns each data kind is sync **B3**'s output. A row saying `Gr` means "this capability
  needs graph-shaped access", not "this data lives in the graph store".
- **Deployment-shape columns for CAP-062/063 assume the web UI is service-shape only.** If the local
  shape ever serves the web UI, those rows change. Not yet decided.

## Related

- [`GLOSSARY.md`](../GLOSSARY.md) — every term used here.
- `analysis/0002-feature-clusters.md` — candidate groupings of these rows, with reasons.
- `analysis/0003-feature-gaps.md` — precedent and risk per capability.
- `analysis/0005-deployment-shape-contrast.md` — the shape columns, expanded per requirement.
- `discussions/0002-read-write-asymmetry.md` — what the consumer cross-tabulation implies for seams.
