# code-intelligence

Requirements for a **Rust code-intelligence platform** — a system that parses repositories into a
queryable knowledge graph and serves it to humans over a web UI and to AI agents over MCP, in two
deployment shapes: a local CLI and a Kubernetes-native microservice.

**This plan owns requirements documentation only.** It produces the SPEC, PRD, feature list and
analysis documents that a Software Architect consumes. It deliberately writes **no Rust, no
`Cargo.toml`, and no crate names** — module decomposition is the architect's deliverable, and
pre-empting it is the main way this work fails.

**Status (2026-08-19): trigger prompt written, not yet executed.** Only `PROMPT.md` and this file
exist.

## Why this plan exists

A mature reference implementation of this capability already exists — **GitNexus** (TypeScript) —
and hosting it was the original plan. That plan is blocked. GitNexus is **PolyForm Noncommercial
1.0.0**, and its licensor confirmed in writing that internal use at a for-profit company requires a
paid commercial licence. The full determination, with quoted clauses and primary sources, is in
`~/repos/woven/forks/gitnexus/.claude/plans/hosted-service/FINDINGS.md` §0 (on `main`).

`gitnexus/.claude/plans/hosted-service/adrs/0001-gitnexus-licensing-path.md` framed four options —
buy, adopt permissive alternatives, stop, or managed SaaS. **A clean-room Rust implementation is
effectively a fifth**, and the only one that keeps every capability without a recurring licence or a
fragmented three-tool composition.

## The clean-room constraint is load-bearing

PolyForm's **No Other Rights** clause forbids sublicensing. A derivative of GitNexus therefore
**could not be released under this repository's AGPL-3.0 licence at all.** The clean room is not
hygiene — it is what makes the licence choice coherent.

The protocol is a **dirty-team / clean-team split**, specified in full in `PROMPT.md`:

- The requirements author **may** read the prior grounding research, and **may not** read GitNexus
  source.
- The architect and implementers read **only** what the author writes.
- Every requirement must pass the laundering test: *would this be implementable by an engineer who
  has never heard of GitNexus?*

## Known constraints

1. **This repository is AGPL-3.0.** Unlike PolyForm Noncommercial it places no bar on internal
   commercial use, so it solves the original problem — but two consequences shape the library / SDK /
   binary split: internal consumers must accept AGPL to *link* the libraries, and §13's network
   clause binds if the service is ever exposed beyond the organisation.
2. **Two deployment shapes, one design.** Local CLI (single binary, embedded stores, one user) and
   K8s microservice (external stores, authenticated, ~20–50 humans plus up to ~10 000 mostly
   read-only agents). Not two configurations — two points a single design must reach.
3. **The house Rust conventions already answer several architectural questions.**
   `~/repos/woven/forks/muster/.claude/rules/{00-non-negotiables,04-rust-conventions}.md` establish
   persistence behind a repository trait with no concrete datastore type in the public API,
   per-backend feature flags with an in-memory default, `thiserror` in libraries and `anyhow` in
   binaries, and that the async decision must be resolved during screening because retrofitting it
   is a rewrite.
4. **The product name is undecided.** House precedent (`orrery`, `muster-sdk`, `muster`) is that the
   engine library carries a real product name — there is no `-core` anywhere in the estate.

## Map

| Path | What it is | Exists |
|---|---|---|
| `PROMPT.md` | Trigger prompt — write the requirements documentation. | ✅ |
| `README.md` | This file: what the plan is, and the map. | ✅ |
| `PRD.md` or `prds/` | Problem, why now, functional requirements, out of scope, user flows, dependencies, success criteria. | ⬜ |
| `specs/NN-*.md` | The SPEC, split across numbered files. | ⬜ |
| `FEATURES.md` | Flat, ID'd feature list traceable to SPEC requirement IDs. | ⬜ |
| `analysis/` | Capabilities · feature clusters · feature gaps. | ⬜ |
| `questions/NNNN-*.md` + `QUESTIONS.md` | One file per architectural fork, plus an index. | ⬜ |

Directories are created on their first real document — a stub tree reads as coverage and is a lie.
Numbering is global per kind, so gaps are expected; note them here rather than renumbering.

## Related

- `~/repos/woven/forks/gitnexus/.claude/plans/hosted-service/` — the grounding research this plan
  inherits: `FINDINGS.md` (licensing verdict, then the evidence), `RESEARCH.md` (~1,830 lines of
  archaeology across five lanes), `QUESTIONS.md`, and `adrs/0001-gitnexus-licensing-path.md`.
- `~/repos/woven/forks/muster/` — the estate's target pattern for Rust workspaces and for
  plan-scoped specs and PRDs. Its `.claude/plans/orrery/{specs,prds,questions,research}/` is the
  format to mirror.
- `~/repos/woven/infrastructure/infrastructure/docs/src/dev/specs/` — graduated specs, and the
  source of the requirement-ID and `## Verification` conventions.
- `~/.claude/rules/plans-and-docs.md` — governs this layout, and the aspirational-vs-graduated
  distinction for specs and PRDs.
