# SPEC 09 — References and appendices

- **Date:** 2026-08-20
- **Vocabulary:** the glossary is a standalone document, [`GLOSSARY.md`](../GLOSSARY.md), because it is
  a ratified constraint on every other file rather than an appendix to one.

## Appendix A — Mapping to the external SRS structure

The requester supplied an external reference on software-requirements-specification structure, and the
section list in the trigger prompt is drawn from it. This table maps that structure onto this SPEC, so
a reader coming from the reference can find each section, and so anything it recommends that this
corpus omits is visible rather than silently absent.

| Section in the external reference | Where it lives here |
|---|---|
| Introduction and Purpose | [`00-overview.md`](00-overview.md) |
| Business Requirement | [`00-overview.md`](00-overview.md) — `BR-1`–`BR-5` |
| User Personas or Roles | [`01-personas-and-flows.md`](01-personas-and-flows.md) — `P1`–`P5` |
| Feature List | [`../FEATURES.md`](../FEATURES.md) |
| User Story or Use Cases | [`07-use-cases.md`](07-use-cases.md) — `US-*`, `UC-*` |
| User Requirements | [`01-personas-and-flows.md`](01-personas-and-flows.md) (the five flows) and [`07-use-cases.md`](07-use-cases.md) |
| Functional Requirements | [`02-functional-requirements.md`](02-functional-requirements.md) — `FR-*` |
| Nonfunctional Requirements | [`03-non-functional-requirements.md`](03-non-functional-requirements.md) — `COR-*`, `OPS-*`, `REV-*` |
| Interface Requirements | [`04-interfaces-and-external-systems.md`](04-interfaces-and-external-systems.md) — `IF-*` |
| Performance Requirements | [`03-non-functional-requirements.md`](03-non-functional-requirements.md) — `PERF-*`, `SCALE-*` |
| Security Requirements | [`05-security-requirements.md`](05-security-requirements.md) — `SEC-*` |
| Design and Implementation Constraints | [`06-constraints.md`](06-constraints.md) — `CON-*` |
| External System Requirements | [`04-interfaces-and-external-systems.md`](04-interfaces-and-external-systems.md) — `EXT-*` |
| Quality Assurance Requirements | [`08-testing-and-documentation.md`](08-testing-and-documentation.md) — `QA-*` |
| Documentation Requirements | [`08-testing-and-documentation.md`](08-testing-and-documentation.md) — `QA-16`–`QA-21` |

**Where this corpus departs from the reference, deliberately:**

1. **House style wins on form.** Sentence-case headings, en-dashes, no emoji, `### <PREFIX>-<n> —
   <Component> MUST <do X>. *(status)*`, and a closing `## Verification` split into proven and
   not-proven per file. The reference is agnostic about form; the estate is not.
2. **A glossary is written second, not last** — it is a ratified gate (sync **A2**), not an appendix.
3. **Every file states what it has NOT established.** The reference's quality criteria do not require
   this; the estate's requirement-ID convention does, and it is the single most useful thing a
   downstream reader gets.
4. **Analysis documents sit outside the SPEC** (`analysis/`), because their consumer is the architect
   deciding module shapes rather than an implementer reading requirements.

### The reference's quality criteria, assessed against this corpus

Its stated criteria for a well-formed requirement are: unambiguous · complete · traceable · consistent
· measurable · relevant · current · feasible · acceptable · prioritised. An honest assessment:

| Criterion | Assessment |
|---|---|
| **Unambiguous** | Largely met, and the glossary is why — three renames were made specifically to remove ambiguity ("process", "impact analysis", "supports language X"). `FR-004` remains genuinely ambiguous pending `CON-10`, and that is recorded. |
| **Complete** | **Not claimed.** Complete with respect to Appendix A of the trigger prompt, Appendix B's coverage gaps and this session's decisions. Syncs **A1** and **A4** exist because completeness is not established. |
| **Traceable** | Met, and mechanically: `CAP-0nn` ↔ `FR-0nn`, and [`FEATURES.md`](../FEATURES.md) traces both ways. Verified by an executable ID-set diff. |
| **Consistent** | Believed met; not proven. No contradiction has been found, and no systematic contradiction check has been run beyond the ID audit. |
| **Measurable** | Every requirement carries a verification method. **But almost nothing is currently measurable** — there is no telemetry and nothing built (`GAP-004`). `FR-036` is explicitly unverifiable today. |
| **Relevant** | Met — every requirement traces to a capability the requester asked for, an inherited negative, or a stated coverage gap. |
| **Current** | Met as of 2026-08-20, with the four scope decisions of that date recorded. |
| **Feasible** | **Not established.** `analysis/0003-feature-gaps.md` flags every capability with no precedent anywhere as elevated risk, precisely because feasibility is unproven for those. |
| **Acceptable** | **Not established.** Nobody has reviewed this corpus. Sync **A1** is the acceptance step. |
| **Prioritised** | Met at the coarse grain — MUST / SHOULD / WON'T on every requirement, plus v1 versus deferred. Not prioritised *within* MUST, which is a real omission and is the architect's sequencing input rather than a requirements one. |

