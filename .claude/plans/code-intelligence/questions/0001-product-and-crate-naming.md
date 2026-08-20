# Question 0001 — Product and crate naming

- **Status:** **partially decided 2026-08-19.** The CLI is **`git-ctx`**. The engine-library name is
  **deferred** — see the gate below.
- **Date:** 2026-08-19
- **Blocks:** nothing. The CLI name is settled, and the engine name blocks only publication to a
  registry.

## Decision — the CLI is `git-ctx`

Settled by the requester, 2026-08-19. Use `git-ctx` throughout; it is not a placeholder.

The candidate it beat was `git-graph`, and the reason matters enough to record because it will come up
again: **"git graph" already means the commit DAG** to every git user (`git log --graph`). This
product's graph is a code-structure graph — a different object. That name would have invited users to
expect history visualisation and to be surprised by symbol references, and it needed registry
clearing besides.

`git-ctx` also matches what the tool actually provides a caller: the capability list's own term for
the 360-degree symbol view is *context*. The residual weakness, recorded so nobody rediscovers it: a
`-ctx` suffix conventionally signals *context switching* (`kubectx`-style), so some users may expect
identity- or config-switching. Judged acceptable.

## Deferred — the engine-library name, and why deferring is correct

**Gate: decide the engine name once the mapping of engine components, module members, domains,
features and seams is drafted.** Practically, that means after the seam pressure test and the
library/SDK/binary split (syncs S3 and S5 in `PROMPT.md`).

This is not scheduling convenience. **You cannot name the engine until you know what is inside it.**
A library name is a claim about scope, and the scope is exactly what the seam work decides. Naming
first tends to produce one of two failures:

- the name is narrower than the crate becomes, and the crate accretes things its name disowns; or
- the name is a vague abstraction chosen to be safe, which is how `-core` suffixes happen — and there
  is **no `-core` anywhere in this estate**, deliberately.

House precedent supports the deferral: the estate's engine library carries a real brand name
(`orrery`) distinct from its binary (`muster`), which is only possible because the engine's boundary
was settled first.

## The distinction that made this two decisions rather than one

This repository's premise is *"Collection of Crates (Lib/SDK/Bins) for building and running git
subcommands"* — so there is a user-facing verb and, separately, whatever the reusable library is
called. They are different kinds of commitment:

| Slot | What it names | Kind of commitment | Status |
|---|---|---|---|
| Subcommand | What a developer types | UX. Renameable with a deprecation cycle | **`git-ctx`** ✅ |
| Engine library | The reusable analysis contract | **API stability.** Published AGPL-3.0; renaming after publish is a breaking change | deferred ⬜ |
| Orchestration / SDK | The layer above the engine | House convention `<engine>-sdk` or `<product>-sdk` | follows the engine ⬜ |
| Delivery crates | Server, wire types, UI adapter | House convention `-server` / `-types` / `-ui` | follows the engine ⬜ |

Keeping them separate means the CLI can be renamed for UX reasons without breaking a published
library API — which is the practical argument, and it is stronger here because the library is AGPL, so
its name reaches anyone who links it.

## Placeholder discipline until the engine is named

- Write **`git-ctx`** wherever the CLI or the subcommand is meant. Not a placeholder.
- Write **`<ENGINE>`** wherever the engine library is meant, and leave it visibly unresolved.
- **Do not half-rename a document.** A spec that says `git-ctx` in some places and `<ENGINE>` in
  others is correct; one that has silently adopted a guessed engine name in half its sections is not.

## Still to verify before publishing anything

- Registry availability for whatever the engine ends up called.
- Whether `git-ctx` collides with an existing git subcommand or crate — cheap to check, not yet done.

## Notes

The AGPL-3.0 licence interacts with this: whatever the engine crate is called, publishing it means
publishing an AGPL library, and internal consumers must accept that to link it. See the
implementation-constraints section of the SPEC.

## Amendments

- **2026-08-19** — CLI decided as `git-ctx`. Engine name deferred behind the seam-mapping gate.
  Original question was "what is this called — and is that one name or two?"; the answer to the
  second half is **two**.
