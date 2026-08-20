# Question 0009 — Is a terminal interface wanted, or explicitly declined?

- **Status:** open · **Owner:** sync **B5** · **Date:** 2026-08-20
- **Owns:** `GAP-001`
- **Blocks:** nothing. But it changes `B5`'s answer, because four surfaces over a shared contract is a
  different design from three.

## The question

A **TUI** was named in the interface set after the capability list was written. It has **no
requirements at all**. Specify it, or decline it explicitly?

## Why it must be answered either way

An interface with no requirements gets built to whatever the implementer assumed, or silently dropped
and later described as never having been wanted. `IF-14` currently records it as an explicit absence for
exactly this reason — so that the corpus is *wrong* rather than *incomplete* if the answer is yes.

## What a terminal surface would inherit for free

More than it might appear, which is the argument for it being cheap:

- `IF-1` — one internal contract, so a TUI is a projection rather than an implementation.
- `FR-020`–`FR-039` — the whole read surface is already specified, surface-agnostic.
- `FR-039` — freshness on every answer, which a TUI can show persistently in a way a CLI invocation
  cannot.
- The local shape needs no authentication (`SEC-14`), so a local-first TUI has no identity work.

## What it would need that nothing else specifies

And this is the real cost:

1. **Interaction, not invocation.** Every other surface is request/response. A TUI is a session with
   state: a current selection, a navigation history, an expanded neighbourhood. **None of the
   requirements describe stateful interaction**, and `FR-041`'s prohibition on ambient server-side
   repository state was written for the service shape.
2. **Incremental and cancellable rendering.** `PERF-5` allows a traversal 2 s. A TUI that blocks for 2 s
   on a keystroke is unusable, so it needs to render partial results and cancel in-flight work — which
   is a **streaming** requirement the corpus does not have anywhere.
3. **A layout contract.** `IF-11` gives the web UI force-directed, sequential and radial layouts. A
   terminal has none of those. What a graph looks like in a terminal is a genuine design question, not a
   reduction of the web UI.
4. **Its own budget.** Keystroke latency is a different class from `PERF-2`'s 250 ms; interactive
   terminal work is usually budgeted in tens of milliseconds.

**Point 2 is the one that reaches back into the requirements.** Streaming and cancellation of a
read are not specified for any surface, and adding them for a TUI would either be TUI-only — which
`IF-1` makes awkward — or a change to the internal contract that every surface then inherits.

## Options

### A. Decline, with a revisit trigger
`IF-14` stands as written. `git-ctx` remains an invocation-based CLI.

**For:** zero cost; the CLI already serves the terminal user; `analysis/0005` shows the local shape is
already the simpler one and this keeps it so.
**Against:** the CLI is poor for exploration — every widening of a neighbourhood is a fresh invocation
that re-resolves everything. Exploration is `US-D-10`'s whole shape, and it is the flow the CLI serves
worst.

### B. Specify it as a local-shape projection, read-only
A terminal surface over the existing read contract, local shape only, no mutation.

**For:** inherits the read surface; no identity work; genuinely useful for `US-D-2`, `US-D-9` and
`US-D-10`.
**Against:** requires points 1–4 above, and point 2 changes the internal contract.

### C. Specify it fully, both shapes, including mutation
**For:** consistency.
**Against:** a TUI against a remote authenticated service is a client with credential handling, and
`SEC-1`'s per-principal identity in a terminal client is a device-flow problem nobody has scoped. Hard
to justify before B is proven useful.

### D. Defer to after v1, with the streaming question answered now
Decline the surface, but decide whether the internal contract supports streaming and cancellation
**anyway** — because `IF-6`'s output budgeting for agents and `PERF-5`'s truncation are adjacent to it,
and retrofitting streaming through a request/response contract has the same character as retrofitting
async.

## Recommendation

**A or D, and the choice between them turns on one thing: whether the internal contract should support
streaming and cancellation regardless.**

There is a case that it should, independent of any TUI:

- `IF-6` already requires bounded output with truncation as a field — a partial answer by another name.
- `PERF-5` already requires a traversal to return `undetermined` on budget exhaustion, which means the
  traversal is already cancellable internally.
- `US-G-3` and `US-G-4` describe an agent branching on partial and inconclusive results.

**So the streaming-shaped requirement may already be latent in the corpus**, and if it is, D costs
little and A forecloses something. That is worth 20 minutes at `B5` rather than a decision here.

**What must not happen:** the TUI gets built as a fourth hand-rolled adapter. That is `IF-1`'s measured
failure mode — the grounding found two entry points to nominally the same functionality with different
authentication, different concurrency behaviour and different operation inventories. A fourth surface
is a fourth opportunity for it.

## Related

- `specs/04-interfaces-and-external-systems.md` — `IF-14` (the recorded absence), `IF-1`, `IF-6`.
- `GAPS.md` — `GAP-001`.
- `SYNCS.md` — **B5**, which owns the surface set.
