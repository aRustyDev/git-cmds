# Question 0003 — Is the store trait async?

- **Status:** open · **Owner:** sync **B7** · **Date:** 2026-08-20
- **Blocks:** the first store implementation. Nothing before that.
- **Must be answered during backend screening, never after.**

## The question

Does the trait through which all persistence is reached expose asynchronous or synchronous operations?

## Why it cannot wait

House rule, from `muster/.claude/rules/04-rust-conventions.md`:

> *If any candidate backend is async-only, the trait is async and everything above it inherits that.
> Resolve during screening, not after — retrofitting async through a synchronous trait is a rewrite.*

The trait is the boundary that forces the answer, and the answer propagates upward through every
caller to the CLI's entry point. There is no incremental migration: a synchronous trait cannot be made
async without changing every signature above it.

## Why this instance is harder than the general rule

**The two deployment shapes pull in opposite directions**, and both are required (`CON-2`, `REV-2`).

| | Wants | Because |
|---|---|---|
| **Service shape** | async | Mainstream Rust clients for networked services are predominantly asynchronous, and `REV-2` requires a networked implementation of the graph, vector and relational slots in v1 |
| **Local shape** | synchronous | Embedded in-process engines are very likely synchronous; an async trait over one means either a blocking call inside an async function — which stalls an executor, a real defect under the concurrency `PERF-1` requires — or a thread-pool offload for what is a memory access |

**So whichever way this goes, one shape pays.** That is the consequence the ADR must record.

## Options

### A. Async trait
Networked clients are native. The local shape carries an async runtime it may not otherwise need, and
embedded synchronous engines need an explicit offload strategy — getting that wrong is invisible until
it is under load, which is exactly when `PERF-1` is being measured.

### B. Synchronous trait
Embedded engines are native, and `SCALE-4`'s 64 concurrent in-flight reads per replica are served by
threads rather than tasks — a capacity and memory question rather than a correctness one. Networked
clients need a blocking bridge, which either brings a runtime anyway (with a nested-runtime hazard when
the caller is async) or restricts the candidate set to genuinely-synchronous clients.

### C. Both, behind a feature flag
Looks cheapest. **Is not:** it doubles the conformance surface (`COR-6`, six slots), and two code paths
above one seam is `IF-1`'s divergence failure one layer down. Treat with suspicion.

## What settles it

**Not an opinion — a screening record.** `analysis/0004-store-capability-matrix.md` defines the
procedure and currently holds **no results**, because no candidate has been examined. Per candidate:

- client concurrency model — synchronous only · asynchronous only · both;
- if both, whether the synchronous path is a genuine implementation or a blocking facade over a runtime;
- runtime coupling — none, a specific runtime, or runtime-agnostic;
- whether the client performs blocking I/O that would stall an executor.

**"Both" is not automatically the easy answer.** A synchronous facade that blocks on an async runtime
brings the runtime as a dependency and creates a nested-runtime hazard. The screening must distinguish
that from a genuinely synchronous client.

## Recommendation

**None.** This is a structural decision and the requirements author's role is to state what the answer
must satisfy, not to take it. What it must satisfy:

1. It is recorded as an accepted decision record **before** the first store-implementation commit
   (`CON-3`), checkable from history.
2. The record names which deployment shape pays, and how much (house convention: record the consequence
   you dislike).
3. If option A, the offload strategy for embedded synchronous engines is specified, because a blocking
   call in an async context is the failure mode that only appears under the load `PERF-1` measures.
4. If option B, the candidate set is explicitly narrowed to clients that satisfy it, and that narrowing
   is recorded as a cost of the choice rather than discovered later.

## Related

- `analysis/0004-store-capability-matrix.md` — the screening record and procedure.
- `specs/04-interfaces-and-external-systems.md` — `EXT-9` (screening required), `EXT-1`–`EXT-6` (the slots).
- `specs/00-overview.md` — `CON-3`, the procedural requirement.
- `specs/03-non-functional-requirements.md` — `PERF-1`, `SCALE-4`, the requirements the choice bears on.