## Appendix B — External documents

### Supplied by the requester

- **Software requirements specifications**, IEEE Computer Society.
  <https://www.computer.org/resources/software-requirements-specifications>
  Read for the shape of a requirements specification and for what counts as a well-formed
  requirement. Its section list is the source of the trigger prompt's own section list; the mapping
  and the deliberate departures are above.

### Estate documents this corpus depends on

**Paths below are given relative to their own repository, not to this one.** Locations within the
organisation's estate are deliberately omitted — this repository is public, and its internal layout is
not. A reader inside the organisation knows where these repositories live; a reader outside does not need
to. Note that a repository's own rules do **not** auto-load outside it, so these must be opened
explicitly rather than relied on to be present.

| Document | Why it is load-bearing here |
|---|---|
| `muster/.claude/rules/00-non-negotiables.md` | Persistence behind a repository trait; no concrete datastore type in the public API; constraints enforced rather than documented (`CON-7`, `REV-1`, `QA-0`) |
| `muster/.claude/rules/04-rust-conventions.md` | Typed errors in libraries; newtyped identifiers; per-backend feature flags with an in-memory default; **the async rule** (`CON-3`, `CON-7`, `EXT-9`) |
| `muster/.claude/rules/02-decision-records.md` | MADR; global numbering; immutable once accepted; **record the consequence you dislike** (`QA-21`) |
| `muster/.claude/rules/10-docs-structure.md` | Where a durable fact lives; directories created on first real document |
| `~/.claude/rules/plans-and-docs.md` | Aspirational (`.claude/plans/**`) versus graduated (`docs/src/**`) specs — why this corpus is aspirational and what graduation would mean |
| `~/.claude/rules/tool-call-plumbing.md` | The measured plumbing constraints that shaped several verification methods, notably positive controls on absence claims (`QA-15`) |

### Format exemplars followed

| Exemplar | Followed for |
|---|---|
| `muster/.claude/plans/orrery/specs/00-overview.md` … `05-testing-criteria.md` | The multi-file SPEC split and the non-functional vocabulary |
| `muster/.claude/plans/orrery/prds/00-orrery-engine.md` | The PRD outline |
| `infrastructure/docs/src/dev/specs/cluster-egress-requirements.md` | The requirement-ID form and the `## Verification` proven/not-proven split |
| `infrastructure/.claude/plans/airgap-bootstrap/{PRD.md,SPEC.md}` | Out-of-scope **by name**, and `## How we will know we were wrong` |
| `muster/.claude/plans/quality-review/01-gap-matrix.md` | The gap-matrix vocabulary `✓ covered · ◐ partial · ✗ gap · — N/A` |

### Prior grounding — readable by the requirements author only

`gitnexus/.claude/plans/hosted-service/` — `FINDINGS.md`, `RESEARCH.md`,
`QUESTIONS.md` and `adrs/0001-gitnexus-licensing-path.md`.

**Implementers MUST NOT read these** (`CON-1`): they quote internal identifiers, so reading them
would taint a clean-team member. They are cited here for provenance, not as further reading. Everything
this corpus takes from them is already laundered into a requirement.

### Third-party licence facts referenced

Licence classes named in `EXT-8` and in `analysis/0003` come from the licence survey in the grounding.
The specific licences of the reference implementation and of candidate substitutes are matters of
public record; where this corpus relies on one, the requirement states the *class* of constraint
(permissive · weak copyleft · strong copyleft · network copyleft · source-available with a use grant ·
purpose-enumerated), because a class is what the design must accommodate and a specific product's
licence can change.

## Appendix C — Visuals

