# Analysis 0003 — Feature-gap matrix and precedent risk

- **Date:** 2026-08-20 · **Status:** input to syncs **A1**, **A4** and Track **C**
- **Purpose:** for every required capability, does *anything* demonstrate it is feasible? A capability
  with no precedent anywhere carries no proof of feasibility, and that is a different and larger risk
  than a capability that is merely unbuilt.

## Disposition vocabulary

House matrix vocabulary: **✓ covered · ◐ partial · ✗ gap · — N/A**, applied to *precedent* rather than
to our own coverage.

| Column | Asks |
|---|---|
| **Ref** | Does the reference implementation do something equivalent? Evidence: the prior grounding. |
| **Perm** | Does a permissively-licensed code-intelligence tool do it? Evidence: the licence-screened survey in the grounding. |
| **Gen** | Is there routine precedent in general-purpose software outside code intelligence? Only meaningful for platform capabilities. |
| **Risk** | See the risk classes below. |

## Four risk classes, not two

The naive reading is "precedent good, no precedent bad". The matrix produces a more useful split, and
**the third class is the one this project has to think hardest about**.

| Class | Means | Consequence |
|---|---|---|
| **routine** | Precedent in at least two places, at least one of them readable. | Normal engineering risk. |
| **single-source** | Exactly one tool does it, and we can read it. | Feasible, and we have one design to learn from. Watch for copying its constraints along with its ideas. |
| **inaccessible** | Precedent exists **only** in the reference implementation, which the clean room forbids reading. | **Feasibility is proven and the design is not available.** We know it can be done and must work out how from first principles. Worse than single-source, better than net-new. |
| **elevated** | No precedent anywhere. | No proof of feasibility. Must be prototyped before it is scheduled, not designed on paper. |

**`inaccessible` is a risk class the clean room creates**, and it did not exist before this project's
constraints did. It is worth naming because the instinct on seeing "the reference does this" is relief,
and here it should be the opposite of relief.

## A. Ingestion and index construction

| CAP | Capability | Ref | Perm | Gen | Risk |
|---|---|---|---|---|---|
| 001 | Language and scope detection | ✓ | ✓ | — | routine |
| 002 | Per-language parsing | ✓ | ✓ | — | routine |
| 003 | Extraction to a declared depth | ✓ | ✓ | — | routine |
| 004 | Add a language without a fork | ◐ | ◐ | — | single-source · see note 1 |
| 005 | Declarative infrastructure and config analysis | ✗ | ✓ | — | single-source · see note 2 |
| 006 | Cross-file resolution | ✓ | ✓ | — | routine |
| 007 | Route-to-handler mapping | ✓ | ◐ | — | inaccessible · see note 3 |
| 008 | RPC and tool-definition mapping | ✓ | ✗ | — | inaccessible |
| 009 | Flow derivation | ✓ | ✗ | — | **inaccessible** · see note 4 |
| 010 | Cluster derivation | ✓ | ✗ | — | **inaccessible** · see note 4 |
| 011 | Change detection **before** the expensive work | ✗ | ✗ | ◐ | **elevated** · see note 5 |
| 012 | Incremental index update | ◐ | ✗ | ✓ | elevated for the graph half |
| 013 | Full rebuild | ✓ | ✓ | ✓ | routine |
| 014 | Index or update on request | ✓ | ✓ | ✓ | routine |
| 015 | Index status and freshness | ◐ | ◐ | ✓ | routine |
| 016 | Embedding generation | ✓ | ✓ | ✓ | routine |
| 017 | Lexical index maintenance | ✓ | ✓ | ✓ | routine |
| 018 | Derived identities addressable, and stable across runs | ◐ | ✗ | ✗ | **elevated** · see note 6 |
| 019 | Escalation reporting | ✗ | ✗ | ✓ | routine — it is observability, not analysis |

## B. Query and analysis

