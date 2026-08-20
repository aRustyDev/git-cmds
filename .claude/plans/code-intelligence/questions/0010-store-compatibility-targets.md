# Question 0010 — Which products are the per-slot compatibility targets?

- **Status:** **answered 2026-08-20** — the list is supplied and recorded below. **Open** on the
  five consequences it raises (C1–C5), and **entirely unscreened**.
- **Owner:** the requester on C1 and C3; sync **B2** on the screen · **Date:** 2026-08-20
- **Owns:** `GAP-010`
- **Blocks:** nothing in the requirements. Blocks `EXT-9`'s async screening, which blocks
  `questions/0003`, which blocks the first store implementation.

## The question

`PROMPT.md`'s Appendix A records that the requester **named specific products per store slot** and
instructs that they be treated as compatibility targets, named only in the external-systems section.
**The product list itself did not survive into the trigger prompt** — only the six slot names did.

So: what were they?

## ✅ Answered 2026-08-20 — the list, as supplied

Recorded verbatim on receipt, **before any screening**, because this register entry exists precisely
because the list was lost once (`GAP-010`).

| Slot | Candidates, as given |
|---|---|
| **Graph** | Neo4j **(external-only)** · Ladybug · Grafeo · IndraDB · graphdblite · sombra · Omnigraph · raphtory · SparrowDB · kin |
| **Relational** | SQLite · PostgreSQL |
| **Vector** | Qdrant · Lance |
| **Search** | OpenSearch |
| **Key-value** | Valkey · Redis · RocksDB |
| **Text-search** | **dropped — slot removed** |

**Nothing here is screened.** No candidate has been checked for licence, maintenance status, embedded
versus networked, client concurrency model, dialect coverage, or the capability profile in `specs/04`.
`EXT-9`'s screening record remains empty, so `questions/0003` is still unanswerable. Treat every name
above as a **candidate**, not a selection.

**Two observations that are decisions rather than screening**, and both are the requester's to confirm:

1. **Marking Neo4j external-only is correct and worth keeping explicit.** Its Community edition is
   GPL-3.0, and reaching it over its network protocol as a separate process is the arm's-length posture
   `EXT-8` clause 2 requires. Embedding it would be a materially different licence question.
2. **Dropping text-search relocates a requirement rather than removing one** — see below. That is the
   one consequence of this list that needs an answer before `specs/04` can be amended.

## Consequences of the list that need answers

### C1 — **Decided 2026-08-20: OpenSearch provides lexical ranking**

`FR-017`'s lexical index moves into the **search slot**. `EXT-4` becomes **MUST** and gains the consumer
it lacked; `EXT-5` becomes an explicit `WON'T` with a revisit trigger; `GAP-011` closes for the search
half and stays open for key-value.

**Three consequences, two of them good:**

- ✅ **It resolves C2 instead of relocating it.** Per-document lexical update was mandatory because the
  grounding measured an engine that could only rebuild its whole index. A general-purpose search engine
  satisfies that natively, so the hazard is removed rather than moved onto the graph slot.
- ✅ **It widens the graph candidate set**, since lexical ranking is no longer a graph-engine requirement.
  `analysis/0008` screens the graph slot on that basis.
- ⚠️ **The embedded half is unnamed.** There is no embedded OpenSearch, and the candidate list contains no
  pure-Rust lexical index — so the slot has one implementation and is **not yet a proven seam** under
  `REV-2`. Worse, the local shape then has no lexical lane at all, which makes the two deployment shapes
  differ in *capability* rather than configuration — uncomfortably close to what `CON-2` forbids. Filed as
  `GAP-021`, and it needs a named candidate rather than a screening pass.

**The reasoning kept for the record** — the three options as they stood before the decision:

`FR-017` requires a lexical index; `FR-021`'s hybrid search has a lexical lane. Removing the
text-search slot does not remove that requirement — it **relocates** it, to either the graph engine or
the search slot. Which one changes the screening criteria substantially:

- **If the graph engine provides it**, then lexical ranking becomes a **mandatory** graph-candidate
  capability rather than an optional one — and it carries a specific known failure mode, see C2.
- **If the search slot provides it**, then OpenSearch acquires the consumer it currently lacks
  (`GAP-011`), the slot becomes **required rather than optional**, and its embedded half is empty,
  because there is no embedded OpenSearch. `REV-2`'s two-implementations rule would then need a
  pure-Rust lexical index naming a second candidate that this list does not contain.
- **If neither provides it**, `FR-021` loses a lane permanently and should be respecified as
  traversal-plus-semantic, with `FR-017` becoming a `WON'T`.

### C2 — Per-document lexical update is now a hard screening filter, not a preference

`EXT-5`'s profile made per-document update **required** because the grounding measured an engine whose
full-text surface offers only whole-index create, drop and query — **no per-row or per-document
update** — so every index run re-tokenises the entire corpus, incremental path included.

With text-search dropped and lexical ranking relocated to the graph engine, **that constraint moves onto
the graph slot and becomes load-bearing**: a graph candidate whose full-text index can only be rebuilt
wholesale directly contradicts `PERF-6` and `FR-012`. This is the sharpest single screening criterion
the list produces, and it eliminates candidates rather than ranking them.

### C3 — The key-value slot still has no consumer

Naming products does not create one (`GAP-011`). Valkey, Redis and RocksDB are candidates for a slot no
capability reads or writes. Recommendation unchanged: specify it, do not build it, until something needs
it. Note that if it is ever used for **coordination** rather than caching, compare-and-set becomes
load-bearing and the slot stops being optional.

### C4 — Licence notes worth carrying into the screen

Stated at the confidence I actually have, since `EXT-8` is a build gate and a wrong assumption here is
expensive:

