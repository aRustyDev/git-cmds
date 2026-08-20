# Question 0001 — Product and crate naming

- **Status:** open — candidates supplied, decision outstanding
- **Date:** 2026-08-19
- **Blocks:** nothing hard. Use a marked placeholder and proceed; renaming crates before first
  publish is cheap. It blocks only the point at which anything is published to a registry.

## The question

What is this called — and is that one name or two?

Candidates supplied by the requester: **`git-graph`** and **`git-ctx`**.

## The distinction that has to be drawn first

**The subcommand name and the engine-library name need not be the same, and probably should not be.**
This repository's premise is *"Collection of Crates (Lib/SDK/Bins) for building and running git
subcommands"* — so there is a user-facing verb (`git <something>`) and, separately, whatever the
reusable library is called.

House precedent is explicit about this. The estate's Rust workspace pairs a binary named for the
product with an engine library carrying its **own** brand name (`orrery`), plus an orchestration
layer as `<product>-sdk` and a delivery split of `-types` / `-server` / `-ui`. **There is no `-core`
anywhere in the estate** — the engine gets a real name rather than a suffix.

So the decision decomposes:

| Slot | What it names | Constraint |
|---|---|---|
| Subcommand | What a developer types | Must read naturally after `git `; discoverability matters |
| Engine library | The reusable analysis contract | Published under this repo's AGPL-3.0; name is an API-stability commitment |
| Orchestration / SDK | The layer above the engine | House convention is `<product>-sdk` |
| Delivery crates | Server, wire types, UI adapter | House convention is `-server` / `-types` / `-ui` |

## Assessment of the two candidates

### `git-graph`

**For:** immediately descriptive; "graph" is the central noun of the product; reads well as
`git graph`.

**Against, and this is a real problem:** *"git graph"* already means something else to every git
user — `git log --graph`, the **commit** DAG. This product's graph is a *code-structure* graph, a
different object entirely. The name invites users to expect commit-history visualisation and to be
confused when they get symbol references. There is also prior art on crates.io in the
commit-graph-visualisation space using this name, so registry availability needs checking before it
is committed to.

**Verify before choosing:** `cargo search git-graph`, and whether `git-graph` is taken on crates.io.

### `git-ctx`

**For:** no collision with commit-graph semantics; short to type; "context" is genuinely what the
tool provides to an agent — the 360-degree symbol view is literally called context in the capability
list.

**Against:** abbreviations are less discoverable, and `-ctx` follows a naming pattern
(`kubectx`-style) that usually signals *context switching* — selecting between environments or
identities. A user could reasonably expect `git ctx` to switch git identities or configs. Worth
checking whether anything already claims that meaning.

### A third direction worth considering

Neither candidate names the *engine*. If the engine library needs a real name under house precedent,
options include a distinct brand name for the library with a descriptive subcommand on top — e.g.
subcommand `git ctx`, engine crate named for what it is rather than for the CLI. That keeps the CLI
free to be renamed for UX reasons without breaking a published library API, which is the practical
argument for separating them.

## Recommendation

Not for the requirements author to settle. But two things should be recorded as constraints
regardless of the outcome:

1. **Check registry availability and semantic collision before publishing anything.** `git-graph` in
   particular needs clearing.
2. **Decide the subcommand name and the engine-library name as separate decisions.** Conflating them
   couples a UX choice to an API-stability commitment.

## Until it is decided

The requirements documents use `<PRODUCT>` as a marked placeholder. Do not silently adopt either
candidate mid-document — a half-renamed spec is worse than a placeholder.

## Notes

The AGPL-3.0 licence interacts with this: whatever the engine crate is called, publishing it means
publishing an AGPL library, and internal consumers must accept that to link it. See the
implementation-constraints section of the SPEC.