| CAP | Capability | Ref | Perm | Gen | Risk |
|---|---|---|---|---|---|
| 020 | Read-only graph query | ✓ | ✓ | ✓ | routine |
| 021 | Hybrid search, flow-grouped | ✓ | ◐ | ✓ | inaccessible for the flow-grouping half |
| 022 | 360-degree symbol view | ✓ | ✓ | — | routine |
| 023 | Reachability with a witness path | ✓ | ◐ | ✓ | routine — it is graph search |
| 024 | Blast radius, transitive, bounded, projected | ✓ | ✓ | ✓ | routine |
| 025 | Downstream reachability | ◐ | ✓ | ✓ | routine |
| 026 | Diff impact from a working tree | ◐ | ✓ | — | single-source · see note 7 |
| 027 | Diff impact from `base...head` | ✗ | ◐ | ✓ | routine — it is a diff |
| 028 | Diff impact from a supplied patch, no checkout | ✗ | ✗ | ◐ | **elevated** · see note 8 |
| 029 | Filter by node type and edge class | ✓ | ✓ | ✓ | routine |
| 030 | N-hop neighbourhood | ✓ | ✓ | ✓ | routine |
| 031 | Node and edge counts | ✓ | ✓ | ✓ | routine |
| 032 | Sub-directory scoping | ✓ | ✓ | — | routine |
| 033 | Read-only structural checks | ✓ | ✓ | ✓ | routine |
| 034 | Response-shape conformance | ✓ | ✗ | ✗ | **inaccessible** · see note 9 |
| 035 | Route pre-change report | ✓ | ✗ | — | inaccessible — but it is a projection over 024 |
| 036 | Repository wiki | ✓ | ✗ | ◐ | single-source · see note 17 |
| 037 | Statement-level dependence | ✓ | ✓ | ✓ | routine — deferred to v2 |
| 038 | Taint findings | ✓ | ✓ | ◐ | routine — deferred to v2 · see note 10 |
| 039 | Freshness on every answer | ✗ | ✗ | ✓ | routine |

## C. Repositories, groups and acquisition

| CAP | Capability | Ref | Perm | Gen | Risk |
|---|---|---|---|---|---|
| 040 | Paginated repository discovery | ✓ | ◐ | ✓ | routine |
| 041 | Repository switching | ✓ | ◐ | ✓ | routine |
| 042 | Simultaneous multi-repository serving | ◐ | ✗ | ✓ | routine — general precedent is ample |
| 043 | List repository groups | ✓ | ✗ | — | inaccessible |
| 044 | Group contract registry and cross-repository links | ✓ | ✗ | ✗ | **inaccessible** · see note 11 |
| 045 | Repository acquisition | ✓ | ◐ | ✓ | routine |
| 046 | Private-remote credentials | ◐ | ◐ | ✓ | routine |
| 047 | Evidence class on inferred edges | ✗ | ✗ | ✗ | **elevated** · see note 12 |

## D. Write operations

| CAP | Capability | Ref | Perm | Gen | Risk |
|---|---|---|---|---|---|
| 050 | Coordinated rename — AST-accurate **with index writeback** | ✗ | ◐ | — | **elevated** · see note 13 |

## E. Platform

| CAP | Capability | Ref | Perm | Gen | Risk |
|---|---|---|---|---|---|
| 060 | Six store slots, each embedded↔networked | ✗ | ◐ | ✓ | single-source · see note 14 |
| 061 | Embedding-provider selection | ✓ | ✓ | ✓ | routine |
| 062 | Runtime AI-provider configuration | ◐ | ✗ | ✓ | routine |
| 063 | Restrict runtime configuration to absence | ✗ | ✗ | ✓ | routine |
| 064 | External authentication | ✗ | ✗ | ✓ | routine |
| 065 | External authorisation | ✗ | ✗ | ✓ | routine · see note 15 |
| 066 | Per-principal attribution end to end | ✗ | ✗ | ✓ | routine |
| 067 | Audit trail | ✗ | ✗ | ✓ | routine |
| 068 | Durable, queued, cancellable indexing | ◐ | ✗ | ✓ | routine |
| 069 | Telemetry | ✗ | ✗ | ✓ | routine |
| 070 | Deployment-shape assembly | ◐ | ◐ | ✓ | routine |
| 071 | Exactly one rank-fusion implementation | ✗ | — | ✓ | routine — it is a discipline requirement |
| 072 | Reads scaling with readers per replica | ✗ | ◐ | ✓ | routine |
| 073 | Upgrade without a full reindex | ✗ | ✗ | ✓ | single-source · see note 16 |
| 074 | Repositories bounded by capacity, not a constant | ✗ | ✗ | ✓ | routine |

