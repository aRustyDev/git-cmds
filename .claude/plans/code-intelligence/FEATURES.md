# Features — flat list, traceable both ways

- **Date:** 2026-08-20 · **Vocabulary:** [`GLOSSARY.md`](GLOSSARY.md)
- **Purpose:** the flat feature list the external SRS reference calls for, and the traceability
  artefact sync **A3** checks. **A3's question is not "have we found everything?" — that is A1. It is
  "do the feature list and the requirement set describe the same system?"**
- **Both directions are asserted:** every feature names at least one requirement, and every requirement
  is named by at least one feature. The reverse index below is the second half, and the corpus audit
  verifies set equality rather than trusting either table.

## How to read this

| Column | Values |
|---|---|
| **Priority** | `MUST` · `SHOULD` · `WON'T` — the strongest priority among the requirements the feature carries |
| **Consumers** | `U` user · `A` admin · `G` agent · `D` platform developer |
| **Shape** | `L` local · `S` service · `L+S` both |
| **CAP** | the capability rows in `analysis/0001-capabilities.md`, where the mapping is direct |

A feature marked **inherited-negative** carries at least one requirement that exists because a failure
was measured rather than imagined.

## Ingestion

| ID | Feature | Priority | Consumers | Shape | Requirements | CAP |
|---|---|---|---|---|---|---|
| FEAT-001 | Language detection and scope resolution | MUST | D | L+S | `FR-001` | CAP-001 |
| FEAT-002 | Per-language parsing, resilient to malformed and hostile input | MUST | D | L+S | `FR-002`, `COR-7`, `QA-5` | CAP-002 |
| FEAT-003 | Per-language extraction with a declared, generated extraction depth | MUST | D | L+S | `FR-003`, `QA-6`, `QA-16` | CAP-003 |
| FEAT-004 | Language extensibility without a fork | MUST | A, D | L+S | `FR-004`, `CON-10`, `QA-6` | CAP-004 |
| FEAT-005 | Declarative infrastructure and configuration analysis | SHOULD | U, G | L+S | `FR-005` | CAP-005 |
| FEAT-006 | Cross-file reference resolution | MUST | D | L+S | `FR-006` | CAP-006 |
| FEAT-007 | Route-to-handler and RPC/tool-definition mapping | MUST | U, G | L+S | `FR-007`, `FR-008` | CAP-007, CAP-008 |
| FEAT-008 | Flow and cluster derivation, with addressable identities | MUST | U, G | L+S | `FR-009`, `FR-010`, `FR-018`, `COR-3` | CAP-009, CAP-010, CAP-018 |

## Index lifecycle

| ID | Feature | Priority | Consumers | Shape | Requirements | CAP |
|---|---|---|---|---|---|---|
| FEAT-009 | Change detection ahead of the expensive work — **inherited-negative** | MUST | D | L+S | `FR-011`, `PERF-6`, `OPS-3` | CAP-011 |
| FEAT-010 | Incremental index update, equal to a full rebuild — **inherited-negative** | MUST | U, A, G | L+S | `FR-012`, `COR-2` | CAP-012 |
| FEAT-011 | Deliberate full rebuild | MUST | A | L+S | `FR-013` | CAP-013 |
| FEAT-012 | Index-or-update on request | MUST | U, A, G | L+S | `FR-014` | CAP-014 |
| FEAT-013 | Index status, and freshness on every answer | MUST | U, A, G | L+S | `FR-015`, `FR-039`, `OPS-4` | CAP-015, CAP-039 |
| FEAT-014 | Escalation reporting — **inherited-negative** | MUST | A, D | L+S | `FR-019` | CAP-019 |
| FEAT-015 | Embedding generation and lexical index maintenance | MUST | D | L+S | `FR-016`, `FR-017` | CAP-016, CAP-017 |

## Query and analysis

