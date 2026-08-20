# Question 0007 — What is the unit of authorisation?

- **Status:** open · **Owner:** sync **B2**, with the requester on policy · **Date:** 2026-08-20
- **Blocks:** `SEC-4`'s implementation. `SEC-8` exists to make this gate explicit.
- **And it is not only a security decision** — see below.

## The question

When a principal is authorised to read something, what is the *something*?

- **A repository** — you may see this repository or you may not.
- **A path within a repository** — you may see `services/billing/**` but not `services/payroll/**`.
- **A graph node** — you may see this symbol, edge or derived structure.

## Why it is a functional question, not just a security one

**Per-node authorisation changes every traversal.** A walk that must not reveal an unauthorised node
cannot simply filter its output: the *existence* of a path through a hidden node is itself information,
and omitting it silently produces a false negative — exactly the failure `COR-1` exists to prevent.

So if the answer is per-node, then `FR-024` must be able to return **`undetermined` because the walk
passed through a node the caller may not see.** That is a functional requirement, and **it does not
currently exist.** Nothing else in this corpus has that shape.

Path-level authorisation has a weaker version of the same problem: `FR-032`'s scoping already requires
that a traversal leaving a scoped sub-directory returns `undetermined` rather than `none`, so the
machinery is at least analogous.

**Repository-level authorisation has none of this problem**, because a traversal never crosses a
repository boundary except through the cross-repository edges of `FR-044`, where the boundary is
already explicit.

## Options

### A. Repository-level
The principal's entitlement is a set of repository identities.

**For:** simple; composable with `IF-9`'s per-request visibility; no traversal consequences; matches how
most organisations actually grant code access.
**Against:** a monorepo is one repository. An organisation whose code is in one large repository gets
all-or-nothing, which may be exactly the case that matters most.

### B. Path-level
Entitlement is a set of path patterns within a repository.

**For:** answers the monorepo case; analogous machinery to `FR-032` already required.
**Against:** every node must carry a path, which most do but derived structures do not — a **flow**
spans files, and a **cluster** is a set of nodes across paths. So the entitlement model has no natural
answer for the two derived structures, which are precisely what `FR-021` groups results by.

### C. Node-level
Entitlement is evaluated per node.

**For:** the most expressive, and the only one that can express "you may see this symbol's existence but
not its callers".
**Against:** the traversal consequence above; a per-node decision inside a hot loop, against
`PERF-2`'s 250 ms budget and `SCALE-4`'s 64 concurrent readers; and `analysis/0003` records **no
precedent** for per-node authorisation in a graph-query product.

### D. Repository-level for v1, with the model designed to admit finer grain later
Entitlement is repository-level, but the authorisation call site is a single point (`IF-3`, `SEC-4`) and
the decision input includes the target's path, so a finer grain can be introduced without moving the
call site.

**For:** ships; keeps the traversal simple; does not foreclose B or C.
**Against:** the traversal consequence is deferred, not solved — and adding `undetermined`-on-hidden-node
later means revisiting `FR-024`'s contract, which is a contract change for every consumer.

## What must be true whichever is chosen

1. **The decision is recorded before the first authorisation implementation commit** (`SEC-8`),
   checkable from history.
2. **Read authorisation is a decision, not a filter** (`SEC-4`). Filtering after the fact is how a count
   leaks the existence of what it excluded.
3. **If the answer is finer than repository-level, `FR-024` gains a requirement**: a traversal blocked by
   entitlement returns `undetermined` with that as the reason, and this must be distinguishable from a
   budget truncation, because the two have different remedies for the caller.
4. **The choice is compatible with an external decision point** (`SEC-5`, `EXT-11`). Per-node evaluation
   against a remote policy engine inside a traversal is not viable at `PERF-2`'s budget, so option C
   effectively forces the policy to be local or cached — which is itself a decision with a staleness
   consequence.

## The monorepo question — **answered 2026-08-20**

It was asked as *"is the target corpus many repositories or one large one?"* on the grounds that option A
is adequate for the first and inadequate for the second, and that it was the cheapest thing to establish
before arguing the options.

**Answer: one repository containing many deployable units** — a Rust workspace of library and binary
crates, all under one tree (`analysis/0007-target-corpus-implications.md`).

**Consequences, and they do most of the work this question needed:**

1. **Option A is eliminated.** Repository-level entitlement over a single workspace holding every library
   and every binary is all-or-nothing over the whole codebase. That is not an authorisation model.
2. **Option B has a better formulation than "path".** The natural unit is a **workspace member**. Crate
   boundaries are a *declared*, human-authored decomposition, not a path convention someone may
   reorganise — so entitlement expressed against members is stable in a way that `crates/<name>/**` glob
   patterns are not.
3. **B's stated weakness partly survives.** Derived structures still have no natural home in it: a
   **flow** spans members, and a **cluster** is a set of nodes that may cross member boundaries. So
   entitlement over derived structures needs an explicit rule — most likely "visible only if every
   member it touches is visible", which is conservative and produces `undetermined` rather than a
   partial answer.
4. **Option C is unchanged**, and remains the only one with a traversal consequence and no precedent.

**Revised reading: option B, formulated as workspace-member entitlement, is now the leading candidate**,
with C available where finer grain is genuinely needed. That is a narrowing, not a decision — the
requirement remains that `SEC-8`'s gate is satisfied by a recorded decision before any implementation.

**And the clause that must land with it:** since B is finer than repository-level, `FR-024` gains the
requirement noted in the options above — a traversal blocked by entitlement returns `undetermined` with
that as the reason, distinguishable from a budget truncation. **Add it now rather than later**, because
a contract that gains a new `undetermined` reason after ~10 000 agent consumers exist is a breaking
change for every one of them.

## Recommendation

**None on the unit** — it is structural and policy-bearing, and remains the architect's with the
requester on policy. But the monorepo answer has already done the cheap elimination, so what is left is:

- **Option B as workspace-member entitlement is the leading candidate.** Record it or reject it; do not
  let it become the answer by default.
- **Add the `FR-024` entitlement-`undetermined` requirement now**, since B is finer than
  repository-level and the retrofit cost scales with the consumer count.
- **Decide the derived-structure rule explicitly** — consequence 3 above. A flow that crosses an
  unauthorised member is the case that will be got wrong silently.

## Related

- `specs/05-security-requirements.md` — `SEC-4`, `SEC-5`, `SEC-8`, and `IF-9`.
- `specs/02-functional-requirements.md` — `FR-024`, `FR-032`, and `COR-1`'s three-state contract.
- `analysis/0003-feature-gaps.md` — note 15, on why authorisation is routine generally and absent in this field.
- `analysis/0006-threat-model.md` — adversary T2.