No diagram appears in this corpus, and that is a decision rather than an omission.

**Why:** the visuals a reader would expect here are a module diagram, a crate-dependency graph and a
component topology. All three are **the architect's deliverable** (`CON-8`), and drawing any of them —
even "illustratively" — would pre-empt the decision this corpus exists to inform. A diagram is
particularly hard to un-decide: it is remembered as the design long after the caveat is forgotten.

**What stands in for them, deliberately non-structural:**

| Instead of | This corpus provides |
|---|---|
| A module diagram | The capability inventory with consumer, mode, store and shape metadata (`analysis/0001`), and **multiple candidate clusterings** with what would decide between them (`analysis/0002`) |
| A data-flow diagram | Flow **D** in [`01-personas-and-flows.md`](01-personas-and-flows.md), written as stages and ordering requirements rather than boxes |
| A deployment topology | The deployment-shape contrast tables in [`00-overview.md`](00-overview.md) and `analysis/0005` |
| A component-interaction diagram | The surface table and `IF-1`'s single-contract requirement in [`04`](04-interfaces-and-external-systems.md) |
| A trust-boundary diagram | `analysis/0006-threat-model.md`, as a table of boundaries per shape |

**When diagrams should be added, and by whom:** after sync **B1** and **B6**, by the architect, in
`docs/src/dev/` where conclusions live rather than in a plan directory where work-in-progress lives.

## Appendix D — Requirement counts

Derived by counting the corpus, and asserted by the audit rather than by this table.

| File | Prefix | Count |
|---|---|---|
| `00-overview.md` | `BR-`, `CON-` | 5 business, 2 constraints |
| `02-functional-requirements.md` | `FR-` | 51 |
| `03-non-functional-requirements.md` | `PERF-`, `SCALE-`, `COR-`, `OPS-`, `REV-`, `QA-0` | 7 + 5 + 7 + 7 + 5 + 1 |
| `04-interfaces-and-external-systems.md` | `IF-`, `EXT-` | 14 + 13 |
| `05-security-requirements.md` | `SEC-` | 17 |
| `06-constraints.md` | `CON-` | 8 declared here, 12 in the registry |
| `07-use-cases.md` | `US-`, `UC-` | 34 stories, 6 use cases |
| `08-testing-and-documentation.md` | `QA-` | 21 |
| **Total requirements** | — | **163** |

Plus 34 user stories and 6 use cases, which are traceability artefacts rather than requirements and
are counted separately.

**Numbering gaps are expected and are not errors.** `FR-051`–`FR-067`, `FR-069`, `FR-070`, `FR-072`
and `FR-074` are unused: the `CAP-0nn` ↔ `FR-0nn` alignment means cross-cutting capabilities
`CAP-060`–`CAP-074` mostly map to `SEC-`, `EXT-`, `OPS-`, `PERF-` and `SCALE-` identifiers instead, and
only `CAP-068`, `CAP-071` and `CAP-073` kept an `FR-` number. The gaps are the price of a mechanical
mapping, and they are cheaper than renumbering.

## Verification

### What is proven

- **The external reference's every recommended section has a home**, and the four deliberate departures
  are named.
- **The reference's own quality criteria are assessed honestly**, including the four that are **not
  met** — complete, measurable-in-practice, feasible, acceptable. A corpus claiming all ten would be
  the less trustworthy document.
- **The absence of diagrams is a recorded decision** with a named substitute for each diagram a reader
  would expect.
- **The numbering gaps are explained** rather than left to look like omissions.

### What is NOT proven

- **The requirement counts in Appendix D are hand-tallied** and are asserted by the audit. If the audit
  and this table disagree, the audit is right and this table is stale.
- **The estate-document list is what this author read**, not a complete list of what bears on the work.
  In particular, no `docs/src/dev/policies/` page was consulted, and there may be standing policies
  this corpus contradicts without knowing.
- **No legal source is cited for the AGPL reading** in `CON-4`/`CON-5` — only the licence text itself.
  `questions/0005` should be settled with counsel.

## Amendments

- **2026-08-20** — Created.

## Related

- [`../GLOSSARY.md`](../GLOSSARY.md) — the ratified vocabulary, which is not an appendix.
- [`../README.md`](../README.md) — the plan map.
- [`../FEATURES.md`](../FEATURES.md) — the feature list the external reference calls for.