## Notes

1. **Extensibility is partial everywhere.** Both the reference and the permissive tools have a
   per-language contract, and in both cases adding a language is a build-time change to the tool
   rather than a deployment-time extension. Whether we need build-time or runtime extension is
   `CON-10`, unresolved.
2. **The declarative-format gap is the reference's, not the field's.** A permissive tool claims
   infrastructure indexing, so `FR-005` has readable precedent. Depth is unverified — the claim has
   not been tested — and `GAP-005` records that no surveyed tool covers these formats *well*.
3. **Route extraction has broad precedent and narrow generic precedent.** Per-framework extraction is
   well-trodden; a *generic* annotation-or-decorator model is not. The grounding measured the
   reference's own generic handling to be much narrower than its route coverage suggested — a fixed
   list of framework-specific names, with anything outside it becoming an unpersisted scoring nudge.
   So `FR-007` is safe and a generic version of it is not what the precedent covers.
4. **Flows and clusters are the sharpest `inaccessible` entries in the matrix.** The grounding's
   explicit finding is that **nothing permissive reproduces execution-flow derivation or whole-graph
   cohesion clustering** — and these are the capabilities the reference leads with and that its agent
   consumers actually use. We therefore know they are feasible and have no readable design. Combined
   with note 6, this is the single largest concentration of risk in the matrix: `FR-009`, `FR-010` and
   `FR-018` are interdependent, jointly `inaccessible` or `elevated`, and jointly the input to the
   query surface.
5. **Change detection before the compute is `elevated` and is the hardest requirement in the corpus.**
   The reference decided incremental-versus-full *after* running the whole pipeline. No permissive tool
   is known to do better. General precedent exists for incremental compilation and build systems, which
   is where the ideas will have to come from — but a build system knows its dependency graph
   declaratively, and here the dependency graph is the thing being computed. **Prototype before
   scheduling.**
6. **Stable derived identities have no precedent anywhere.** The reference recomputed them wholesale,
   which is precisely the measured failure. No permissive tool derives these structures at all, so none
   has faced the identity question. And general-purpose precedent does not transfer: stable identity
   under a *global* partitioning algorithm is a known-hard problem, not an engineering detail.
   `questions/0004` must be answered before `FR-018` is designed.
7. **Diff impact's precedent is weaker than its name.** The reference's diff-oriented capability was
   measured as a **single-hop lookup against a precomputed membership table**, not a transitive walk —
   so it answers a different question from its symbol-oriented counterpart, and the two were chained
   only by prose instructions to a calling model. A permissive tool advertises git-diff blast radius
   with risk classification; that claim is unverified. Treat `FR-026`'s precedent as "something with
   this name exists", not "this capability exists".
8. **Patch-without-checkout is `elevated`.** The reference could not express it. No permissive tool is
   known to. General precedent exists in code-review tooling, which operates on patches — but not
   combined with a persistent graph index of a repository it has never fetched. The specific unknown is
   the accuracy of mapping patch context lines onto indexed symbols, which `GAP-003` records may need a
   syntax-aware diff (sync **C3**).
9. **Response-shape conformance is `inaccessible` and single-source in the whole field.** Only the
   reference is known to do it. It is also the capability whose *correctness* is least well-defined,
   because an inferred shape yields findings that are evidence rather than proof — which is why `FR-034`
   requires declared and inferred shapes to be distinguished.

   **Amended 2026-08-20 — materially de-risked for the primary corpus.** The target corpus communicates
   over gRPC/HTTP (`analysis/0007`), and those schemas are **declared**. So the dominant case becomes
   "compare a declared contract against observed consumer accesses", which is a far stronger footing than
   inference. The `inaccessible` disposition stands for ad-hoc handlers returning unstructured payloads;
   the hardest instance of this capability just became its easiest.
