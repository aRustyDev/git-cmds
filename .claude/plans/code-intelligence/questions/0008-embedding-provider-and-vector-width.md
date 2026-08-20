# Question 0008 — Which embedding provider, and what is the vector-width policy?

- **Status:** open · **Owner:** sync **B2**, with the requester on the provider · **Date:** 2026-08-20
- **Blocks:** the vector slot's schema. Vector width is **frozen at index creation**, so this is a
  migration event rather than a configuration change once anything is built.

## Two questions, and the second is the load-bearing one

1. **Which provider?** A remote inference endpoint, a local in-process runtime, or both.
2. **What happens when the width changes?** Because it will — a better model, a different provider, a
   deployment with different hardware.

## Why width is a policy question rather than a number

The vector store fixes the dimensionality when the collection or table is created (`EXT-2`). So:

- Two providers' vectors are **not comparable**, even at the same width. `EXT-7` clause 1 therefore
  requires provider identity to be recorded with the vectors.
- Changing provider or model invalidates every stored vector.
- The invalidation is **silent unless something checks**: a query embedded by provider B searching
  vectors written by provider A returns plausible, wrong results. Not an error — worse than an error.

**So the policy must state what happens on a width or provider change**, and the options differ in cost
by orders of magnitude.

## Options for the width-change policy

### A. Full re-embed on any provider or width change
Detect the mismatch, refuse to serve semantic results, re-embed everything.

**For:** simple, and correct. The detection requirement is small — provider identity plus width, stored
with the index, compared at open.
**Against:** re-embedding a repository at `SCALE-1` is a provider call per embeddable node. That is the
most expensive routine operation in the system, and it is triggered by what looks like a configuration
change.

### B. Side-by-side, with a migration window
Both widths coexist; new vectors are written at the new width; queries use whichever matches the
configured provider; the old set is dropped when re-embedding completes.

**For:** no loss of semantic search during migration, which matters if agents depend on it.
**Against:** the vector slot's capability profile grows a multi-collection requirement, and
`EXT-2`'s conformance suite must cover it. Roughly doubles the slot's complexity for a rare event.

### C. Refuse the change
Width and provider are fixed at deployment; changing them requires a new index from empty.

**For:** zero mechanism. Honest.
**Against:** in practice this means a full reindex including parse and graph construction, not just
re-embedding — which is `FR-073`'s failure mode arriving through a side door. **This option looks
cheapest and is the most expensive.**

## What must be true whichever is chosen

1. **Provider identity and width are recorded with the index** and checked on open (`EXT-7` clause 1).
   A mismatch must be detected, not discovered.
2. **A mismatch degrades explicitly.** Semantic ranking reports itself absent (`FR-021`); it does not
   return results computed against incomparable vectors.
3. **`FR-073` is not violated.** A provider change may force re-embedding; it must not force a **parse
   and graph** rebuild. Embeddings are derived data (`REV-4`), and this is a case where the
   authoritative/derived split earns its keep.
4. **Re-embedding is resumable** (`FR-016`). At `SCALE-1` it is long enough that an interruption is
   expected, not exceptional.

## The provider question

`EXT-7` already fixes four requirements regardless of which provider is chosen, and each corresponds to
a measured prior-art failure:

| Requirement | The measured failure |
|---|---|
| Provider identity recorded with vectors | mixing two providers' vectors silently |
| Private certificate authority supported | a remote-provider client with **no** private-CA story, using a bare default HTTP client |
| No model artefact fetched from a public network at first use, in a restricted deployment | weights downloaded at runtime from a public host, with none vendored |
| Misconfiguration fails loudly | a configuration error **swallowed**, so semantic search returned zero results with no diagnostic |

**The fourth is the one to hold onto.** A provider configured but unusable, returning empty results
quietly, is indistinguishable from a corpus with no matches — and an agent cannot tell.

### What is undecided

- **Remote, local, or both.** A local runtime avoids an egress path (`SEC-13`) and constrains the model
  to what runs on the host; a remote endpoint is the expected internal-inference deployment here.
- **Whether the local shape defaults to no embeddings at all.** Semantic ranking is one of three lanes
  in `FR-021`, and the requirement already covers a lane being absent. A local default of
  lexical-plus-traversal, with embeddings opt-in, is plausible — and it would make `PERF-3`'s tighter
  budget easier. Nobody has decided.
- **Whether an embeddable-node cap exists.** If a repository at `SCALE-1` has more embeddable nodes than
  is economical to embed, either the cap is explicit and reported, or embeddings quietly cover part of
  the corpus. **The second is unacceptable** and it is a live risk: the grounding recorded prior art
  where a default run on a large repository embedded **nothing at all** because of an
  undocumented node-count cap, and the resulting empty semantic results had no diagnostic.

## Recommendation

**Option A for the width policy**, with two provisos, because it is correct and the mechanism it needs
is small:

- The detection half is required by `EXT-7` anyway, so A's incremental cost is only the re-embed path,
  which `FR-016`'s resumability already requires.
- B should be revisited if it turns out that agents depend on semantic ranking heavily enough that
  losing it during a migration is unacceptable. That is a question about consumer behaviour and there
  is no data on it yet.

**On the provider: no recommendation** — it depends on the internal inference plane, which is the
requester's to name.

**On the cap: it must be explicit and reported.** That is not a recommendation, it is `FR-021`'s
degradation requirement applied to this case, and the measured failure above is why.

## Related

- `specs/04-interfaces-and-external-systems.md` — `EXT-2`, `EXT-7`.
- `specs/02-functional-requirements.md` — `FR-016`, `FR-021`, `FR-073`.
- `analysis/0004-store-capability-matrix.md` — the vector slot's hazards.
- `analysis/0006-threat-model.md` — B4, the provider egress boundary.
