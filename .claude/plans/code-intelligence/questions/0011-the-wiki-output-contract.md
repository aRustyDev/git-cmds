# Question 0011 — What is a "repository wiki", exactly?

- **Status:** open · **Owner:** the requester · **Date:** 2026-08-20
- **Blocks:** `FR-036` entirely. It is **the one requirement in `specs/02` with no verification
  method**, and `US-N-1` is recorded as not implementable because of it.

## The question

The capability list's first entry is *"generate a repository wiki from the knowledge graph"*. That names
an output and says nothing about its contract. At least four incompatible things are consistent with the
phrase:

| Reading | Output | Consumed by |
|---|---|---|
| **A static artefact** | a set of generated files, written once per index generation | a docs site, a repository, a browser |
| **Live pages** | rendered on request from the current index | the web UI |
| **Generated prose** | an AI provider summarises graph structure into narrative | a human reader |
| **A structured document model** | a machine-readable outline the web UI renders | the web UI, and other consumers |

These are not refinements of one another. They differ in where the work happens, what is stored,
whether an AI provider is involved, and whether the output can go stale independently of the index.

## Why it cannot be guessed

Each reading changes different requirements:

| Reading | What changes |
|---|---|
| Static artefact | Becomes **derived data with its own generation**, so `FR-039`'s freshness applies to the artefact *and* the index — two staleness notions, and a consumer must be able to tell which it is looking at. Also needs somewhere to be written, which the store slots do not currently cover. |
| Live pages | It is a read capability with a rendering budget. `PERF-4`'s web-UI budget would have to cover a whole-repository summary, which is a much larger query than the interactive ones the budget was derived from. |
| Generated prose | It becomes an **AI-provider egress path** (`SEC-13`, `IF-12`) sending substantial code-derived content to a provider, and its output is non-deterministic — so `QA-1`'s hand-written expectations do not apply and it cannot be snapshot-tested either. **This reading changes the security surface, not just the feature.** |
| Structured model | It is the cheapest and the least like a "wiki". It pushes presentation entirely into `IF-11`'s contract. |

**The third reading is the one that must not be adopted by accident.** A wiki that quietly involves an
AI provider is a code-egress path arriving through a documentation feature, and `analysis/0006` ranks
source code and its derivatives as asset A1.

## What is known about intent

Very little, and it is worth being explicit about that:

- It is listed under **"Graph and query"** in the capability list, alongside read capabilities — which
  weakly suggests a read rather than a build artefact.
- `US-N-1` and `US-N-2` place it with the **non-technical** persona, so whatever it is, it must be
  navigable without graph vocabulary.
- The prior art has an equivalent capability, so precedent exists — but `analysis/0003` marks it
  **inaccessible**: the clean room forbids reading it, so precedent proves feasibility and supplies no
  design.

## What `FR-036` already fixes, regardless

Three clauses hold under every reading, and they are the requirement's current content:

1. It is **derived from the knowledge graph** — not from source text directly, and not from a separate
   documentation source.
2. It is **navigable without graph vocabulary** — the P4 constraint.
3. It **states the index generation it was generated from** — so a reader can tell what it describes.

## What a good answer includes

- **Which of the four readings**, or which combination.
- **Whether an AI provider is involved.** If yes, this becomes an `IF-12`/`SEC-13` concern and needs
  the same administrative restriction as any other provider path.
- **Whether output is persisted**, and if so, in which store slot — because none of the six currently
  holds documents, and `EXT-4`'s search slot is the only candidate, which would finally give that
  slot a consumer (`GAP-011`).
- **What "good" looks like**, because this is the only capability in the corpus whose quality is
  subjective. Every other requirement has a testable pass condition; a wiki's usefulness does not.
  **A verification method is what `FR-036` is missing**, and an honest one may be "a named human judges
  a fixture repository's output acceptable" rather than an automated assertion.

## Recommendation

**Answer the AI-provider question first**, independently of the rest. It is a security-surface decision
with an owner, it is a yes/no, and it determines whether this capability is a rendering concern or a
provider-egress concern. The other three axes can then be decided on product grounds.

**Interim position, if no answer is forthcoming:** treat `FR-036` as the **structured document model**
reading — the cheapest, with no AI provider and no new store — and let `IF-11`'s web-UI contract own the
presentation. That keeps the requirement implementable and forecloses nothing, and it should be recorded
as an interim decision with a revisit trigger rather than allowed to become the answer by default.

**What must not happen:** `FR-036` shipping as generated prose because that was the easiest thing to
build, thereby adding a code-egress path nobody reviewed.

## Related

- `specs/02-functional-requirements.md` — `FR-036`, and its explicit "currently unverifiable" note.
- `specs/07-use-cases.md` — `US-N-1`, recorded as not implementable.
- `specs/04-interfaces-and-external-systems.md` — `IF-11`, `IF-12`, `EXT-4`.
- `analysis/0006-threat-model.md` — asset A1 and boundary B4.