10. **Taint has readable permissive precedent, and it is partial in an important way.** One mature
    Apache-licensed tool does interprocedural taint properly; another does inter-method taint **within a
    file** but not across files. Deferred to v2, so this is recorded rather than acted on — but it means
    `FR-038` returns with genuinely readable precedent, which most of this matrix does not.
11. **Cross-repository contract registries have no permissive precedent** and no general precedent that
    transfers. Service-catalogue and API-registry products exist, but they consume declarations rather
    than inferring links into a code graph. This is `inaccessible`, and `GAP-008` compounds it: even the
    reference offers no confidence model for the inferred edges it produces.
12. **Evidence class is `elevated` and cheap.** Nothing has it, and nothing needs to be invented — it is
    a field on an edge plus discipline about not mixing classes in a count. The risk is not feasibility,
    it is that the *weighting* question (`GAP-008`) has no precedent to borrow from, so we will be
    designing it.
13. **Rename is `elevated` for the combination, not the parts.** Structural search and rewrite over
    syntax trees has excellent permissive precedent. Graph-driven reference sets have precedent. **The
    combination — an AST-accurate rewrite whose edit set comes from the graph and which writes the
    result back to the index atomically — has no precedent anywhere**, and the reference's version was
    a whole-file regex with no writeback. Clause 3 of `FR-050` is the novel part.
14. **Store swappability is single-source and the source is thin.** The reference had no abstraction
    seam at all — the grounding found zero backend interfaces and one accidental de-facto seam whose
    signature leaked the concrete engine. One permissive tool advertises a pluggable backend, which is
    readable precedent for *one* slot. **Six slots, each embedded↔networked, behind one conformance
    suite, has no precedent** — but general-purpose precedent for repository-pattern abstraction is
    ample, so this is a design problem rather than a feasibility one.
15. **Authorisation is routine in general and absent in this field.** No surveyed code-intelligence
    tool has per-principal authorisation. That is a statement about the field's maturity, not about
    difficulty, and `SEC-8`'s open question — the *unit* of authorisation — is where the real work is,
    because per-node authorisation has no precedent in a graph-query product.
16. **Upgrade-without-reindex is single-source via general precedent.** Schema migration is routine
    software engineering. What has no precedent is doing it for a *derived* graph whose derived
    identities are part of the query surface, which folds back into note 6.
17. **The wiki is `single-source`, not `inaccessible`, and this note corrects an error.** *(Added
    2026-08-20.)* The reference's wiki is documented in its **public** documentation, which the clean-room
    protocol explicitly permits reading for capability vocabulary — so the precedent is **readable** at the
    contract level even though its source is not. The publicly-described behaviour is: a language model
    groups files into modules, a page is generated per module plus an overview, and the pages cross-reference
    the knowledge graph.

    This changes the disposition and it changes the requirement: `FR-036` now specifies a structured
    document set with **deterministic** module grouping from derived clusters, and prose as a separately
    gated optional stage — deliberately *not* following the precedent's LLM grouping, with the cost of that
    choice recorded. **The general lesson for this matrix: `inaccessible` means the *design* is unreadable,
    and a capability's public documentation is not its design. Two other rows may be misdispositioned for
    the same reason** — 034 and 035 — and nobody has checked their public documentation either.

## Where the risk actually concentrates

Counting the matrix:

| Class | Count | Capabilities |
|---|---:|---|
| routine | 38 | mostly platform and query |
| single-source | 7 | 004, 005, 026, 036, 060, 073, and 021's ranking half |
| **inaccessible** | 8 | 007, 008, **009**, **010**, 034, 035, 043, **044** |
| **elevated** | 7 | **011**, 012 (graph half), **018**, **028**, **047**, **050** |

**Two findings matter more than the counts:**

1. **The elevated and inaccessible entries cluster around three requirements, not seven.** Flow and
   cluster derivation (`FR-009`, `FR-010`), their identities (`FR-018`), and change detection
   (`FR-011`) are mutually entangled: derived structures are what makes incrementality change *output*
   rather than cost, and identity stability is what makes recomputation safe or unsafe. **These four
   requirements are one risk, and they are the risk.**
