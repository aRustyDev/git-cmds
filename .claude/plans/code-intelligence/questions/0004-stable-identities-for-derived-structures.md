# Question 0004 — Must derived structures have stable identities across runs?

- **Status:** open · **Owner:** sync **B3**, with requirements input · **Date:** 2026-08-20
- **Blocks:** `FR-018`'s design, and it changes `FR-018` from a **cost** requirement into a
  **correctness** requirement. Interacts with `FR-011`, `FR-012`, `FR-073` and `COR-3`.

## The question

**Flows** and **clusters** are produced by computation over the whole graph, and both are addressable
by the query surface. When an analysis run recomputes them, must a given flow or cluster keep the
identifier it had before?

## Why this is not a performance question

If a derived identifier is part of the query surface — and `FR-009`, `FR-010` and `FR-022` all make it
so — then recomputation that changes identifiers **changes answers, not just cost**. Concretely:

- A cached result referencing a flow becomes wrong rather than stale.
- An agent holding an identifier between calls (`US-G-6`) silently changes subject.
- A saved view or a permalink breaks.
- Two runs cannot be compared, so "what changed in this release" is unanswerable.

The grounding measured exactly this: derived structures recomputed wholesale on every run while their
identifiers were primary keys of the query surface.

## Why it is hard

**A global partitioning algorithm has no natural stable identity.** One added node can re-label
clusters that no changed file touches — the partition is a property of the whole graph, not of any
region of it. So stability is not a matter of remembering to keep an identifier; it is an additional
algorithmic requirement layered on the partitioning.

`analysis/0003` marks this **elevated**: no precedent anywhere. The reference recomputed wholesale. No
permissive tool derives these structures at all, so none has faced the question. And general-purpose
precedent does not transfer, because stable identity under global partitioning is a known-hard problem
rather than an engineering detail.

## Options

### A. Stable identities are required
Derived structures carry an identity that survives recomputation where the structure is "the same"
structure. Requires defining sameness — by membership overlap, by a designated anchor member, by a
content hash over a canonical subset — and each definition has failure cases (a cluster that splits; a
flow whose entry point moves).

**For:** every consumer above works. Cross-run comparison becomes possible, which is itself a
capability nobody has asked for yet and might want (sync **A4**).
**Against:** it is the hardest single algorithmic requirement in the corpus, with no precedent, and the
sameness definition will be wrong in cases nobody anticipated.

### B. Identities are per-generation, and the surface prevents holding them
Identifiers are scoped to an **index generation**. Any request carrying an identifier from a different
generation is **rejected**, not silently answered.

**For:** implementable immediately, and it is honest — the identifier means what it says.
**Against:** every consumer must handle generation invalidation, agents cannot hold references across a
reindex, and cross-run comparison is impossible. It pushes the cost onto ~10 000 agents.

### C. Stable where cheap, per-generation otherwise
Flows may be stabilisable — they are anchored on an entry point, which is a real symbol with a real
identity — while clusters may not be, since a partition has no anchor.

**For:** plausibly matches the actual difficulty, and the two structures genuinely differ.
**Against:** two contracts for two things that look alike to a consumer. `COR-3` would then have to be
tested twice with different properties, and the surface must make the difference visible or it is a
trap.

## What must be true whichever option is chosen

These are requirements, not preferences:

1. **The choice is tested** (`COR-3`). The unacceptable outcome is neither branch: identifiers that
   happen to be stable, relied on informally, and churning at a bad moment.
2. **Identifier churn is reported** (`FR-018`'s verification). A run whose derived identities changed
   must say so, whether or not stability was promised.
3. **The contract is visible at the surface.** A consumer must be able to tell from the response whether
   an identifier is durable, without reading documentation.
4. **`FR-073` interacts.** If identities are authoritative, they must be migrated on upgrade; if
   per-generation, they may be discarded. This determines which side of the
   authoritative/derived split they fall on — see `analysis/0004`'s placement table, where this is the
   row that constrains most and looks least constraining.

## First step

**Verify the premise before designing either answer.** `GAP-007` records it as `inferred`, and its
verification is: *confirm that derived identifiers are (or will be) externally visible.* If they turn
out to be purely internal — if the query surface can address flows and clusters by their members rather
than by an identifier — **this question is refuted and the problem disappears.**

That check is cheap and nobody has done it. It should precede any work on options A–C.

## Related

- `specs/02-functional-requirements.md` — `FR-009`, `FR-010`, `FR-018`.
- `specs/03-non-functional-requirements.md` — `COR-3`.
- `analysis/0003-feature-gaps.md` — note 6, and why this clusters with `FR-011` as one risk.
- `GAPS.md` — `GAP-007`.
