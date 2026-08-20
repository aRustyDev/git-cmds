# Questions — index

- **Date:** 2026-08-20 · **Status:** living index over [`questions/`](questions/) and
  [`discussions/`](discussions/)
- **The distinction:** a **question** records a fork with a decidable answer. A **discussion** records a
  multi-axis design problem that is not yet one decision, and whose useful output is agreement on what
  would settle it.

## Questions

| # | Question | Status | Owner | Blocks |
|---|---|---|---|---|
| [0001](questions/0001-product-and-crate-naming.md) | Product and crate naming | **partly decided** — CLI is `git-ctx`; engine deferred. **Amended 2026-08-20: `git-ctx` is taken on crates.io** | requester · sync **B6** for the engine | publication, not work |
| [0002](questions/0002-where-does-the-backlog-live.md) | Where does the backlog live? | open — recommends deferring with a revisit trigger | requester | handing off `scheduled` gaps |
| [0003](questions/0003-the-async-decision.md) | Is the store trait async? | open | sync **B7** | the first store implementation |
| [0004](questions/0004-stable-identities-for-derived-structures.md) | Must derived identities be stable across runs? | open — verify the premise first | sync **B3** | `FR-018`'s design; changes it from cost to correctness |
| [0005](questions/0005-agpl-linkability-for-internal-consumers.md) | Does any internal consumer need to *link* the engine? | open | requester, with counsel | shapes sync **B6** |
| [0006](questions/0006-v1-scope-decisions.md) | What is in v1? | **decided 2026-08-20** on four axes; one residual open | requester | — |
| [0007](questions/0007-what-is-the-unit-of-authorisation.md) | What is the unit of authorisation? | open — answer the monorepo question first | sync **B2** + requester | `SEC-4`'s implementation |
| [0008](questions/0008-embedding-provider-and-vector-width.md) | Which embedding provider, and the width policy? | open — recommendation given on the width half | sync **B2** + requester | the vector slot's schema |
| [0009](questions/0009-is-a-tui-wanted.md) | Is a terminal interface wanted? | open | sync **B5** | nothing; changes **B5**'s answer |
| [0010](questions/0010-store-compatibility-targets.md) | Which products are the per-slot targets? | open — ask once, then screen from the profiles | requester → sync **B2** | `EXT-9` screening → `0003` |
| [0011](questions/0011-the-wiki-output-contract.md) | What is a "repository wiki", exactly? | open — answer the AI-provider half first | requester | `FR-036` entirely |

## Discussions

| # | Discussion | Status | Feeds |
|---|---|---|---|
| [0001](discussions/0001-what-impact-analysis-means.md) | What "impact analysis" means | open — **its vocabulary is adopted**; the seven axes remain | sync **A5**, gated by **C3** |
| [0002](discussions/0002-read-write-asymmetry.md) | Is read/write asymmetry the primary seam? | open — five axes, one decisive and unknown | syncs **B1**, **B2**, **B6** |

## The dependency chain that matters most

Most questions are independent. One chain is not, and it ends at a rewrite:

```text
0010 (which products?)
  └─▶ EXT-9 screening record  (analysis/0004, currently empty)
        └─▶ 0003 (async?)      ← must be answered DURING screening, never after
              └─▶ the first store implementation
```

Every step is cheap except the last, and the last is where the house rule applies: *retrofitting async
through a synchronous trait is a rewrite.* **`0010` is therefore the highest-leverage question here**,
despite looking like a bookkeeping one.

## Questions that block a requirement outright

Two, and both are recorded as such in the SPEC rather than papered over:

- **`0011`** blocks `FR-036`. It is the only requirement in `specs/02` with no verification method, and
  `US-N-1` is recorded as not implementable.
- **`0007`** blocks `SEC-4`. And if its answer is finer than repository-level, it **adds** a functional
  requirement to `FR-024` — a traversal blocked by entitlement must return `undetermined` — which does
  not exist yet and would be a contract change for every consumer if added later.

## Answer these three first

Not by importance, by leverage per unit of effort:

| # | Question | Why first | Cost to answer |
|---|---|---|---|
| **0010** | store targets | unblocks the async chain above | one question to the requester |
| **0004** | derived identities | **verify the premise before designing anything.** If derived identifiers turn out to be internal-only, the question is refuted and the hardest algorithmic requirement in the corpus disappears | one check of the intended query surface |
| **0007** | authorisation unit | the monorepo sub-question may eliminate three of four options at no cost | one question to the requester |

`0004` is the one most worth doing today: `analysis/0003` marks the capability it governs as
**elevated** — no precedent anywhere — and the cheapest possible outcome is discovering it is not needed.

## Numbering

Global per kind, sequential, never reused. `questions/0001` and `0002` predate this session;
`0003`–`0011` were filed on 2026-08-20. `discussions/0001` predates this session; `0002` was filed on
2026-08-20. Gaps are expected and are noted rather than renumbered.

## Related

- [`GAPS.md`](GAPS.md) — several questions own a gap: `0009`↔`GAP-001`, `0010`↔`GAP-010`, `0004`↔`GAP-007`, `0001`↔`GAP-014`.
- [`SYNCS.md`](SYNCS.md) — which sync owns which question.
- [`README.md`](README.md) — the plan map.
