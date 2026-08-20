# SPEC 06 — Design and implementation constraints

> **Aspirational.** Status markers record justification strength, not implementation status.
> Vocabulary as ratified in [`GLOSSARY.md`](../GLOSSARY.md).

- **Date:** 2026-08-20
- **This is the one file in the SPEC that names the reference implementation**, because licence
  provenance cannot be checked against an anonymous claim. It is named in constraint *rationale*,
  never inside a requirement.

## Constraint registry

| ID | Constraint | Declared in |
|---|---|---|
| `CON-1` | Clean room | this file |
| `CON-2` | Business logic identical across deployment shapes | [`00-overview.md`](00-overview.md) |
| `CON-3` | The async decision is recorded before the first store implementation | [`00-overview.md`](00-overview.md) |
| `CON-4` | AGPL-3.0 — linkability | this file |
| `CON-5` | AGPL-3.0 — §13, the network clause | this file |
| `CON-6` | Deployment shape is composition, not a fork | this file |
| `CON-7` | House Rust conventions bind | this file |
| `CON-8` | Module decomposition is the architect's, and this corpus MUST NOT pre-empt it | this file |
| `CON-9` | The engine library name is gated | this file |
| `CON-10` | Parsing technology may make runtime language extension a different commitment | this file |
| `CON-11` | Graph query dialects diverge outside read traversal | [`04-interfaces-and-external-systems.md`](04-interfaces-and-external-systems.md) `EXT-1` |
| `CON-12` | Dependency licences are gated, not reviewed once | [`04-interfaces-and-external-systems.md`](04-interfaces-and-external-systems.md) `EXT-8` |

`CON-2` and `CON-3` are full requirements declared in [`00-overview.md`](00-overview.md), where the
reader meets them; they are listed here so the registry is complete, and are not restated — a fact
appearing in two documents will drift.

**`CON-11` and `CON-12` are aliases, not requirements.** They name design constraints that are already
stated as `EXT-1` and `EXT-8` respectively, and they exist only so a reader looking for "the constraint
about query dialects" or "the constraint about licences" finds it from this registry. They carry no
independent requirement text, appear in no traceability count, and are covered through the `EXT-`
identifiers they alias.

## Implementation constraints

### CON-1 — No implementer MUST read the reference implementation's source. *(VERIFIED)*

**MUST.** A dirty-team / clean-team split applies for the life of this project.

- The requirements author **may** read the prior grounding research: the findings, research and
  questions documents and the licensing decision record under
  `gitnexus/.claude/plans/hosted-service/`.
- **Nobody** may read `gitnexus/src/**`, its tests, or its schema files.
- No implementer may read the grounding research either, because it quotes internal identifiers.
  Implementers work **only** from this corpus.
- No internal name — module, file, function, phase, table or tool — and no magic constant may be
  reproduced. Every numeric budget in this corpus is ours and carries its derivation
  ([`03-non-functional-requirements.md`](03-non-functional-requirements.md)).

**Why this is a legal constraint and not hygiene.** GitNexus is licensed **PolyForm Noncommercial
1.0.0**, whose *No Other Rights* clause forbids sublicensing. A derivative work therefore **could not
be released under this repository's AGPL-3.0 licence at all** — not "would be awkward to", but could
not. The clean room is what makes the licence choice coherent. Separately, the licensor confirmed in
writing that internal use at a for-profit company requires a paid commercial licence, which is why
this project exists rather than a deployment.

**Verification:** every requirement in this corpus passes the laundering test — *would this be
readable, unambiguous and implementable by an engineer who has never heard of the reference?* Enforced
by an executable denylist check over `specs/**`, `FEATURES.md` and `analysis/**` for reference-internal
identifiers and carried constants, and by an attestation from each implementer. The audit result is
recorded in this plan's handoff.

**A consequence that binds a person, not a document:** whoever reads the grounding is tainted and
**must not implement**. That is recorded in the handoff, and it applies to the author of this corpus.

