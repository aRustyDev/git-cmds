# Analysis 0008 — Graph slot: first-pass candidate screen

- **Date:** 2026-08-20 · **Status:** first pass, registry evidence only. Input to syncs **B2** and **B7**.
- **Scope:** the ten graph candidates supplied in `questions/0010`. This is the `EXT-9` screening record
  for the graph slot; `analysis/0004` points here.
- **Vocabulary:** [`GLOSSARY.md`](../GLOSSARY.md)

## What this screen does and does not establish

**Established, from the package registry on 2026-08-20:** licence · published version · first-published
and last-updated dates · total and recent download counts · self-described shape · whether a query
language is mentioned at all.

**Not established, and it needs running the software:** conformance to `EXT-1`'s capability profile ·
**client concurrency model** (so this screen does **not** answer `questions/0003`) · how much of Cypher
is actually implemented · whether an embedded engine is pure Rust or an FFI binding · read-during-write
semantics for `COR-4` · bulk-load performance.

**So this is a screen that eliminates, not one that selects.** Its value is that it disqualifies on
cheap evidence before anyone spends effort on capability testing — and it disqualifies more than half
the list.

## The register

Sorted by recent adoption, because `C5` in `questions/0010` established that maintenance and survival —
not capability — are the dominant risk here.

| Candidate | Crate | Licence | Version | First published | Last updated | Total dl | Recent dl | Shape | Query language |
|---|---|---|---|---|---|---|---:|---:|---|---|
| **Ladybug** | `lbug` | MIT | 0.19.1 | 2025-11-01 | **2026-08-04** | 367,274 | 309,495 | in-process | Cypher |
| **raphtory** | `raphtory` | unchecked | 0.17.0 / 0.18.5 | — | 2026-03-10 / 2026-06-25 | 43,210 | — | temporal graph **library** | GraphQL |
| **IndraDB** | `indradb-lib`, `indradb` | **MPL-2.0** | 5.0.0 | 2018-01-24 | **2025-08-16** | 87,763 | 4,222 | **library *and* server** | **none** |
| **Grafeo** | `grafeo` | Apache-2.0 | 0.5.42 | 2026-01-29 | 2026-05-04 | 17,235 | 14,580 | embeddable, **no C deps** | GQL, Cypher, SPARQL, Gremlin, GraphQL |
| **Neo4j** | not a crate | **GPL-3.0** (Community) | — | mature | mature | — | — | **networked only** | Cypher |
| **sombra** | `sombra` | MIT | 0.3.6 | 2025-10-22 | **2025-10-26** | 959 | **20** | embedded, single-file | **none** |
| **SparrowDB** | `sparrowdb` | MIT | 0.1.27 | 2026-03-23 | **2026-08-17** | 717 | 355 | embedded, no server | Cypher (own parser/planner) |
| **Omnigraph** | `omnigraph-*` | unchecked | 0.8.0 / `-db` 0.0.1 | — | 2026-07-01 / 2026-08-08 | 171–568 / **17** | — | engine + server + cluster | unchecked |
| **graphdblite** | `graphdblite` | MIT | 0.1.2 | 2026-05-16 | 2026-07-09 | **66** | 53 | embedded | Cypher |
| **kin** | **not found** | — | — | — | — | — | — | — | — |

## The finding that matters most

**The list contains exactly one networked openCypher candidate: Neo4j.**

`EXT-1` requires the slot to swap **embedded ↔ networked**, and `REV-2` requires both halves before v1.
Of the ten:

- **Embedded and speaks Cypher:** Ladybug, Grafeo, SparrowDB, graphdblite.
- **Networked and speaks Cypher:** **Neo4j, alone.**
- **Spans both halves in one project:** IndraDB — which has **no query language at all**.

So the pair is effectively **forced**: one young embedded Rust engine on one side, Neo4j on the other.
And that is precisely `EXT-1`'s recorded hazard — the abstraction must span **two unrelated dialects**,
where read traversal ports and schema definition, bulk load, index creation and standard-function return
types do not.

**The most interesting near-miss is IndraDB**, and it is worth stating plainly: the one candidate that
would solve the hardest part of this slot — a single project offering both an embedded library and a
server, so the pair is spanned by one dialect and one team — is disqualified by the query-language
requirement. If the openCypher requirement were relaxed to "a graph query interface", IndraDB becomes the
strongest structural fit in the list. That is a **requirements** question, not a screening one, and it
belongs to the requester.

