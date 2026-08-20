# Finding 0001 — `kin` is not a store candidate. It is a peer implementation of this product.

- **Date:** 2026-08-20 · **Status:** discovered; **unassessed**
- **Bears on:** the premise of this whole plan, not on any single requirement
- **Escalates to:** the requester, via sync **A4** and the build-versus-adopt decision the licensing
  determination originally framed

## What was asked, and what turned up

`kin` was the tenth entry on the graph-store candidate list and the one entry
`analysis/0008` could not identify — no graph database by that name exists on the Rust package
registry. The requester supplied two locations. They resolve to something that is **not a store**.

Its own description, verbatim:

> *"The system of record for AI-written software. A persistent graph of entities, relationships,
> changes, and provenance, so humans and AI agents see what a change touches before it merges."*

And from its site: *"software that remembers itself"* — a queryable semantic graph in which *"every
entity — class, function, struct, interface — is registered"*, indexed as rich symbols rather than text
chunks, exposed through a local CLI against a standing daemon, and *"through MCP, so Claude, Cursor and
Gemini inspect the graph directly."*

| | |
|---|---|
| **Language** | Rust |
| **Licence** | **Apache-2.0** — permissive, with a separate commercial "KinLab" for teams |
| **Version** | 0.5.19, dated 2026-08-10 |
| **Shape** | local CLI plus daemon; MCP surface; hosted collaboration tier |
| **Adoption** | 46 stars, ~2,400 commits, actively developed |
| **Query language** | **no evidence of Cypher** |

## Why this matters more than a mis-filed candidate

Read that description against this corpus. It claims: a repository parsed into a graph of entities and
relations · impact analysis framed as *"what a change touches before it merges"* · an MCP surface for
agents · a CLI · agents as a first-class consumer.

**That is substantially the product `specs/**` specifies — in Rust, under a permissive licence,
already existing.**

This plan's premise is that a capable reference implementation exists and cannot be used, because it is
PolyForm Noncommercial and its licensor confirmed internal commercial use requires payment. The options
framed at the time were: buy the licence, adopt permissive alternatives, stop, or a managed service — and
the permissive-alternatives survey concluded that **nothing permissive spanned both halves of the
capability**, and nothing reproduced flow or cluster derivation.

`kin` was not in that survey. It plausibly did not exist in a usable form when the survey was run: it is
at 0.5.x, dated three months ago. **So the finding is not that the survey was wrong — it is that the
survey has expired.**

## What this does NOT establish

Stated first and firmly, because the temptation is to over-read a good README — and this corpus has
already recorded, twice, the exact failure mode of doing that.

1. **Nothing here has been read or run.** This is registry metadata plus the project's own marketing.
   `analysis/0003` note 19 applies with full force: **public descriptions are evidence of contract, never
   of mechanism.** The claim *"see what a change touches"* is almost word-for-word the claim the grounding
   measured, in the other tool, to be **a single hop against a precomputed table** rather than a
   traversal. Assume nothing about depth, direction, soundness, or the three-state result.
2. **It is very early.** 0.5.x, 46 stars. `analysis/0008` declined four store candidates on adoption
   grounds an order of magnitude *above* this. Applying a different standard here would be inconsistent.
3. **Open-core is a licence question, not a licence answer.** Apache-2.0 core plus a commercial tier means
   the boundary matters: which capabilities are in the permissive core and which are the paid product?
   `EXT-8` clause 3 requires assessing a grant rather than a category, and the grounding recorded prior
   art where the single most valuable capability *was* the vendor's flagship paid feature. **That is the
   first thing to check, before any capability comparison.**
4. **No Cypher.** So it would not satisfy `FR-020` as written, and probably not `FR-021`'s traversal lane
   in the form specified.
5. **Unknown against most of this corpus:** flows and clusters, dependence and taint, hybrid search with
   semantic ranking, cross-repository contracts, per-principal identity, the three-state result contract,
   durable queued indexing, and every non-functional requirement in `specs/03`.

## One thing it does establish cheaply

**`CON-1` does not apply to it.** The clean room is specific to one PolyForm-licensed codebase. `kin` is
Apache-2.0, so reading it, depending on it, forking it or vendoring it are all permitted, and nobody who
reads it becomes tainted. Anyone tempted to over-apply the clean room here should not.

That asymmetry is worth naming plainly: **this corpus forbids reading the tool it is replacing and
permits reading the tool that may replace it.**

## What should happen, in order

1. **Check the open-core boundary.** Which capabilities are Apache-2.0 and which are KinLab? One reading
   of the repository and the pricing page. If the graph and the impact analysis are behind the commercial
   tier, this collapses into the same shape as the original problem and the answer is quick.
2. **Test the impact claim specifically.** Give it a change and ask what it reaches. Establish whether it
   is a bounded transitive walk with a direction, and whether it can distinguish *nothing affected* from
   *could not determine*. **That single property is the one this corpus treats as non-negotiable**
   (`COR-1`), and it is the one the prior art got wrong while claiming otherwise.
3. **Then, and only then, a capability comparison** against `analysis/0001`'s inventory — with the
   `inaccessible` and `elevated` rows first, since those are where building is most expensive and adopting
   would save most.
4. **Escalate the result to the requester as a premise question**, not an architecture one. Whether to
   build, adopt, extend or contribute is not the architect's call and is certainly not the requirements
   author's.

## The honest framing for the requester

This does not mean stop. It means **the build-versus-adopt comparison was made against a survey that has
since expired**, and a candidate now exists that is closer to the target than anything the survey found —
same language, permissive licence, agent-first, already shipping.

It may well fail steps 1 or 2 above. Four store candidates were declined today on adoption grounds this
project would also fail. But the comparison is cheap and the cost of not making it is building a large
system beside one that already does part of the job.

**The disliked consequence, recorded per house convention:** if `kin` turns out to be a good fit, a
substantial part of this requirements corpus becomes an evaluation checklist and a gap list against
someone else's roadmap, rather than a specification for something we build. That is a worse outcome for
the effort already spent and a better outcome for the organisation, and those two facts should not be
confused with each other.

## Related

- `analysis/0008-graph-slot-screening.md` — where `kin` was recorded as unidentifiable.
- `questions/0010-store-compatibility-targets.md` — the candidate list it arrived on.
- `analysis/0003-feature-gaps.md` — note 19, on public descriptions as evidence of contract and not
  mechanism; and the permissive-alternative column this finding dates.
- `GAPS.md` — `GAP-023`.
- `SYNCS.md` — **A4** is the generative sync this belongs to; Track **C**'s outcome vocabulary
  (adopt · vendor · emulate · take the UX only · decline) is the right frame for the decision.
