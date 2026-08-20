# Analysis 0005 — Deployment-shape applicability, per requirement

- **Date:** 2026-08-20 · **Status:** input to syncs **B1**, **B2** and **B6**
- **Purpose:** the deployment duality is described in `PROMPT.md` as a first-class force and as *two
  points a single design must reach*. That claim is only checkable if applicability is stated **per
  requirement**. This document states it.
- **Vocabulary:** [`GLOSSARY.md`](../GLOSSARY.md)

## Notation

| Mark | Means |
|---|---|
| **L+S** | Applies to both shapes, identically. |
| **L+S\*** | Applies to both, but the *budget or threshold* differs. The requirement is one; the number is two. |
| **S** | Service shape only. |
| **L** | Local shape only. |
| **S / n-a-L** | Service shape only, and **not applicable** locally — the concept does not exist there. Distinguished from **S** (where the requirement simply is not imposed locally) because the two have different consequences for the design. |

**The distinction between `S` and `S / n-a-L` is the point of this document.** A requirement that is
merely unimposed locally can be implemented once and switched off. A requirement whose *concept does
not exist* locally cannot — and if the design assumes it exists, the local shape inherits machinery it
has no use for. That is `CON-6`'s failure mode and invariant 9 of `analysis/0002`.

## Business requirements

| ID | Shape | Note |
|---|---|---|
| `BR-1`, `BR-2`, `BR-3` | L+S | Licence and clean room bind the artefacts, not a deployment. |
| `BR-4` | L+S | This requirement *is* the duality. |
| `BR-5` | L+S | Tool consolidation applies to both. |

## Functional requirements

### Ingestion and index construction

| ID | Shape | Note |
|---|---|---|
| `FR-001`–`FR-010` | L+S | Ingestion behaviour is identical. `CON-2` requires it. |
| `FR-011`, `FR-012`, `FR-013` | L+S | Incrementality matters locally too — arguably more, since a developer waits for it. |
| `FR-014` | L+S | |
| `FR-015` | **L+S\*** | *"The current repository"* is resolvable from the working directory locally and **does not exist** in the service shape. Same requirement, two resolution strategies. |
| `FR-016`, `FR-017` | L+S | |
| `FR-018` | L+S | Derived identities matter locally the moment anything is cached. |
| `FR-019` | L+S | An escalation a developer cannot see is the same defect as one an operator cannot see. |

### Query and analysis

| ID | Shape | Note |
|---|---|---|
| `FR-020`–`FR-027` | L+S | The analysis surface is the part that must be identical. |
| `FR-028` | **S** | Diff impact from a supplied patch with no checkout. Permitted locally, not required — a local user has a working tree. |
| `FR-029`–`FR-036` | L+S | |
| `FR-037`, `FR-038` | L+S | `WON'T` in both. |
| `FR-039` | L+S | Freshness is not a service-only concern; a local index goes stale between commands. |

### Repositories, groups and acquisition

| ID | Shape | Note |
|---|---|---|
| `FR-040` | L+S | |
| `FR-041` | **L+S\*** | Locally, switching is session state. In the service shape, ambient per-connection repository state is **forbidden** — so the requirement is satisfied by opposite means. |
| `FR-042` | L+S | Cross-repository analysis is wanted locally too. |
| `FR-043`, `FR-044` | L+S | |
| `FR-045`, `FR-046` | **S** | Acquisition from a remote. A local user already has the repository; `git-ctx` reads a path. **This is the cleanest single-shape boundary in the corpus.** |
| `FR-047` | L+S | |

### Write operations and platform

| ID | Shape | Note |
|---|---|---|
| `FR-050` | L+S | Rename mutates a working tree, which the service shape only has for acquired repositories. |
| `FR-068` | **L+S\*** | Durable queued cancellable jobs. **Locally, a foreground run is permitted** — but durability and cancellation still apply, because a developer interrupting an index run must not corrupt it. Queue depth of one is acceptable locally; rejecting a second repository is not. |
| `FR-071` | L+S | |
| `FR-073` | L+S | A developer upgrades too, and a forced reindex is worse locally where there is no operator to schedule it. |

## Performance and scale

| ID | Shape | Note |
|---|---|---|
| `PERF-1` | **S** | Reads scaling with readers. Unobservable locally with one user — **but must not be designed away**, because it cannot be added back later. This is the most dangerous `S` in the document. |
| `PERF-2` | S | 250 ms n95, networked stores. |
| `PERF-3` | L | 100 ms n95, embedded stores. The tighter budget, because the transport is gone. |
| `PERF-4` | S | Web-UI contract budget. |
| `PERF-5` | **L+S\*** | Traversal budget. Same 2 s ceiling stated for both; local may well beat it, and the requirement is the ceiling. |
| `PERF-6` | L+S | Incrementality is proportional work in both. |
| `PERF-7` | **L+S\*** | Full-build baseline. Separate baselines per shape, since the store performance differs. |
| `SCALE-1` | L+S | Same repository scale target. A developer's monorepo is the same monorepo. |
| `SCALE-2` | **S / n-a-L** | Principal populations. **No concept locally** — there is one user and no principals. |
| `SCALE-3` | L+S | Repositories bounded by capacity. A developer with 40 repositories hits this. |
| `SCALE-4` | **S / n-a-L** | 64 concurrent in-flight reads per replica. No replicas locally. |
| `SCALE-5` | L+S | Concurrent submissions for distinct repositories. |

