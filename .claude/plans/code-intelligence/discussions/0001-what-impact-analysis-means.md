# Discussion 0001 — What "impact analysis" means

- **Status:** open — needs a decision before `specs/02-functional-requirements.md` can be written
- **Date:** 2026-08-19
- **Audience:** the requirements author and the Software Architect, jointly
- **Blocks:** the impact requirements, the diff-impact requirements, and any PR-automation capability

## Why this needs settling first

"Impact analysis" appears in the capability list as if it were one feature. It is not. It is at least
seven independent decisions, and the combinations are not interchangeable — several of them produce
tools that answer *different questions* while sharing a name.

It also drives module shape directly, which is why it lands in front of the architect and not just
the requirements author. If impact is one thing, it is one component. If it is a shared traversal
core with several projections layered on top, that is a library-versus-SDK seam, and the shape of the
core's public contract is decided by how many projections have to sit on it.

## The evidence that prompted this

Two measured findings from the grounding of the reference implementation. Both are behavioural; no
internals are reproduced here, so this document is safe for a clean-room reader.

1. **Its diff-impact and its symbol-impact are different mechanisms wearing one name.** The
   symbol-oriented one performs a real bounded graph walk with a direction and a depth limit. The
   diff-oriented one performs a **single hop** against a precomputed membership table — it answers
   "which precomputed flows does this symbol belong to?", not "what does changing this reach?" The
   two were chained only by prose instructions to the calling model, not by code.
2. **Its risk verdict was a count ladder over one projection.** Risk was derived purely from how
   many precomputed flows were touched. A changed symbol belonging to no flow therefore reported zero
   affected and *low* risk — even with many direct callers. That is the failure mode to design out:
   **risk must not be a function of a single countable projection.**

A third finding is the most important one, and the reference got it *right*: it paired an empty
result with an explicit **UNKNOWN** verdict and a note that an empty caller set is not evidence of no
callers, because dynamic dispatch, property access on untyped objects, reflection and cross-language
calls are all invisible to the walk. Preserve that instinct.

## The seven axes

### 1. Direction