**A consequence that binds the architect's deliverable, added 2026-08-20.** Tool names are on the MUST NOT
list, and the requester's module-seam sketch (Appendix B of `PROMPT.md`) is a **transcription of the
reference's public command surface** — five of its node descriptions match the public documentation
verbatim (`analysis/0002`). **So crate and module names MUST NOT be derived from the sketch's node names.**
The sketch is safe to reason from and unsafe to name from. This is the one laundering failure that would be
externally visible, because it would ship in a published artefact's crate names, and the audit in
`scripts/audit-corpus.py` will not catch it — that script audits this corpus, not the future workspace.
Filed as `GAP-020`.

### CON-4 — Internal consumers MUST accept AGPL-3.0 in order to link the libraries. *(VERIFIED)*

**MUST.** This repository is AGPL-3.0 (`LICENSE`, 661 lines). Anything that **links** `<ENGINE>` — in
Rust's sense, statically, which is the normal case — forms a combined work subject to AGPL-3.0.

**What that constrains, concretely:**

1. **A differently-licensed internal codebase cannot link `<ENGINE>`.** It must reach the capability
   across a process boundary instead — the CLI, the API, or the agent protocol.
2. **The library / SDK / binary split is therefore partly a licence decision, not only a cohesion
   decision.** Which capability lives in a linkable library versus behind a service boundary
   determines who can consume it at all. This is an input to sync **B6**, and it is the reason `B6`
   also unblocks the engine name.
3. **A permissively-licensed shim does not launder this.** A thin wrapper crate under a different
   licence that links an AGPL library produces a combined work all the same.

**Verification:** every published crate declares AGPL-3.0, and the licence file ships **inside each
published package** rather than only at the repository root. A package whose manifest declares a
licence it does not contain is a compliance defect — one measured in the reference implementation's
own published artefact, where the declared licence text existed only at the repository root, outside
the package's file list.

**The open half:** whether any internal consumer actually needs to link rather than call across a
boundary has not been established. Filed as `questions/0005`. If none does, `CON-4` costs nothing; if
one does, it changes the split.

### CON-5 — If the service is exposed beyond the organisation, §13 obliges offering source to its users. *(VERIFIED)*

**MUST.** AGPL-3.0 §13 requires that users interacting with the software **over a network** be offered
the corresponding source of the version they are interacting with.

**What that constrains:**

1. **It binds the service shape, not the local shape.** A local binary a developer runs for themselves
   interacts with no remote user.
2. **Internal-only exposure is the assumed posture, and it is what makes this cheap.** The PRD records
   "exposing the service beyond the organisation" as out of scope, and that scope statement is a
   **licence** decision as much as a product one.
3. **Any future decision to expose it externally acquires a source-offer obligation** covering the
   exact deployed version, including local modifications. That is a release-engineering obligation —
   the deployed artefact must be identifiable and its source retrievable — not a one-off legal note.

**Verification:** the deployed artefact carries a version identifier resolvable to a source revision.
This is required regardless of exposure, because it is also how `FR-073`'s upgrade path and
`PERF-7`'s baselines stay meaningful.

**The consequence we dislike:** the two AGPL consequences pull in opposite directions. `CON-4` pushes
capability *out* of linkable libraries and behind a service boundary, so more consumers can use it;
`CON-5` attaches an obligation to that service boundary the moment it faces anyone outside. Neither is
avoidable and the tension has to be resolved deliberately in `B6` rather than discovered.

### CON-6 — A deployment shape MUST be a composition decision, never a code fork. *(assumed)*

**MUST.** The local shape and the service shape are assembled from the same behaviour. There MUST be
no shape-conditional analysis code.

**What may differ by shape:** which stores are configured; whether a network listener exists; whether
authentication is present; whether indexing is queued or foreground; whether telemetry is enabled.
**What MUST NOT differ:** what an analysis concludes (`CON-2`).

