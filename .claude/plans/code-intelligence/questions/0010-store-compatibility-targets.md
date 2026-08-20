# Question 0010 — Which products are the per-slot compatibility targets?

- **Status:** open · **Owner:** the requester, then sync **B2** · **Date:** 2026-08-20
- **Owns:** `GAP-010`
- **Blocks:** nothing in the requirements. Blocks `EXT-9`'s async screening, which blocks
  `questions/0003`, which blocks the first store implementation.

## The question

`PROMPT.md`'s Appendix A records that the requester **named specific products per store slot** and
instructs that they be treated as compatibility targets, named only in the external-systems section.
**The product list itself did not survive into the trigger prompt** — only the six slot names did.

So: what were they?

## What was done in the meantime

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