## Dispositions

Using the outcome vocabulary Track C already shares: *adopt · vendor · emulate · take the UX only ·
decline*, adapted here to *carry forward · hold · decline*.

### Carry forward to capability screening — 3

| Candidate | Why | What to check first |
|---|---|---|
| **Ladybug (`lbug`)** | Overwhelmingly the most-adopted candidate — 367k downloads, 84% of them recent — MIT, and updated two weeks ago. Embedded, Cypher. | Whether it is pure Rust or an FFI binding (the single-binary question, `CON-10`'s shape in another slot). Client concurrency model. **Plus two dialect quirks measured in this engine during the prior grounding** — see below. |
| **Grafeo** | Apache-2.0, and the **only candidate that addresses the single-binary constraint head-on** — "no required C dependencies". Real adoption for its age. | Its claim to support **five** query languages is a breadth-over-depth signal in a project seven months old; check how much Cypher is real. Last release is 3.5 months old — confirm it is still moving. |
| **Neo4j** | The only networked option, mature, and `external-only` is already the right call — GPL-3.0 Community reached arm's-length over its protocol satisfies `EXT-8` clause 2. | Dialect distance from whichever embedded engine is chosen. This is the abstraction's real cost. |

**Two measured quirks in `lbug`, carried forward because withholding a known defect from a screen would
be worse than the awkwardness of citing it.** Both were measured during the prior grounding, and both are
properties of the engine rather than of anything built on it:

1. **A standard function returns a scalar where other Cypher implementations return a list.** Code written
   against it therefore breaks on a port, and — worse — breaks *silently*, because indexing a scalar
   yields an empty value rather than an error. This is `EXT-1`'s "standard-function return types diverge"
   hazard, with a concrete instance.
2. **Edge kind is carried as a *property* on a single relationship type rather than as the relationship
   type itself.** That is a legitimate design and it means engines that index by relationship type cannot
   use their primary index for the most common filter in this system. It is `B3`'s modelling decision with
   a portability consequence, and it must be settled **before any schema**.

A third measured quirk — that its full-text index can only be rebuilt wholesale, with no per-document
update — **no longer bears on this slot**, because lexical ranking moved to the search slot on 2026-08-20
(`EXT-4`). It would have been disqualifying had it stayed.

### Hold — 2

| Candidate | Why held rather than declined |
|---|---|
| **IndraDB** | Structurally the best pair-spanner in the list and disqualified only by the query-language requirement. Holds pending the requester's answer on whether openCypher is negotiable. Note MPL-2.0 is file-level copyleft — permissive enough to link, and worth counsel's glance rather than mine. |
| **SparrowDB** | Genuinely active — released three days ago — with a real Cypher parser and planner, and an embedded-only design that fits the local shape. Held, not carried forward, because **717 total downloads and a single maintainer** is a survival risk that `REV-2` cannot absorb: if it dies, the seam loses its proof, not just a backend. |

### Decline — 4, with reasons

| Candidate | Reason |
|---|---|
| **raphtory** | **Wrong shape.** A temporal graph *analytics library* exposing GraphQL, not a property-graph database answering Cypher. It would not satisfy `EXT-1`'s profile without being something else. Its adoption is real; its purpose is different. |
| **sombra** | **Abandonment signature.** First published 2025-10-22, last updated 2025-10-26 — **four days of activity, then ten months of silence** — and 20 recent downloads. Also no query language. The grounding's recorded lesson from four archived graph projects applies directly: do not build on these. |
| **graphdblite** | Three releases, **66 total downloads**, first published three months ago. The description is exactly right for the slot; there is no evidence yet that the project exists in any durable sense. |
| **Omnigraph** | Very young with essentially no adoption (17 downloads on the database crate). Worth one note for later: it ships a **Cedar-backed policy engine**, which is the only candidate that touches `SEC-8`'s authorisation-unit problem natively — interesting if per-node authorisation is ever chosen, irrelevant otherwise. |

### Not a store candidate — 1

**`kin`** — identified 2026-08-20 from locations supplied by the requester. **It is not a graph store.**
It is a Rust, Apache-2.0, agent-first code-intelligence tool — *"a persistent graph of entities,
relationships, changes, and provenance, so humans and AI agents see what a change touches before it
merges"* — with a CLI, a daemon and an MCP surface.

That is **substantially this product**, not a component of it. It is therefore removed from this screen and
escalated: see [`findings/0001-kin-is-a-peer-implementation.md`](../findings/0001-kin-is-a-peer-implementation.md),
which bears on the plan's build-versus-adopt premise rather than on any requirement. `GAP-023`.

**Nine candidates screened, not ten.**

## Two things the screen found that were not being looked for

**1. `EXT-8` poses no problem for this slot.** Every identified candidate is MIT, Apache-2.0, MPL-2.0, or
GPL-3.0-reached-arm's-length. **No source-available, BSL, or purpose-enumerated licence appears in the
list** — so the class of trap that disqualified prior-art options, including one whose grant excludes
feeding its output to AI systems, is absent here. That is a genuinely clean result and it means licence
review is not the gate for this slot; survival is.

**2. An existing crate may already be this slot's abstraction.** `grust-graph` — MIT OR Apache-2.0,
updated 2026-08-06 — describes itself as *"a backend-neutral property graph facade for Rust"* and carries
optional backends for nine engines plus an in-memory implementation, with Cypher support. A sibling crate
provides a Ladybug backend.

That is **`EXT-1`'s seam, as prior art**. It is young (first published 2026-06-07) and lightly adopted
(1,531 downloads), and its backend list does not include Neo4j — so it is not a drop-in answer. But its
existence is evidence the seam is buildable, and its shape is worth reading before designing ours.
**This is Track C material — adopt · vendor · emulate · decline — and it did not have a sync.** Recorded
as `GAP-022`.

## What this screen does not answer, and what would

| Question | Why unanswered | Cheapest next step |
|---|---|---|
| `questions/0003` — is the trait async? | Client concurrency model is not in registry metadata | Check the vector pair instead: if **both** Lance and Qdrant are async-only, the answer is determined by that slot alone, whatever the graph slot does |
| Does the chosen embedded engine ship a single binary? | Pure-Rust versus FFI is not in registry metadata | Build a trivial dependent crate for `lbug` and `grafeo` and inspect the link output |
| How much Cypher is real? | Descriptions claim; only running them tells | Run `EXT-1`'s profile as a conformance fixture against both |
| Can it satisfy `COR-4`? | Read-during-write semantics are undocumented at this level | The four-cell cross-process matrix, with a control that must fail |

## Verification

### What is proven

- **Every candidate's licence, version, publication dates and download counts were read from the package
  registry on 2026-08-20**, not recalled. Where a value could not be read it is marked `unchecked`.
- **The pair-forcing finding is derived from the register**, by counting which candidates are networked
  and speak Cypher. Exactly one does.
- **Four declines each name a specific disqualifying fact** — wrong shape, a four-day activity window,
  66 downloads, 17 downloads — rather than a judgement.
- **`kin` is recorded as unidentifiable rather than guessed at.**

### What is NOT proven

- **No candidate was installed, built or run.** Every capability claim here is the project's own
  description. The grounding's own recorded lesson applies with full force: **a capability whose name
  matches is not evidence it exists**, and three of four such verdicts were overturned when someone
  checked. Treat the "Query language" column as `presumed`.
- **Download counts are a weak survival proxy.** `lbug`'s 84%-recent profile is consistent with rapid
  genuine adoption *and* with continuous-integration churn; nothing here distinguishes them.
- **raphtory's and Omnigraph's licences were not checked**, because both were declined on shape and
  adoption. If either is revived, that gap must be closed first.
- **Neo4j was not screened at all** beyond its licence and role — it is mature, well-known, and the only
  networked option, so the screen adds nothing. Its dialect distance from the embedded half is the real
  unknown and this document does not measure it.
- **"Maintenance" here means last-published-version date.** Commit cadence, contributor count and issue
  responsiveness were not examined, and a project can publish rarely and be healthy.

## Amendments

- **2026-08-20** — Created. First-pass registry screen of the ten candidates supplied in `questions/0010`.

## Related

- `questions/0010-store-compatibility-targets.md` — the candidate list and the five consequences it raised.
- `analysis/0004-store-capability-matrix.md` — the capability profile this screen is against, and the slot-wide record.
- `specs/04-interfaces-and-external-systems.md` — `EXT-1`, `EXT-8`, `EXT-9`.
- `GAPS.md` — `GAP-022` (`grust-graph` as prior art for the seam).