**Verification:** both shapes pass one behavioural conformance suite (`QA-9`). Additionally, an
executable check asserts no analysis code branches on a deployment-shape flag.

### CON-7 — House Rust conventions bind. *(operational)*

**MUST.** These are settled house practice and are not open questions. Read
`muster/.claude/rules/{00-non-negotiables,04-rust-conventions}.md` by absolute
path — a repository's own rules do not load outside it.

1. **All persistence behind a repository trait, with no concrete datastore type in the public API**
   (`REV-1`).
2. **Per-backend feature flags with an in-memory default**, so the test suite needs no external engine
   (`01-personas-and-flows.md` §E1).
3. **Typed errors in libraries** — one error library, used uniformly, never mixed. Context-chaining
   error handling belongs at a binary's top level only.
4. **No `unwrap()` or `expect()` in library code**, outside tests and const-evaluable invariants.
5. **Newtype every identifier.** A bare integer or string crossing a function boundary is a
   transposed-argument bug waiting to happen — and this corpus has repository identities, node
   identities, derived identities, index generations, principals and correlation identifiers, which is
   six identifier kinds that would otherwise all be strings.
6. **Constraints are executable, not documentary.** A comment saying "do not do this" does not satisfy
   a constraint (`QA-0`).

**Verification:** each is a lint, a test or an API check in CI.

**Cited as precedent, not mandated:** point 2's specific mechanism. Whether feature flags are the right
shape for six store slots is sync **B2**'s decision; the *property* — tests need no external engine —
is a requirement either way.

### CON-8 — This corpus MUST NOT decide the module decomposition. *(satisfied by design)*

**MUST.** Module shapes, crate boundaries, the workspace layout and the dependency graph are the
architect's deliverable. This corpus names no crate, draws no module diagram, and proposes no layout.

**Why it is a constraint rather than a scope note:** pre-empting the architect is the identified
primary failure mode for this work. A requirements corpus that has already decided the structure
produces an architect who either rubber-stamps it or spends their time undoing it.

**What this corpus provides instead:** the capability inventory with consumer, mode, store and shape
metadata (`analysis/0001`); candidate clusterings **with alternatives** and what would decide between
them (`analysis/0002`); and the forces — deployment duality, read/write asymmetry, the AGPL split, the
async question — surfaced as questions rather than resolved.

**Verification:** an executable check over the corpus for crate-shaped names other than `git-ctx` and
`<ENGINE>`, for `Cargo.toml`, and for `-core`-suffixed names. Expected: zero hits.

### CON-9 — The engine library name MUST NOT be chosen before sync B6. *(operational)*

**MUST.** Write `<ENGINE>` and leave it visibly unresolved. `git-ctx` is decided and is written
literally.

**Why:** a library name is a claim about scope, and scope is exactly what the seam work decides.
Naming first yields either a name narrower than the crate becomes, or a vague abstraction — which is
how `-core` suffixes happen, and there are none anywhere in this estate, deliberately.

**MUST also:** do not half-rename a document. A document using `git-ctx` in some places and `<ENGINE>`
in others is correct. One that has silently adopted a guessed engine name in half its sections is a
defect.

**Verification:** the `CON-8` check covers it. `questions/0001` holds the decision and its gate.

## Design constraints

### CON-10 — If grammars are native code compiled at build time, runtime language extension is a different commitment. *(assumed)*

**MUST be decided, not assumed.** `FR-004` requires that a language be addable without a fork. Whether
that means **build-time** extension (recompile with a new grammar) or **runtime** extension (a
deployment adds a language to a running system) is a materially different requirement, and the
difference is usually forced by the parsing technology rather than chosen.

**Three consequences that must be settled together (sync C1):**

1. **Build-time extension** means "without a fork" is satisfied by a contract plus a rebuild. An
   administrator cannot add a language; a developer can.