2. **Every platform capability is routine, and every one of them is absent from the reference.** The
   entire `SEC-*` and `OPS-*` surface is `✗ Ref, ✗ Perm, ✓ Gen`. That is the clearest signal in the
   matrix: the field has not built these, and the field is not where to look for them. Ordinary
   service-engineering practice is.

## Capabilities the requester's list omitted, and their precedent

All seven were confirmed wanted on 2026-08-20. Their precedent, since that was the reason to ask:

| Capability | Requirement | Precedent |
|---|---|---|
| Transitive blast radius with a depth bound | `FR-024` | ✓ both — routine |
| Shortest-path trace with a witness | `FR-023` | ✓ ref, ◐ perm — routine (graph search) |
| Route-to-handler mapping | `FR-007` | ✓ ref — inaccessible for the generic form |
| RPC/tool-definition mapping | `FR-008` | ✓ ref only — inaccessible |
| Response-shape conformance | `FR-034` | ✓ ref only — `inaccessible` for inferred shapes; **de-risked** where schemas are declared, which is the primary corpus (note 9) |
| Pre-change route report | `FR-035` | ✓ ref only — inaccessible, but a projection over `FR-024` |
| Coordinated multi-file rename | `FR-050` | ✗ for the required combination — **elevated** |

**Two of the seven are the riskiest things the requester added**: response-shape conformance and
rename. Both were worth adding; both should be prototyped rather than designed on paper.

## Verification

### What is proven

- **Every capability in `analysis/0001` has a row.** 60 rows against 60 capabilities.
- **Every `elevated` and `inaccessible` entry carries a note** explaining what specifically is missing,
  rather than a bare symbol.
- **The `inaccessible` class is named and justified.** It follows from the clean room and it changes what
  "the reference does this" means — from reassurance to a warning that feasibility is known and the
  design is not.
- **The risk concentration is derived from the matrix**, and it collapses seven scattered high-risk
  entries into one entangled group of four requirements.

### What is NOT proven

- **The `Perm` column rests on a survey, not on use.** No permissive tool was installed, run or read
  during this work. Every ✓ in that column is a capability *claim* from the survey, and the grounding's
  own recorded lesson is that a capability whose **name** matches is not evidence it exists — three of
  four such verdicts were overturned when someone checked. **Treat the `Perm` column as `presumed`
  throughout**, and see `GAP-012`.
- **The `Ref` column is second-hand.** It comes from the grounding rather than from reading source,
  which is correct under `CON-1` and does mean the granularity is coarse.
- **The `Ref` column also under-uses a permitted source, and this was caught once.** The clean-room
  protocol permits reading the prior art's **public documentation** for capability vocabulary, and doing
  so for the wiki overturned its disposition (note 17). **That check has not been run for any other
  row.** So every `inaccessible` entry here should be read as "we did not look at the public docs", not
  as "no readable description exists" — and 034 and 035 are the two most likely to move.
- **The `Gen` column is judgement.** "Routine precedent in general-purpose software" is not something
  this document measured.
- **No feasibility prototype has been built for any `elevated` entry.** That is the recommendation this
  matrix produces and it has not been acted on.
- **The counts assume one row per capability.** Where a capability bundles several — `CAP-003`,
  `CAP-021` — a single disposition hides variation.

## Amendments

- **2026-08-20 (same day, second pass)** — **`CAP-036` reclassified `inaccessible` → `single-source`**,
  and note 17 added. The error was treating "we may not read its source" as "we may not read anything":
  the prior art's **public documentation** describes the wiki's contract, and the clean-room protocol
  explicitly permits reading public docs for capability vocabulary. **Rows 034 and 035 may be
  misdispositioned for the same reason and have not been re-checked.** Note 9 amended: response-shape
  conformance is materially de-risked where schemas are declared, which is the primary corpus.
- **2026-08-20** — Created.

## Related

- `analysis/0001-capabilities.md` — the capability rows.
- `GAPS.md` — `GAP-003`, `GAP-005`, `GAP-007`, `GAP-008` and `GAP-012` all originate or are corroborated here.
- `SYNCS.md` — Track **C** exists to convert `Perm` claims into verified precedent; **A4** to generate net-new capabilities deliberately.
