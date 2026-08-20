# Question 0006 — What is in v1, and what is deliberately not?

- **Status:** **decided 2026-08-20** by the requester, on four axes. Open on one residual.
- **Date:** 2026-08-20
- **Purpose:** record the decisions as an auditable artefact, so the SPEC's `WON'T` entries have a
  provenance and are not mistaken for omissions.

## Why this is a question file rather than a note

`PROMPT.md`'s closing note asked the requirements author to **ask** rather than assume, on capabilities
the requester's own list had omitted. Four questions were put and four were answered. Recording them
here means a later reader can tell the difference between *"nobody thought about this"* and *"this was
decided, on this date, for this reason"* — which is the distinction that keeps a `WON'T` from silently
becoming a gap.

## Decision 1 — Statement-level dependence and taint are deferred to v2

**Answered:** defer both. Reachability, blast radius and diff impact are v1 MUSTs.

**Rationale:** statement-level control and data dependence is a different index, a different cost
class, and an interprocedural analysis. Bundling it with symbol-level reachability would make v1's
largest component the one capability with the least immediate demand.

**Recorded as:** `FR-037`, `FR-038` — both `WON'T (v1)`.

**The clause that makes the deferral safe rather than a dead end:** `FR-037` requires v1 to **name the
seam**. The unit of analysis is an explicit parameter of an analysis request, with `symbol` the only
accepted value in v1, and `statement` returning an explicit *not supported in this version* error
rather than a validation failure or a wrong answer. So dependence inserts later rather than forcing a
redesign.

**Revisit trigger:** a consumer asks for source-to-sink reasoning that blast radius cannot answer.

**Note for whoever revisits:** `analysis/0003` records that this is the one deferred capability with
genuinely **readable** permissive precedent — one mature Apache-licensed tool does interprocedural
taint properly. Most of this corpus does not have that luxury, so v2 starts from a better position than
v1 did.

## Decision 2 — Pull-request-shaped diff input is a v1 MUST

**Answered:** MUST. Diff impact accepts a `base...head` ref pair **and** a patch supplied directly for a
repository the service has never checked out.

**Rationale:** it gates pull-request automation entirely, and the grounding measured that the reference
implementation could express **neither** — its comparison mode diffed a ref against the local working
tree and required a checkout.

**Recorded as:** `FR-027`, `FR-028`.

**The consequence, accepted:** it forces repository *acquisition* to be separable from analysis *input*.
That is a seam worth having anyway, and it means the system must map patch context lines onto indexed
symbols without being able to read the post-change file. That mapping is lossy, `GAP-003` records that
it may require a syntax-aware diff, and sync **C3** gates it. `analysis/0003` marks `FR-028` **elevated**
— no precedent anywhere — so this is the decision that added the most risk, deliberately.

## Decision 3 — All seven previously-omitted capabilities are wanted

**Answered:** all three groups wanted. Nothing recorded as `WON'T` on this axis.

| Group | Capabilities | Recorded as |
|---|---|---|
| Traversal-shaped | transitive blast radius with a depth bound; shortest-path trace with a witness | `FR-024`, `FR-023` |
| Web/API-shaped | route-to-handler mapping; RPC and tool-definition mapping; response-shape conformance; pre-change route report | `FR-007`, `FR-008`, `FR-034`, `FR-035` |
| Write-shaped | coordinated multi-file rename | `FR-050` |

**Rename carries a condition, not just an approval:** it is specified **AST-accurate with mandatory
index writeback**, never text-level. The reference's version is inherited-negative #8, and `FR-050`'s
six clauses each correspond to one measured failure.

**Two of the seven are the riskiest additions**, and this is worth stating plainly given the decision
was to take all of them: `analysis/0003` marks response-shape conformance **inaccessible** (precedent
exists only in the reference, which the clean room forbids reading, and it is the capability whose
correctness is least well-defined) and rename **elevated** for the required combination. Both should be
**prototyped rather than designed on paper.**

## Decision 4 — Store slots get capability profiles plus `presumed` candidates

**Answered:** specify each slot as a capability profile, and name candidate products marked `presumed`,
drawn from this estate and from the licence-screened survey.

**Rationale:** the requester's original per-slot product list did not survive into the trigger prompt —
only the slot names did. Naming no products at all would lose the licence and async screening signal;
naming products as if selected would be invention.

**Recorded as:** `EXT-1`–`EXT-6`, with every product marked `presumed`, plus `questions/0010` and
`GAP-010` for confirmation.

## The residual, still open

**Within the v1 MUST set, nothing is prioritised.** `specs/09` records this as a real omission when
assessing the corpus against the external reference's quality criteria: 58 features are MUST and no
ordering distinguishes them.

That is arguably the architect's sequencing decision rather than a requirements one — but it means
**nobody has said which MUST is allowed to slip** if the date pressures the scope. `analysis/0003`
supplies the natural answer if one is wanted: the entangled group of `FR-009`, `FR-010`, `FR-018` and
`FR-011` is both the highest risk and the deepest dependency, so it is the one thing that cannot be
deferred without deferring the product.

**Open question for the requester:** is there a date? If so, which MUSTs are the descope candidates, by
name? A scope statement that names no candidates lets a capability be dropped silently and later
described as never having been in scope.

## Related

- `specs/02-functional-requirements.md` — every requirement these decisions produced.
- `analysis/0003-feature-gaps.md` — the precedent and risk behind decisions 2 and 3.
- `questions/0010-store-compatibility-targets.md` — decision 4's open half.
- `discussions/0001-what-impact-analysis-means.md` — the vocabulary decision 1 and 2 both rest on.