2. **Runtime extension** means loadable analysis code, which is a substantially larger commitment
   including a sandboxing question — untrusted analysis code parsing untrusted source.
3. **A lighter path for declarative formats** (`FR-004`'s SHOULD) may not need a grammar at all. Where
   most of an extraction contract is meaningless — no inheritance, no method resolution, no call graph
   — a dedicated processor is both cheaper and a better fit, and this is the route by which
   infrastructure-and-configuration support (`FR-005`) most plausibly arrives.

**Verification:** the decision is recorded before `FR-004` is implemented, and `FR-004`'s verification
is written against the chosen meaning.

## Constraints deliberately NOT imposed

Stated so their absence is a decision rather than an oversight:

- **No parsing technology is mandated.** `FR-002` and `FR-003` specify behaviour; sync **C1** chooses.
- **No graph algorithm is mandated** for clustering (`FR-010`) or flow derivation (`FR-009`). Both are
  cost and identity decisions for `B3`.
- **No store product is mandated.** Candidates are `presumed` compatibility targets only
  ([`04`](04-interfaces-and-external-systems.md)).
- **No frontend technology is mandated** (`IF-11`).
- **No telemetry protocol is mandated** (`OPS-1`, sync **D1**).
- **No transport or wire format is mandated** for the API. `IF-1` constrains the contract's
  *singularity*, not its encoding.
- **No release or versioning scheme is mandated.** Track **D** owns it; the only requirement that
  reaches into it is `CON-5`'s artefact-to-source resolvability and `FR-073`'s upgrade path.

## Verification

### What is proven

- **AGPL-3.0 is stated with both consequences named** — `CON-4` linkability and `CON-5` §13 — and the
  tension between them is written down rather than left for someone to discover in `B6`.
- **The clean room is justified legally, not hygienically.** `CON-1` names the *No Other Rights* clause
  and states the conclusion it forces: a derivative could not be AGPL-licensed at all.
- **`CON-8` is executable.** The check for crate-shaped names, `Cargo.toml` and `-core` suffixes is a
  grep, and it is part of the corpus audit rather than a promise.
- **The registry is complete** — every `CON-` identifier referenced anywhere in this SPEC is listed,
  including the four declared in other files.
- **`CON-4`'s packaging clause is evidenced**, from a compliance defect measured in the reference
  implementation's own published artefact: a manifest declaring a licence whose text was not in the
  package.

### What is NOT proven

- **No lawyer has read `CON-4` or `CON-5`.** They are the requirements author's reading of AGPL-3.0
  and of the licensing determination in the grounding. The determination that PolyForm bars this use
  is well-evidenced — including the licensor's written confirmation — but the AGPL *consequences* for
  the module split are an engineering reading of a licence, and `questions/0005` should be settled
  with counsel rather than by inference.
- **`CON-4`'s practical cost is unknown**, because no internal consumer has been identified that needs
  to link rather than call across a boundary.
- **`CON-10` is unresolved and it gates `FR-004`'s meaning.** Until sync C1, "add a language without a
  fork" has two readings and the requirement is ambiguous between them. That ambiguity is recorded
  rather than resolved by guessing, but it is a real hole.
- **`CON-1`'s attestation mechanism does not exist.** There is no implementer yet to attest, and no
  process for recording it.
- **The denylist for the laundering check is the requirements author's**, built from what they saw in
  the grounding. An identifier they did not notice is not on the list, so a clean run is evidence and
  not proof.

## Amendments

- **2026-08-20** — Created.

## Related

- [`00-overview.md`](00-overview.md) — `CON-2`, `CON-3`.
- [`04-interfaces-and-external-systems.md`](04-interfaces-and-external-systems.md) — `CON-11` (`EXT-1`), `CON-12` (`EXT-8`).
- `questions/0005-agpl-linkability-for-internal-consumers.md` — `CON-4`'s open half.
- `questions/0001-product-and-crate-naming.md` — `CON-9`'s gate.