| ID | Feature | Priority | Consumers | Shape | Requirements | CAP |
|---|---|---|---|---|---|---|
| FEAT-016 | Read-only graph query | MUST | U, G, D | L+S | `FR-020` | CAP-020 |
| FEAT-017 | Hybrid search with one fusion implementation — **inherited-negative** | MUST | U, G | L+S | `FR-021`, `FR-071`, `COR-5` | CAP-021, CAP-071 |
| FEAT-018 | 360-degree symbol view | MUST | U, G | L+S | `FR-022` | CAP-022 |
| FEAT-019 | Reachability with a witness path | MUST | U, G | L+S | `FR-023` | CAP-023 |
| FEAT-020 | Blast radius — bounded, projected, three-state | MUST | U, G | L+S | `FR-024`, `PERF-5`, `COR-1` | CAP-024 |
| FEAT-021 | Downstream reachability | MUST | U, G | L+S | `FR-025` | CAP-025 |
| FEAT-022 | Diff impact from a working tree, a ref pair, or a supplied patch — **inherited-negative** | MUST | U, G, D | L+S | `FR-026`, `FR-027`, `FR-028` | CAP-026, CAP-027, CAP-028 |
| FEAT-023 | Filtering, N-hop neighbourhoods, counts and sub-directory scoping | MUST | U, A, G | L+S | `FR-029`, `FR-030`, `FR-031`, `FR-032` | CAP-029–CAP-032 |
| FEAT-024 | Read-only structural checks | MUST | U, G, D | L+S | `FR-033` | CAP-033 |
| FEAT-025 | Response-shape conformance and the route pre-change report | MUST | U, G | L+S | `FR-034`, `FR-035` | CAP-034, CAP-035 |
| FEAT-026 | Repository wiki | MUST | U | L+S | `FR-036` | CAP-036 |
| FEAT-027 | Dependence and taint — deferred, with the seam named | WON'T | U, G | L+S | `FR-037`, `FR-038` | CAP-037, CAP-038 |

## Repositories, groups and acquisition

| ID | Feature | Priority | Consumers | Shape | Requirements | CAP |
|---|---|---|---|---|---|---|
| FEAT-028 | Repository discovery, pagination and explicit addressing | MUST | U, A, G | L+S | `FR-040`, `FR-041`, `IF-7` | CAP-040, CAP-041 |
| FEAT-029 | Simultaneous multi-repository serving — **inherited-negative** | MUST | U, G | L+S | `FR-042`, `SCALE-3` | CAP-042, CAP-074 |
| FEAT-030 | Repository groups and the contract registry | MUST | U, A, G | L+S | `FR-043`, `FR-044` | CAP-043, CAP-044 |
| FEAT-031 | Evidence class on cross-repository edges | MUST | U, G | L+S | `FR-047` | CAP-047 |
| FEAT-032 | Repository acquisition and credential handling | MUST | A, G | S | `FR-045`, `FR-046`, `EXT-12`, `SEC-10`, `SEC-12` | CAP-045, CAP-046 |

## Write operations

| ID | Feature | Priority | Consumers | Shape | Requirements | CAP |
|---|---|---|---|---|---|---|
| FEAT-033 | Coordinated rename — AST-accurate, with index writeback — **inherited-negative** | MUST | U, G | L+S | `FR-050` | CAP-050 |

## Work management

| ID | Feature | Priority | Consumers | Shape | Requirements | CAP |
|---|---|---|---|---|---|---|
| FEAT-034 | Durable, queued, cancellable indexing jobs — **inherited-negative** | MUST | A, G, D | L+S | `FR-068`, `SCALE-5` | CAP-068 |

## Storage abstraction

| ID | Feature | Priority | Consumers | Shape | Requirements | CAP |
|---|---|---|---|---|---|---|
| FEAT-035 | Graph slot, embedded or networked | MUST | A, D | L+S | `EXT-1` | CAP-060 |
| FEAT-036 | Vector slot and embedding-provider selection | MUST | A, D | L+S | `EXT-2`, `EXT-7` | CAP-060, CAP-061 |
| FEAT-037 | Relational slot — and the home of all authoritative data | MUST | A, D | L+S | `EXT-3` | CAP-060 |
| FEAT-038 | Optional search, text-search and key-value slots | SHOULD | A, D | L+S | `EXT-4`, `EXT-5`, `EXT-6` | CAP-060 |
| FEAT-039 | Swappability guarantees — conformance, no leaked types, export, rebuildability, async screening | MUST | D | L+S | `COR-6`, `REV-1`, `REV-2`, `REV-3`, `REV-4`, `EXT-9`, `QA-7`, `QA-17` | CAP-060 |

## Surfaces

| ID | Feature | Priority | Consumers | Shape | Requirements | CAP |
|---|---|---|---|---|---|---|
| FEAT-040 | One internal contract behind every surface — **inherited-negative** | MUST | U, A, G, D | L+S | `IF-1`, `IF-2`, `IF-10`, `COR-5`, `QA-9` | — |
| FEAT-041 | Agent surface: advertised equals callable, bounded output, per-request scoping — **inherited-negative** | MUST | G | L+S | `IF-4`, `IF-5`, `IF-6`, `IF-8`, `IF-9`, `QA-18` | — |
| FEAT-042 | Web-UI contract and its budget | MUST | U | S | `IF-11`, `PERF-4`, `QA-8` | — |
| FEAT-043 | AI-provider configuration, restrictable to absence | MUST | A, U | S | `IF-12`, `IF-13`, `SEC-11` | CAP-062, CAP-063 |
| FEAT-044 | Terminal surface — not specified | WON'T | U | L | `IF-14` | — |

## Security