- **Confident:** OpenSearch, Qdrant, RocksDB — Apache-family. SQLite — public domain. PostgreSQL — its
  own permissive licence. Neo4j Community — GPL-3.0. Valkey — BSD, and it exists *because* Redis
  relicensed, which is itself the `EXT-8` failure mode in the wild.
- **Needs checking:** Redis's current terms (they have changed more than once recently), Lance, IndraDB,
  raphtory, and **every one of Grafeo, graphdblite, sombra, Omnigraph, SparrowDB and kin**.
- **One point that cuts helpfully:** AGPL-3.0 is generally understood to permit combination with
  GPL-3.0 code, which may make a strong-copyleft **embedded** engine linkable where a permissive project
  licence could not. Worth counsel's confirmation rather than mine — but if it holds, it widens the
  embedded candidate set rather than narrowing it.

### C5 — The dominant risk in the graph list is maintenance, not capability

Most of the graph candidates appear to be small or young projects. The grounding recorded the specific
trap: **four graph projects surveyed for the prior effort were archived or unmaintained**, with the
recorded conclusion *"do not build on these"*. And `REV-2` requires **two** implementations per slot to
prove the seam is real — so a candidate that is abandoned takes the seam's proof with it, not just a
backend.

**So the screen must score maintenance status, not only capability**: last release, commit cadence,
contributor count, whether anything else depends on it in production. That criterion is absent from
`specs/04` and should be added to `EXT-9`'s procedure.

## What was done before the list arrived

Per the requester's decision of 2026-08-20: each slot is specified as a **capability profile** — the
contract business logic depends on — and candidate products are named in `specs/04` **marked
`presumed`**, drawn from this estate and from the licence-screened survey in the grounding.

| Slot | Embedded candidate | Networked candidate | Confidence |
|---|---|---|---|
| Graph | an in-process property-graph engine speaking openCypher | a networked openCypher-speaking engine | `presumed` |
| Vector | an in-process vector index | **Qdrant** (Apache-2.0) — already run in this estate | `presumed` |
| Relational | an embedded single-file SQL engine | a networked SQL server | `presumed` |
| Search | — | **OpenSearch** (Apache-2.0) or equivalent | `presumed`, and no consumer |
| Text-search | a lexical index inside the graph engine | **Zoekt** (Apache-2.0) or the search engine | `presumed`, conditional |
| Key-value | an in-process map | a networked key-value server | `presumed`, and no consumer |

**The graph slot's networked candidate is deliberately unnamed.** The requester specified "networked
openCypher", and the credible products in that space carry licence positions that need `EXT-8`'s
treatment individually — strong copyleft, business-source, or source-available with a use grant. Naming
one before that assessment would smuggle a licence decision into a compatibility note.

## Why the answer still matters

Three things depend on knowing the actual candidates, and none can be resolved from a capability profile
alone:

1. **`EXT-9`'s async screening.** The screening record in `analysis/0004` is **empty** because there is
   nothing to screen. And `questions/0003` — the async decision, which must be taken during screening
   and never after — cannot be answered without it. **This is the real dependency chain**, and it ends
   at a rewrite if it is got wrong.
2. **`EXT-8`'s licence gate.** A copyleft or source-available store must be reached at arm's length over
   its network protocol rather than linked, and at least one credible engine's grant excludes feeding
   its output to AI systems — which would disqualify it for this use case specifically, whatever its
   other terms say. That assessment is per product.
3. **`EXT-1`'s dialect hazard.** openCypher implementations agree on read traversal and diverge on
   schema definition, bulk load, index creation, extensions, and even standard-function return types.
   **How much the abstraction has to hide depends entirely on which two engines it spans.**

## What a good answer includes

Not just names:

- **Per slot, which embedded and which networked**, since `REV-2` requires both for the graph, vector
  and relational slots.
- **Whether any is already operated in this estate.** An engine with an existing operational story is
  materially cheaper than one without, and Qdrant is the one known case.
- **Whether any is mandated** rather than preferred — for instance because a platform team already runs
  it and will not run a second.
- **Whether the local shape's embedded choice is free**, or constrained by packaging: an embedded engine
  that requires native compilation at build time changes what "a single binary" means (`CON-10`'s
  shape, in a different slot).

## If the list cannot be recovered

Then the honest path is:

1. **Screen from the capability profiles**, treating the profile as the requirement and the product as
   an outcome. `analysis/0004` is written to support exactly this.
2. **Prioritise the graph slot**, because it carries the most risk on all three counts above and it is
   the slot whose abstraction is most likely to leak.
3. **Screen for async and licence in the same pass** (`EXT-9`, `EXT-8`). Doing them separately is how a
   candidate gets selected on capability grounds and then disqualified on licence grounds after a
   design depends on it.
4. **Record the screening as a scorecard per candidate**, which is house precedent — the estate's
   prior datastore screening paired a mandate document with a per-candidate scorecard template. Copy
   that shape rather than inventing one.

## Recommendation

**Ask the requester once, then stop waiting.** The question is cheap to ask and the answer may be
partially recoverable. But the dependency chain — product list → async screening → the async decision →
the first store implementation — means that waiting indefinitely converts a missing note into a blocked
project.

**The capability profiles are sufficient to begin screening.** That is deliberate: they were written so
that the absence of the product list is an inconvenience rather than a blocker.

## Related

- `specs/04-interfaces-and-external-systems.md` — `EXT-1`–`EXT-9`.
- `analysis/0004-store-capability-matrix.md` — the profiles, the hazards, and the empty screening record.
- `questions/0003-the-async-decision.md` — what this unblocks.
- `GAPS.md` — `GAP-010`.