## Correctness, operability, reversibility

| ID | Shape | Note |
|---|---|---|
| `COR-1`–`COR-3` | L+S | Correctness cannot differ by shape. |
| `COR-4` | L+S | Torn reads are possible locally too — a query during a rebuild. |
| `COR-5` | L+S | Ranking identical across surfaces, in both shapes. |
| `COR-6` | L+S | Conformance per backend. |
| `COR-7` | L+S | Source is untrusted in both. |
| `OPS-1` | **L+S\*** | **Required in the service shape; optional and off by default locally.** Locally there is no operator to consume it, and a developer's tool should not emit telemetry by default. |
| `OPS-2` | S | Per-replica concurrency observability. |
| `OPS-3` | L+S | Skip reporting is how a developer learns why a run was slow. |
| `OPS-4` | **S** | Staleness as a metric, without a request. Locally, `FR-015` on demand suffices. |
| `OPS-5` | **L+S\*** | Correlation identifiers. Locally this is a run identifier, not a request identifier. |
| `OPS-6` | **S / n-a-L** | Metric cardinality. No metrics backend locally. |
| `OPS-7` | L+S | Explicit degradation. Locally the store failure is a file error and must still be explicit. |
| `REV-1`, `REV-2`, `REV-4` | L+S | |
| `REV-3` | L+S | Export matters more locally, where there is no operator to run a backup. |
| `REV-5` | L+S | This requirement *is* the duality. |

## Interfaces

| ID | Shape | Note |
|---|---|---|
| `IF-1` | L+S | One internal contract, both shapes. |
| `IF-2` | L+S | |
| `IF-3` | **S / n-a-L** | Authentication terminates in one place. **No authentication exists locally**, so there is nowhere for it to terminate. |
| `IF-4`, `IF-5`, `IF-6` | L+S | The agent surface exists in both shapes — a local agent protocol is a primary use. |
| `IF-7` | **L+S\*** | Explicit repository per operation. Locally, defaulting from the working directory is permitted **when exactly one repository is visible**. |
| `IF-8` | **S** | Session identity. |
| `IF-9` | **S / n-a-L** | Per-request repository visibility and read-only mode. **No concept locally** — one user sees everything they have. |
| `IF-10` | L+S | CLI self-sufficiency, and no CLI-only capability. |
| `IF-11` | **S** | Web-UI contract. Currently service-shape only, and `questions/0009`/`SEC-14` note this may change. |
| `IF-12` | **L+S\*** | Provider configuration. Locally it is a config file; there is no runtime UI path. |
| `IF-13` | **S** | Restricting the runtime path. Nothing to restrict locally. |
| `IF-14` | L | The unspecified terminal surface would be local-first. |

## External systems

| ID | Shape | Note |
|---|---|---|
| `EXT-1`–`EXT-3` | **L+S\*** | Both shapes need the slot; the *implementation* differs by shape and that is the whole point of the seam. |
| `EXT-4`, `EXT-6` | S | Optional networked slots; no consumer in either shape today. |
| `EXT-5` | **L+S\*** | Required if the graph engine cannot rank lexically, and the graph engine differs by shape — **so this slot's necessity may itself differ by shape.** The one place where the duality reaches into the store set. |
| `EXT-7` | L+S | Embedding provider. Locally it may be an in-process runtime; the requirement that misconfiguration fails loudly is identical. |
| `EXT-8` | L+S | Licence gating binds the artefacts. |
| `EXT-9` | L+S | Async screening covers both shapes' candidates — see `analysis/0004`, where the two shapes pull opposite ways. |
| `EXT-10`, `EXT-11` | **S / n-a-L** | Identity and authorisation providers. No concept locally. |
| `EXT-12` | **S** | Remote transports. |
| `EXT-13` | S | Telemetry export. |

## Security

