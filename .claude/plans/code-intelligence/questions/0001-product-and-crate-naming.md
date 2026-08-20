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
library/SDK/binary split — syncs **B1** and **B6** in [`SYNCS.md`](../SYNCS.md).

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
- ~~Whether `git-ctx` collides with an existing git subcommand or crate — cheap to check, not yet
  done.~~ **Checked 2026-08-20. It collides. See the amendment below.**

## ⚠️ `git-ctx` is taken, and by something with the semantics this document worried about

**Checked 2026-08-20 against the crates.io API.** A crate named exactly `git-ctx` exists and is live:

| Field | Value |
|---|---|
| Name | `git-ctx` — exact match |
| Description | *"A git custom command to list and switch most recent branches"* |
| Version | 0.1.1, MIT |
| First published | 2022-02-28 · last updated 2022-03-08 |
| Downloads | 2,838 total, 13 recent |
| Status | **published, not yanked** |
| Repository / homepage | none declared |

**Two distinct problems, and the second is worse than the first.**

1. **Registry collision.** The name cannot be published to crates.io. A binary crate publishing as
   `git-ctx` is refused. This is a blocker for publication only, not for local work — but note that
   `questions/0001`'s own table marks the CLI as UX-renameable *"with a deprecation cycle"*, and that
   assumption is cheaper before anything ships than after.
2. **Semantic collision, and it is exactly the residual weakness this document already recorded.** The
   text above says: *"a `-ctx` suffix conventionally signals context switching (`kubectx`-style), so
   some users may expect identity- or config-switching. Judged acceptable."* The existing crate **is a
   branch switcher**. So the risk is no longer hypothetical: a user who installs both gets two tools
   competing for `git ctx`, and the incumbent does the context-switching thing the suffix implies.

**What this does and does not change:**

- **It does not change the decision.** `git-ctx` is written literally throughout the corpus, as
  instructed. Renaming on the requirements author's authority would be exactly the half-rename this
  document forbids.
- **It does mean the decision was taken without this evidence.** The requester judged the `-ctx`
  ambiguity acceptable against a hypothetical; it is now a live conflict with a published tool.
- **Low incumbency is a real mitigation.** 13 recent downloads, no repository URL, untouched since
  March 2022. This is a dormant crate, not a popular one. Options include a different crate name for the
  same subcommand (`cargo` allows the binary name to differ from the crate name), a different
  subcommand verb, or contacting the owner.

**Filed as `GAP-014`.** Owner: the requester. It is not blocking — nothing is published and nothing is
built — and it should be settled before the first release rather than at it.

## Notes on method

The check was two API calls: a search for the name, then the crate detail for version, licence,
download counts and dates. Recorded because the previous state of this file was *"cheap to check, not
yet done"* — and it was indeed cheap, which is the argument for doing the remaining verification item
(engine-name availability) at the moment the engine is named rather than later.

## Notes

The AGPL-3.0 licence interacts with this: whatever the engine crate is called, publishing it means
publishing an AGPL library, and internal consumers must accept that to link it. See the
implementation-constraints section of the SPEC.

## Amendments

- **2026-08-19** — CLI decided as `git-ctx`. Engine name deferred behind the seam-mapping gate.
  Original question was "what is this called — and is that one name or two?"; the answer to the
  second half is **two**.
- **2026-08-20** — **`git-ctx` verified as taken on crates.io**, by a 2022 MIT crate that is a git
  subcommand for listing and switching recent branches. The registry name is unavailable and the
  `-ctx`-means-context-switching risk this document recorded as acceptable is now a live conflict with
  a published tool rather than a hypothesis. The decision stands as written — renaming is the
  requester's — and the finding is filed as `GAP-014`. The remaining verification item (engine-name
  availability) is unchanged and still owed, at the moment the engine is named.
