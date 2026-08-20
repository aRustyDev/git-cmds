# Question 0005 — Does any internal consumer need to *link* the engine?

- **Status:** open · **Owner:** the requester, with counsel · **Date:** 2026-08-20
- **Blocks:** nothing immediately. **Shapes** sync **B6**, the library/SDK/binary split.

## The question

This repository is **AGPL-3.0**. Anything that links `<ENGINE>` — statically, which is the normal Rust
case — forms a combined work subject to AGPL-3.0.

**Is there an internal consumer that needs to link the engine, rather than reach the capability across
a process boundary?**

## Why the answer changes the module split

`CON-4` makes the library/SDK/binary boundary partly a licence decision rather than only a cohesion
decision:

- **If no internal consumer needs to link**, `CON-4` costs nothing. Every consumer arrives over the
  CLI, the API or the agent protocol, and the split can be decided purely on cohesion grounds.
- **If one does**, then whichever capabilities that consumer needs must sit in a crate it can accept
  AGPL for — or the capability must be pushed behind a service boundary, which changes the split.

**A permissively-licensed shim does not resolve this.** A thin wrapper crate under a different licence
that links an AGPL library still produces a combined work.

## The tension with §13, which is the part most likely to be missed

`CON-5`: if the service is exposed to users beyond the organisation, AGPL §13 obliges offering them the
corresponding source of the version they interact with.

So the two AGPL consequences **pull in opposite directions**:

| Consequence | Pushes capability |
|---|---|
| `CON-4` linkability | **out** of linkable libraries and behind a service boundary, so more consumers can use it without accepting AGPL |
| `CON-5` §13 | an obligation **onto** that same service boundary, the moment it faces anyone outside the organisation |

Neither is avoidable. The tension must be resolved deliberately in `B6` rather than discovered, and
that is the main reason this question exists rather than being left implicit.

## What is currently assumed

The PRD records "exposing the service beyond the organisation" as out of scope. **That scope statement
is a licence decision as much as a product one**, and it is what currently makes `CON-5` cheap. If it
changes, `CON-5` becomes a release-engineering obligation: the deployed artefact must be identifiable
and its source retrievable.

Note that artefact-to-source resolvability is required **anyway** (`CON-5` verification), because
`FR-073`'s upgrade path and `PERF-7`'s baselines both need it. So the incremental cost of external
exposure is the source *offer*, not the traceability.

## What to establish, and in what order

1. **Is there a candidate internal consumer at all?** A named codebase that would embed this capability
   rather than call it. If none exists, this question closes as "no cost" with a revisit trigger.
2. **If one exists, what is its licence position?** An internal codebase with no external distribution
   accepting AGPL is a very different question from one that ships to customers.
3. **Get counsel's reading**, not an engineer's. `CON-4` and `CON-5` are the requirements author's
   reading of the licence text. The determination that the *reference implementation's* licence bars
   this use is well-evidenced — including the licensor's written confirmation — but the AGPL
   consequences for our own module split are an engineering inference about a licence, which is exactly
   the class of inference that should not be relied on.
4. **Record the answer as a decision record** (`QA-21`), including the disliked consequence.

## Options for the split, if a linking consumer exists

### A. Engine stays AGPL; consumers use the service boundary
Simplest. The linking consumer is told to call rather than link.
**Against:** if the consumer needs in-process latency, this is not a workaround — it is a refusal.

### B. Engine stays AGPL; the consumer accepts AGPL
Fine for an internal-only codebase.
**Against:** it propagates the obligation to a codebase whose future distribution nobody controls.

### C. A narrow permissively-licensed contract crate, with the AGPL engine behind it
Types and traits under a permissive licence; the implementation AGPL. The consumer links only the
contract and obtains the implementation at runtime.
**Against:** in Rust this is a dynamic-loading design, which is a substantial commitment, and whether
it achieves the licence separation is precisely a question for counsel rather than for engineering
judgement.

### D. Relicense
Not in scope for this plan, and it is the requester's decision, not the architect's. Recorded so the
option is visible rather than assumed away.

## Recommendation

**Establish step 1 before anything else.** It is a single question to the requester — *is there a
codebase that would embed this?* — and a "no" closes the question at zero cost with a revisit trigger,
while a "yes" makes it one of the more consequential inputs to `B6`.

## Related

- `specs/06-constraints.md` — `CON-4`, `CON-5`, and their not-proven section.
- `analysis/0002-feature-clusters.md` — "What the AGPL split adds".
- `SYNCS.md` — **B6**, which owns the split and is also what unblocks the engine name.