Upstream ("who reaches me — what breaks if I change this") and downstream ("what do I reach — what
must exist for this to work") are different queries with different consumers. Upstream serves change
safety; downstream serves comprehension and dependency review. Decide whether both are required,
whether either is the default, and whether a bidirectional mode exists.

### 2. Unit of analysis

File · symbol · statement. These are not refinements of one another — they need different indexes and
have different costs. Statement-level dependence (control and data) is a materially larger commitment
than symbol-level call reachability, and the capability list asks for **both** (statement-level
control/data dependence is named separately). Decide whether they share one contract or are separate
capabilities that happen to be adjacent.

### 3. Edge admissibility — which relationships count as "impact"

The candidate set is much larger than "calls":

| Edge class | Include by default? |
|---|---|
| Direct calls | almost certainly yes |
| Imports / module dependency | ? |
| Inheritance, interface implementation, method override | ? |
| Dependency injection and framework wiring | ? |
| Data flow / reaching definitions | ? |
| Route-to-handler, handler-to-consumer | ? |
| Cross-repository contract links | ? |
| Test-to-subject | ? |

This is the single highest-leverage decision, because it sets both the false-positive rate and the
cost. The reference kept framework-wiring and conditional-configuration edges **out** of its impact
defaults and made them opt-in — a defensible call, and one worth making deliberately rather than
inheriting. Decide whether the answer is a fixed default set, a caller-supplied filter, a named
profile ("safety", "comprehension", "review"), or all three.

### 4. Transitivity and depth

One hop · N hops · unbounded with a cost ceiling. And if bounded: is the bound a **correctness
statement** ("we assert nothing beyond depth N") or a **budget** ("we stopped at N and there may be
more")? Those must be distinguishable in the output, because the second is a truncation and the first
is an answer. Also decide whether depth is uniform or per-edge-class — inheritance may deserve
unbounded traversal where imports do not.

### 5. Input shape

- A symbol, by name or stable id
- A file, or a file and a line
- A working-tree diff
- Two refs — `base...head`
- A patch or diff supplied directly, for a repository the service has never checked out

**The last two are what a pull-request integration actually needs, and the reference could express
neither** — its comparison mode diffed a ref against the local working tree and required a checkout.
If PR automation is wanted at any point, this axis is a hard requirement, not a nicety.

### 6. Output projection

The same traversal can be projected as: affected symbols · affected files · affected flows or
processes · affected API routes · affected tests · affected downstream repositories · a ranked risk
summary · a human-readable narrative. Decide which are required, which are derived, and — critically
— **whether the projections share one traversal or each get their own.** One traversal with N
projections is a library with a stable core. N traversals is how the reference ended up with two
incompatible impact mechanisms and, separately, three divergent implementations of its result-ranking
fusion.

### 7. Soundness posture — the one that matters most

Is the analysis **sound** (no false negatives; an empty answer means genuinely nothing) or
**heuristic** (best-effort; an empty answer may mean the walk could not see)? Full soundness is not
achievable across dynamic dispatch, reflection, untyped property access, string-keyed routing and
cross-language boundaries.

Therefore the requirement is not "be sound" — it is **"never let an inconclusive result be read as a
clean one."** Concretely, the output must distinguish at least three states:

- **affected: the following** — a positive result
- **nothing affected** — a genuine negative, only claimable where the walk was complete
- **could not determine** — the walk was truncated, degraded, or met a construct it cannot follow

An agent acting on "nothing affected" when the truth was "could not determine" is the specific
dangerous outcome. Whatever the eventual answer, this distinction must be in the contract, must be
machine-readable, and must not be collapsible into a numeric score.

## Three cross-cutting concerns

**Cross-repository.** The capability list wants cross-repo analysis and a contract registry. Decide
whether impact crosses repository boundaries by default, on request, or never — and what confidence
attaches to a cross-repo edge inferred from a contract rather than observed in code.

**Index staleness.** Impact computed against a stale index is confidently wrong, which is worse than
unavailable. Decide whether an impact response must carry the index's freshness, and whether a stale
index degrades the answer to "could not determine" or merely annotates it.

**Cost and abuse.** Unbounded transitive traversal on a large graph is an expensive operation
reachable by any caller. With up to ~10 000 mostly-read-only agents in the target profile, the
bounding strategy is a capacity-planning input, not just a correctness one.

## A proposed vocabulary

The requester's own SPEC guidance asks for consistent terminology. These four terms are distinct and
should not be used interchangeably anywhere in the SPEC:

| Term | Means |
|---|---|
| **Reachability** | Does a path exist from A to B, under a stated edge set. A yes/no with a witness path. |
| **Blast radius** | The set reachable *from* a change, upstream, under a stated edge set and depth. Answers "what might break". |
| **Dependence** | Statement-level control and data dependence within and across procedures. A different index and a different question. |
| **Diff impact** | Blast radius whose *input* is a change set rather than a symbol. A projection over blast radius, not a separate mechanism. |

If the SPEC adopts these, then "impact analysis" as a phrase should not appear in a requirement at
all — it is a category, not a capability.

## What must be decided, and by whom

| Decision | Owner | Notes |
|---|---|---|
| Which of the four vocabulary terms are in scope for v1 | requester | Dependence is the largest; it may defer |
| Default edge admissibility set, and whether profiles exist | architect, with requirements input | Axis 3 — highest leverage |
| Whether PR-shaped input (`base...head`, or a supplied patch, no checkout) is required | requester | Gates PR automation entirely |
| Bounded-versus-budget semantics, and how truncation is signalled | architect | Must be machine-readable |
| The three-state result contract, and that it cannot be collapsed to a score | **non-negotiable requirement** | Write it as a MUST |
| One traversal with projections, or several | architect | This is the module seam |
| Cross-repo default, and confidence for contract-inferred edges | architect | Depends on the group/contract capability |

## How we will know we got this wrong

- Two components in the final design both walk the graph to answer an impact-shaped question.
- Any consumer has to read prose rather than a field to learn whether an empty result was conclusive.
- A risk score exists that can be low while the underlying walk was truncated.
- Someone asks "can this answer a pull request?" and the answer requires a local checkout.