| ID | Shape | Note |
|---|---|---|
| `SEC-1`–`SEC-9` | **S / n-a-L** | The entire identity, authorisation, audit and abuse surface. **No principals exist locally**, so these are not switched off — they are absent. |
| `SEC-10` | L+S | Path confinement. A symlink escape is a defect locally too. |
| `SEC-11` | **L+S\*** | Credentials not readable back. Locally the config file is the user's own, so the requirement reduces to "no surface echoes it". |
| `SEC-12` | L+S | Credentials never in an argument list or a log. Applies wherever a credential exists — including a local acquisition, if that is ever supported. |
| `SEC-13` | **L+S\*** | Code egress enumerable. **This is the requirement that matters most locally**, because a local tool with a provider credential sends the user's code to a third party from their own machine, with no operator and no audit trail. |
| `SEC-14` | **L** | The local shape's no-listener requirement. Applies only to the shape it constrains. |
| `SEC-15` | S | Transport and browser-facing controls. |
| `SEC-16` | L+S | No code in telemetry or logs. |
| `SEC-17` | **S / n-a-L** | Query privacy between principals. One user locally. |

## Constraints and quality

| ID | Shape | Note |
|---|---|---|
| `CON-1`, `CON-4`, `CON-5` | L+S | `CON-5` binds only if the service is exposed externally — a deployment decision, not a shape one. |
| `CON-2`, `CON-3`, `CON-6`–`CON-10` | L+S | |
| `QA-0`–`QA-7`, `QA-11`–`QA-21` | L+S | |
| `QA-8` | **L+S\*** | Budget gates per shape, with separate baselines. |
| `QA-9` | L+S | This gate *is* the duality's proof. |
| `QA-10` | L+S\* | Separate baselines. |

## What the tally says

| Mark | Count | Reading |
|---|---:|---|
| **L+S** | ~103 | The large majority. The duality is a smaller force than it feels, in requirement count. |
| **L+S\*** | ~19 | One requirement, two numbers or two resolution strategies. |
| **S** | ~19 | Imposed only on the service shape; implementable once and configured off. |
| **S / n-a-L** | ~20 | **The real seam.** |
| **L** | 2 | `PERF-3` and `SEC-14`. |

### The finding

**Twenty requirements have no local counterpart at all, and seventeen of them are the identity,
authorisation, audit and abuse surface plus their providers.** That is one coherent block, not a
scatter.

Two consequences fall out, both for the architect and neither decided here:

1. **The access-plane block is the cleanest candidate boundary the duality produces.** It is the only
   group where the local shape needs *nothing*, so it is the only group whose absence must be a
   composition property rather than a configuration flag. `analysis/0002` clustering B4 and C3 both
   isolate roughly this block, from different signals — which is weak corroboration, since two
   clusterings agreeing is not evidence, but it is worth noting they agree here and disagree elsewhere.
2. **`PERF-1` is the trap.** It is marked `S` because a single local user cannot observe read
   concurrency — and it is the one `S` requirement that **cannot be added later**, because it is a
   property of how state is shared rather than a feature. A design that satisfies the local shape
   naturally, with one shared handle behind one lock, is precisely the design the measured prior-art
   failure had. **The local shape's simplicity is an active hazard to `PERF-1`**, and that is the
   sentence in this document most worth carrying into `B2`.

### The counter-finding, stated because it cuts the other way

**`SEC-13` and `REV-3` matter *more* locally**, not less. A local tool holding a provider credential
sends source code off the machine with no operator, no audit trail and no egress policy; and a local
index has no operator to back it up. It would be easy to read this document as "the local shape is the
service shape minus security", and that reading is wrong in exactly these two places.

## Verification

### What is proven

- **Every requirement declared in `specs/**` has an applicability mark**, and the marks distinguish
  *unimposed* from *inapplicable*, which is the distinction that determines whether something can be a
  flag or must be a composition property.
- **The tally is derived from the table**, and it identifies one coherent 17-requirement block rather
  than a scatter.
- **Two findings run in opposite directions** — the access plane is absent locally, and two
  security-adjacent requirements are *stronger* locally.

### What is NOT proven

- **The marks are the requirements author's judgement.** Several are arguable: `FR-050` (rename) is
  marked `L+S` on the assumption the service shape mutates acquired working trees, which is not
  specified anywhere. `IF-11` is marked `S` on the assumption the local shape never serves the web UI,
  which `SEC-14` flags as likely to change.
- **The counts are approximate** — marked "~" — because a handful of requirements could defensibly take
  a different mark, and the tally's value is the shape of the distribution rather than the exact
  figures.
- **`PERF-1`'s hazard is an argument, not a measurement.** Nothing has been built, so the claim that
  the local shape's natural design endangers it is inference from the measured prior-art failure.
- **No shape has been built**, so every `L+S\*` row asserts that one requirement can be met by two
  strategies without becoming two requirements. That is `CON-2`'s bet and it is untested.

## Amendments

- **2026-08-20** — Created.

## Related

- `specs/00-overview.md` — the deployment-duality contrast table this document expands per requirement.
- `analysis/0002-feature-clusters.md` — clustering B4 and C3, which isolate roughly the block found here.
- `analysis/0004-store-capability-matrix.md` — where the duality pulls opposite ways on async.
- `specs/05-security-requirements.md` — `SEC-14`, the local shape's own constraint.