| ID | Feature | Priority | Consumers | Shape | Requirements | CAP |
|---|---|---|---|---|---|---|
| FEAT-045 | Per-principal identity, terminating in one place — **inherited-negative** | MUST | A, D | S | `SEC-1`, `SEC-2`, `SEC-3`, `IF-3`, `EXT-10` | CAP-064, CAP-066 |
| FEAT-046 | Authorisation, optionally external, with a specified unit | MUST | A | S | `SEC-4`, `SEC-5`, `SEC-8`, `EXT-11` | CAP-065 |
| FEAT-047 | Audit trail | MUST | A | S | `SEC-6` | CAP-067 |
| FEAT-048 | Fail closed — **inherited-negative** | MUST | A, D | S | `SEC-7` | — |
| FEAT-049 | Abuse bounding, transport policy and query privacy | MUST | A | S | `SEC-9`, `SEC-13`, `SEC-14`, `SEC-15`, `SEC-16`, `SEC-17` | — |

## Performance, concurrency and consistency

| ID | Feature | Priority | Consumers | Shape | Requirements | CAP |
|---|---|---|---|---|---|---|
| FEAT-050 | Reads that scale with readers per replica — **inherited-negative** | MUST | U, G | S | `PERF-1`, `SCALE-2`, `SCALE-4`, `OPS-2` | CAP-072 |
| FEAT-051 | Interactive latency budgets, per shape | MUST | U, G | L+S | `PERF-2`, `PERF-3` | — |
| FEAT-052 | Scale targets and a gated build baseline | MUST | A, D | L+S | `PERF-7`, `SCALE-1`, `QA-10` | — |
| FEAT-053 | Generation isolation — no torn reads | MUST | U, G | L+S | `COR-4` | — |

## Operability and lifecycle

| ID | Feature | Priority | Consumers | Shape | Requirements | CAP |
|---|---|---|---|---|---|---|
| FEAT-054 | Telemetry sufficient to verify the budgets | MUST | A, D | S | `OPS-1`, `OPS-5`, `OPS-6`, `OPS-7`, `EXT-13` | CAP-069 |
| FEAT-055 | Upgrade without a full reindex — **inherited-negative** | MUST | A | L+S | `FR-073`, `QA-12` | CAP-073 |
| FEAT-056 | Deployment-shape assembly by composition | MUST | D | L+S | `CON-2`, `CON-6`, `REV-5`, `QA-9` | CAP-070 |

## Compliance and engineering practice

| ID | Feature | Priority | Consumers | Shape | Requirements | CAP |
|---|---|---|---|---|---|---|
| FEAT-057 | Licence compliance and the clean room | MUST | D | L+S | `BR-1`, `BR-2`, `BR-3`, `CON-1`, `CON-4`, `CON-5`, `EXT-8`, `QA-14` | — |
| FEAT-058 | Engineering conventions as executable constraints | MUST | D | L+S | `CON-3`, `CON-7`, `CON-8`, `CON-9`, `QA-0` | — |
| FEAT-059 | Test architecture, with must-fail controls | MUST | D | L+S | `QA-1`, `QA-2`, `QA-3`, `QA-4`, `QA-11`, `QA-13`, `QA-15` | — |
| FEAT-060 | Documentation that cannot drift | MUST | U, A, D | L+S | `QA-19`, `QA-20`, `QA-21` | — |
| FEAT-061 | Product positioning — one design, two shapes, fewer tools | MUST | — | L+S | `BR-4`, `BR-5` | — |

## Reverse index — requirement to feature

The second half of the two-way trace. Every requirement declared in `specs/**` appears exactly once
below.

