# Question 0011 — Is generated prose wanted in the wiki, and what groups its modules?

- **Status:** **narrowed 2026-08-20.** The output contract is decided (`FR-036`); two residuals remain.
- **Owner:** the requester, on the prose question · sync **B3** on module grouping
- **Date:** 2026-08-20

## What changed, and the correction behind it

An earlier draft of this question asked *"what is a repository wiki, exactly?"* and concluded that
`FR-036` was not implementable because four incompatible readings were consistent with the capability
list's one-line entry.

**That conclusion was wrong, and it was wrong in an avoidable way.** The reference implementation ships
this capability and its **public documentation** describes the contract — which the clean-room protocol
explicitly permits reading for capability vocabulary. The public behaviour is: a CLI invocation
requiring a language-model API key, which groups files into modules using the model, generates a
documentation page per module plus an overview page, and cross-references them to the knowledge graph.

So a contract was available and I did not look for it. `FR-036` now has one.

## What is now decided, in `FR-036`

A **structured document set**, not a rendering:

- one page per module, plus an overview page linking them;
- cross-references that resolve to graph identities rather than to text;
- the index generation on every page;
- navigable without graph vocabulary;
- **module = a derived cluster** (`FR-010`), not a separately-computed grouping;
- **prose is a separate, optional stage**, gated behind the AI-provider path, and its absence must leave
  a usable document set.

## Residual 1 — is generated prose wanted in v1 at all?

**This is a security-surface decision before it is a product one.**

Prose generation sends substantial code-derived content to a configured AI provider. That makes the
wiki an **egress path for asset A1** (`analysis/0006`), reachable through what looks like a
documentation feature. The corpus already requires the controls — `IF-12` provider configuration,
`IF-13` restrictable to absence, `SEC-11` credential handling, `SEC-13` enumerable egress — so the
question is not whether it *can* be governed but whether it should exist in v1.

| Option | For | Against |
|---|---|---|
| **Prose in v1** | It is what makes the wiki readable by the non-technical persona (`US-N-1`), and it is what the precedent does | Adds a code-egress path, a provider dependency, non-determinism, and a verification method that is a human |
| **Structure only in v1, prose later** | Fully testable; no new egress path; the document set is still navigable and still useful to an engineer | A page of resolved cross-references and no narrative is a graph browser, not a wiki. The non-technical persona may get little from it |
| **Prose, but off by default** | Ships the capability; makes the egress path an explicit administrative act | Two supported output shapes to test and document |

**Note that the third option is what `FR-036` already specifies**, since prose is optional and its
absence must leave a usable set. So the honest reading is that this residual asks whether prose is
built in v1 at all, not how it is governed.

## Residual 2 — do cluster-shaped modules read well?

`FR-036` groups pages by **derived cluster**, deliberately rejecting the precedent's approach of
grouping with the language model. The reasoning is in the requirement: deterministic, testable, reuses a
capability that must exist anyway, and confines the provider to prose.

**The cost is real and is worth stating plainly.** Clusters are optimised for graph cohesion, not for
human readability. A cohesion-optimal partition may cut across the boundaries a person would draw, and
"here are eleven modules, one of which is a cluster of test utilities and one of which is everything
that touches serialisation" is a worse table of contents than a model would produce.

**What would decide it:** generate both for one real repository and have a reader compare. Cheap, and it
is the only evidence that matters. Until then `FR-036` takes the testable option, which is the right
default when the alternative is unmeasured.

**If clusters read badly**, the fallback is not necessarily LLM grouping — a declared structure is a
third option, and in this estate's target corpus it is a strong one. A Rust workspace's crates *are* a
human-authored module decomposition, so grouping pages by workspace member would be deterministic
**and** readable. See `analysis/0007-target-corpus-implications.md`.

## Residual 3 — where does the document set go?

`FR-036` specifies the document set and not its destination. Three possibilities, none decided:

- **Returned to the caller** and rendered by a surface. No new storage; the wiki is a read capability.
- **Written to disk** by `git-ctx`. Useful locally; makes the wiki a build artefact with its own
  staleness relative to the index.
- **Persisted in a store.** Would finally give the search slot a consumer (`GAP-011`), and would make
  the wiki authoritative-or-derived, which `B4` must then place.

The first is the cheapest and forecloses nothing; the third is the only one that changes the store set.

## Recommendation

- **Residual 1:** ask the requester. It is a one-line answer with a security consequence, and `FR-036`
  is already written so that either answer is implementable.
- **Residual 2:** take the testable option now, and generate a comparison against the alternatives on a
  real repository before treating it as settled. Note the target corpus offers a third grouping that may
  dominate both.
- **Residual 3:** return it to the caller in v1. Persisting it is a store-set decision that should not be
  made as a side effect of a documentation feature.

## Related

- `specs/02-functional-requirements.md` — `FR-036`, now with a contract and a two-part verification.
- `specs/04-interfaces-and-external-systems.md` — `IF-12`, `IF-13`, `EXT-4`.
- `specs/05-security-requirements.md` — `SEC-11`, `SEC-13`.
- `analysis/0006-threat-model.md` — asset A1, boundary B4.
- `analysis/0007-target-corpus-implications.md` — why workspace members may be the best module grouping.
- `GAPS.md` — `GAP-016`, narrowed.