| Prefix | Requirement → feature |
|---|---|
| `BR-` | 1→057 · 2→057 · 3→057 · 4→061 · 5→061 |
| `CON-` | 1→057 · 2→056 · 3→058 · 4→057 · 5→057 · 6→056 · 7→058 · 8→058 · 9→058 · 10→004 · **11 and 12 are registry aliases**, not separate requirements — `CON-11` is `EXT-1` (→035) and `CON-12` is `EXT-8` (→057) |
| `FR-` (ingestion) | 001→001 · 002→002 · 003→003 · 004→004 · 005→005 · 006→006 · 007→007 · 008→007 · 009→008 · 010→008 |
| `FR-` (lifecycle) | 011→009 · 012→010 · 013→011 · 014→012 · 015→013 · 016→015 · 017→015 · 018→008 · 019→014 |
| `FR-` (query) | 020→016 · 021→017 · 022→018 · 023→019 · 024→020 · 025→021 · 026→022 · 027→022 · 028→022 · 029→023 · 030→023 · 031→023 · 032→023 · 033→024 · 034→025 · 035→025 · 036→026 · 037→027 · 038→027 · 039→013 |
| `FR-` (repos) | 040→028 · 041→028 · 042→029 · 043→030 · 044→030 · 045→032 · 046→032 · 047→031 |
| `FR-` (other) | 050→033 · 068→034 · 071→017 · 073→055 |
| `PERF-` | 1→050 · 2→051 · 3→051 · 4→042 · 5→020 · 6→009 · 7→052 |
| `SCALE-` | 1→052 · 2→050 · 3→029 · 4→050 · 5→034 |
| `COR-` | 1→020 · 2→010 · 3→008 · 4→053 · 5→017, 040 · 6→039 · 7→002 |
| `OPS-` | 1→054 · 2→050 · 3→009 · 4→013 · 5→054 · 6→054 · 7→054 |
| `REV-` | 1→039 · 2→039 · 3→039 · 4→039 · 5→056 |
| `IF-` | 1→040 · 2→040 · 3→045 · 4→041 · 5→041 · 6→041 · 7→028 · 8→041 · 9→041 · 10→040 · 11→042 · 12→043 · 13→043 · 14→044 |
| `EXT-` | 1→035 · 2→036 · 3→037 · 4→038 · 5→038 · 6→038 · 7→036 · 8→057 · 9→039 · 10→045 · 11→046 · 12→032 · 13→054 |
| `SEC-` | 1→045 · 2→045 · 3→045 · 4→046 · 5→046 · 6→047 · 7→048 · 8→046 · 9→049 · 10→032 · 11→043 · 12→032 · 13→049 · 14→049 · 15→049 · 16→049 · 17→049 |
| `QA-` | 0→058 · 1→059 · 2→059 · 3→059 · 4→059 · 5→002 · 6→003, 004 · 7→039 · 8→042 · 9→040, 056 · 10→052 · 11→059 · 12→055 · 13→059 · 14→057 · 15→059 · 16→003 · 17→039 · 18→041 · 19→060 · 20→060 · 21→060 |

## Features with no requirement, and requirements with no feature

**None, by construction and by audit.** The audit extracts both ID sets and diffs them; a residue in
either direction is either filed as a gap or explicitly dropped, per sync **A3**.

What the audit does **not** establish, and A3 must:

- **That a feature is the right grain.** `FEAT-023` bundles four requirements that a user experiences as
  four features, and `FEAT-049` bundles six security requirements that share only a category. Both may
  be wrong groupings; neither is a traceability failure.
- **That the feature list is what a stakeholder would recognise.** `FEAT-057` through `FEAT-061` are
  not features anyone asks for — they are compliance and practice requirements given feature identity
  so that no requirement is orphaned. That is honest bookkeeping and poor product language, and it is
  worth deciding at A3 whether they should be a separate register instead.

## Priority summary

| Priority | Features |
|---|---:|
| MUST | 58 |
| SHOULD | 2 — `FEAT-005` (declarative formats), `FEAT-038` (optional store slots) |
| WON'T | 2 — `FEAT-027` (dependence and taint), `FEAT-044` (terminal surface) |

**Fourteen features are marked inherited-negative**, which is the clearest single indicator of where the
design risk is concentrated: change detection, incrementality, escalation reporting, derived
identities, diff-impact input shapes, multi-repository serving, rename, indexing jobs, rank fusion,
upgrade, the surface contract, the agent surface, identity, fail-closed, and read concurrency.

## Verification

### What is proven

- **Two-way traceability**, asserted by an executable ID-set diff rather than by reading: every feature
  names ≥1 requirement, and every one of the requirement IDs declared in `specs/**` appears exactly
  once in the reverse index.
- **The requirement ID list was extracted from the SPEC files**, not written from memory, so the reverse
  index cannot silently miss a requirement that exists.
- **Priorities are inherited from the requirements**, not assigned here, so a feature cannot be a MUST
  while every requirement under it is a SHOULD.

### What is NOT proven

- **That the grain is right.** See above — two features are acknowledged over-bundles.
- **That the list is complete as a *product* description.** It is complete as a *requirement* index.
  Sync **A1** owns completeness of the capability set; A3 owns only the correspondence.
- **`FEAT-026` is not implementable** (`FR-036`, `questions/0011`), and `FEAT-044` is a recorded
  absence rather than a decision (`questions/0009`).
- **No feature has an effort estimate or a sequence.** Deliberate — sequencing is the architect's, and
  MUST-level priority within the 58 is not differentiated, which `specs/09` records as a real omission.

## Amendments

- **2026-08-20** — Created.

## Related

- `specs/` — the requirements every row here carries.
- `analysis/0001-capabilities.md` — the capability rows, and the `CAP-0nn` ↔ `FR-0nn` alignment.
- `SYNCS.md` — sync **A3**, the traceability checkpoint this document exists for.
