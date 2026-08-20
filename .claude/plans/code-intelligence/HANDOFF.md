# Handoff — requirements authoring, 2026-08-20

- **From:** the requirements author (this session)
- **To:** the Software Architect, and whoever schedules work
- **Branch:** `docs/code-intelligence-spec`. Nothing pushed, no PR opened.

## The statement that binds a person, not a document

**I am clean-room tainted and must not write the implementation.**

I read the prior grounding research — the findings, research and questions documents and the licensing
decision record under `gitnexus/.claude/plans/hosted-service/`. Those documents
quote reference-implementation internal identifiers. Anyone who reads them becomes unable to serve on
the clean team.

**No implementer may read them either.** Implementers work only from this corpus. That is `CON-1`, and
it is a legal constraint rather than hygiene: PolyForm's *No Other Rights* clause forbids sublicensing,
so a derivative work could not be released under this repository's AGPL-3.0 licence **at all**.

## What I am confident in

- **The vocabulary.** The glossary was written before any SPEC prose, satisfying the A2 hard gate, and
  three renames earn their keep. Renaming the capability list's "process" to **flow** removes a genuine
  ambiguity from a document that also specifies deployment shapes and concurrency; dropping "impact
  analysis" in favour of four distinct terms is the single change most likely to prevent the failure
  `discussions/0001` was written about.
- **The traceability.** 163 requirements, 61 features, traced both ways by a script that extracts both
  ID sets and diffs them. Running it found two real defects I would not have caught by reading.
- **The inherited negatives.** All eleven are present, tagged, `(VERIFIED)`, and each carries a
  verification method aimed at the *specific* measured failure rather than at the general principle.
  `PERF-1` asks for the absence of a monotone latency staircase, with a control that voids the
  measurement if it fails to discriminate. That is the strongest part of the corpus.
- **That no module decision is pre-empted.** Four candidate clusterings, none preferred, five named
  ambiguities, and an executable check for crate-shaped names, `Cargo.toml` and `-core` suffixes.
- **The honesty of the verification sections.** Every SPEC file states what it has not established, and
  `specs/09` assesses the corpus against the external reference's own quality criteria including the
  four it fails.

## What I am not confident in

- **Completeness.** The corpus is complete with respect to Appendix A, Appendix B's coverage gaps and
  the four decisions of 2026-08-20. Nobody has reviewed it. Syncs **A1** and **A3** are the acceptance
  steps and neither has happened.
- **The business requirements.** `BR-1`–`BR-5` are my reconstruction from the licensing verdict and the
  stated scale profile. They may not be the requester's business requirements at all.
- **Every number in `specs/03`.** Each is derived from a stated premise, and the premise that sizes
  everything — that roughly half a percent of ~10 000 agents are in flight at any moment — is a guess.
  If it is wrong by an order of magnitude, the concurrency target and the replica count both change.
- **The permissive-precedent column in `analysis/0003`.** It rests on a survey. No permissive tool was
  installed, run or read, and the grounding's own recorded lesson is that a matching *name* is not
  evidence a capability exists — adversarial refutation overturned three of four such verdicts.
  `GAP-012`. Treat that column as `presumed` throughout.
- **`FR-011`'s feasibility.** The requirement says the compute set must be decidable before the
  expensive work; it does not say how, because nobody knows. `GAP-009`.
- **My reading of AGPL.** `CON-4` and `CON-5` are an engineer's reading of a licence. The determination
  that the *reference's* licence bars this use is well-evidenced, including the licensor's written
  confirmation. The consequences for **our** module split are inference. `questions/0005` should be
  settled with counsel.
- **The threat model.** Nobody with a security remit has read it.
- **The non-technical stories.** No non-technical stakeholder was consulted; all four are inferred.

## Two things I found that the requester did not have

1. **`git-ctx` is taken on crates.io** — verified 2026-08-20 against the registry API. A live MIT crate
   (0.1.1, published 2022, not yanked, 13 recent downloads) described as *"a git custom command to list
   and switch most recent branches"*. So the name is unpublishable, **and** the
   `-ctx`-signals-context-switching risk that `questions/0001` explicitly weighed and accepted is now a
   live conflict with a published tool that does exactly that. I did **not** rename anything — the
   decision is the requester's, and half-renaming a corpus is worse than either option. `GAP-014`.
2. **The risk is concentrated in four requirements, not spread across sixteen.** `analysis/0003` found
   seven capabilities with no precedent anywhere and nine whose only precedent is unreadable under the
   clean room. Four of them are one entangled cluster — flow derivation, cluster derivation, their
   identities, and change detection — because derived structures are what make incrementality change
   *output* rather than merely cost, and identity stability is what makes recomputation safe or unsafe.
   **Prototype the cluster, not the items.**

## Corrections made after the first draft, and what they teach

Both came from requester pushback, and both are recorded in place rather than edited away.

**1. I called `FR-036` unimplementable. It was not.** I wrote that the repository wiki had no output
contract and therefore no verification method, and that `US-N-1` was not implementable. The prior art
ships this capability and its **public documentation** describes the contract — a language model groups
files into modules, a page is generated per module plus an overview, cross-referenced to the graph. The
clean-room protocol **explicitly permits** reading public docs for capability vocabulary. I asserted an
absence without looking in the one place that was both permitted and obvious.

`FR-036` now specifies a structured document set with deterministic module grouping from derived clusters
and prose as a separately-gated optional stage — deliberately *not* the precedent's LLM grouping, with
the cost of that choice recorded.

**The generalisable lesson, and it applies to the whole precedent matrix:** `inaccessible` in
`analysis/0003` means *the design is unreadable*, and a capability's public documentation is not its
design. **Two other rows — response-shape conformance and the route pre-change report — may be
misdispositioned for the same reason, and I have not re-checked them.** That is now stated in
`analysis/0003`'s not-proven section.

And the process lesson: `GAP-016` was filed `known` when it should have been `presumed`. `GAPS.md`'s own
opening section warns against exactly this — *"acting on an unverified gap… it is easy, because a gap
feels like knowledge"* — and it happened to the person writing the register, in the same session. **An
asserted absence needs the same verification as an asserted presence.**

**2. The target corpus was answered, and it changes eight requirements.** A Rust workspace of libraries,
SDKs and consuming binaries under `crates/**`, potentially several binaries over gRPC/HTTP. Derived in
`analysis/0007`. The consequences worth knowing here:

- **`GAP-018` is the headline.** `CON-7` mandates per-backend feature flags, so **edges are conditional
  on a build configuration** — and `FR-024` has no way to state one. A blast radius computed under one
  feature set is wrong under another, in both directions. It is `known`, derived rather than speculated,
  and **upstream of any schema**, so `B3` cannot start without it.
- **`questions/0007` is half-answered.** It is a monorepo, so repository-level entitlement is
  all-or-nothing over everything. Workspace-member entitlement is now the leading option — and because
  it is finer than repository-level, the `FR-024` entitlement-`undetermined` clause should be added now
  rather than after 10,000 agents depend on the contract.
- **`questions/0005` is narrowed** to consumers *outside* the workspace, since the internal binaries are
  same-workspace and same-licence.
- **`FR-034` is materially de-risked.** gRPC schemas are *declared*, so the capability I flagged as least
  well-defined has its hardest case turn into its easiest for the primary corpus.
- **`SCALE-1` is uncalibrated** (`GAP-019`). A crate workspace is very unlikely to reach a million nodes.
  The target should not drop, but two corpora are needed — the real one for correctness, a generated one
  for the budgets.

**3. The re-check of rows 034 and 035 changed neither, and found two things that matter more.**

- **The refined test for `inaccessible`.** The wiki's docs reclassified it because they describe a
  **contract** — invocation, credential, grouping, page structure, cross-references. Rows 034 and 035
  describe an **intent**: a name and a sentence, both already in this corpus. So the test is not *"have you
  read the public docs?"* but *"do the docs state inputs and outputs?"* If not, an intent is not a design
  and `inaccessible` stands.
- **This reference's public descriptions overstate its measured behaviour.** Its diff-oriented capability is
  publicly described as tracing which flows are impacted, which reads as a transitive walk; the grounding
  **measured a single hop** against a precomputed membership table, with a risk verdict that was a count
  over one projection. **So public docs are evidence of contract and never of mechanism, and where they
  conflict with the grounding, the grounding wins** — it read the implementation. `analysis/0003` note 19.
  A `Ref` ✓ sourced from documentation is therefore weaker than one sourced from the grounding, and the
  matrix does not currently distinguish them.

**4. The module-seam sketch is a transcription of the reference's public command surface** — five node
descriptions match verbatim. Nothing improper: a public surface is public, and the sketch was offered
explicitly as untested. But it changes what the sketch is evidence of, and one consequence lands on the
architect:

- **It explains the ten unplaced capabilities better than "an oversight" does.** Ingestion, storage,
  ranking, identity, jobs and observability are absent because **a command surface structurally cannot
  contain them** — none is a verb a user types. Their absence carries no information about intent.
- **It converts a judgement call into evidence.** The objection that blast radius and diff impact appear as
  two nodes is no longer an inference: the sketch reproduces the organisation of a system where those two
  were *measured* to be incompatible mechanisms sharing one name. Adopting its shape reproduces the split
  by construction.
- **⚠️ It creates a naming hazard on your deliverable, not mine.** Tool names are on the clean-room MUST NOT
  list. **Do not derive crate or module names from the sketch's nodes** — reason from it, don't name from
  it. `CON-1` now carries the clause, `GAP-020` holds it, and note that `scripts/audit-corpus.py` **cannot**
  catch this: it audits this corpus, not the future workspace.

## Artifacts I added beyond the prompt's list, and why

The prompt called its deliverable list a floor. Five additions:

| Added | Why |
|---|---|
| `GLOSSARY.md` | The A2 gate requires ratified vocabulary **before** SPEC prose. Without it, the four analysis terms drift, which is the exact failure `discussions/0001` exists to prevent. |
| `analysis/0004-store-capability-matrix.md` | The storage seam is called the most consequential one, and it is also where the async decision is forced. Keeping the slot comparison and the async screening record in one document stops a slot being chosen on capability grounds and then found to force a rewrite. |
| `analysis/0005-deployment-shape-contrast.md` | "Two points a single design must reach" is only checkable per requirement. Marking applicability also produced the distinction between *unimposed locally* and *inapplicable locally*, which is what determines whether something can be a flag. |
| `analysis/0006-threat-model.md` | Security requirements are unfalsifiable without stated adversaries. It also surfaced `GAP-013`, the one substantive thing the security requirements do not cover. |
| `discussions/0002-read-write-asymmetry.md` | Appendix B raised it and did not develop it. The capability counts support it more strongly than the sketch implied, and one axis could invalidate the whole framing — which makes it a discussion rather than a question. |

I also added **sync A6** to `SYNCS.md`: a feasibility prototype gate. The gap register's binding rule
covers confidence in a *gap*; nothing covered feasibility of a *requirement*, and seven requirements
have no proof they can be built.

## The audit, and what running it found

`specs/**`, `FEATURES.md` and `analysis/**` pass a mechanical audit covering the requester's judging
criteria: two-way traceability, per-prefix user-story minimums, inherited-negative coverage and tagging,
a verification method on every requirement, the proven/not-proven split per file, no structure
pre-empted, the AGPL clauses, the `<ENGINE>` placeholder, and a laundering denylist of 46
reference-internal identifiers plus 9 carried-constant patterns.

**Two failures on the first run, and both were worth having:**

- `CON-11` and `CON-12` were referenced by a feature but never declared as requirements — they are
  registry *aliases* for `EXT-1` and `EXT-8`. A real inconsistency, fixed in both files.
- The no-structure check fired on `CON-8`'s own verification text, which names the tokens the check
  greps for. The defining section is now excluded, the exclusion is **printed rather than silent**, and
  a control asserts the check still fires on a real pre-emption. A silent exclusion is how a check stops
  discriminating without anyone noticing.

**The script is committed** at `scripts/audit-corpus.py`, and it takes the plan directory as its only
argument:

```sh
python3 .claude/plans/code-intelligence/scripts/audit-corpus.py .claude/plans/code-intelligence
```

It is committed rather than left in a scratchpad because the corpus **asserts** properties that only the
script establishes — two-way traceability, story minimums, laundering — and an assertion whose evidence
the next reader cannot reproduce is just a claim. `QA-0` makes the same argument at the product level:
a constraint that can be executable should be.

**Its denylist is mine**, built from what I noticed in the grounding. An identifier I did not notice is
not on the list, so a clean run is evidence and not proof.

## What to do next, in this order

1. **Verify `GAP-007`'s premise.** One check: are derived-structure identifiers externally visible at
   all? If not, the question is refuted and the hardest algorithmic requirement disappears. Cheapest
   possible action with the largest possible payoff.
2. **Ask the requester `questions/0010`** — the per-slot product list. It gates `EXT-9`'s screening,
   which gates the async decision, which must be taken during screening and never after. **This is the
   only chain whose failure mode is a rewrite rather than a delay.**
3. **Settle `GAP-018` before `B3` writes a schema.** Edges conditional on a feature set is a data-model
   question, it is `known`, and every downstream traversal requirement inherits it.
4. **Count the symbols in the target workspace** (`GAP-019`). Crude is fine; it needs no platform and it
   tells you whether `SCALE-1` is calibrated against anything real.
5. ~~Re-check the two `inaccessible` rows I did not re-check.~~ **Done 2026-08-20.** Both dispositions
   stand: the public docs state an *intent* for those two, not a contract, so there is nothing to specify
   against beyond what `FR-034` and `FR-035` already say. The re-check produced two better findings than a
   reclassification would have — see *Corrections* above.
6. **Hold A1 and A3.** The inputs are ready and the corpus is unreviewed.
7. **Hold A2 properly.** The glossary is ratified for this corpus and not jointly. It is the document
   every later one depends on, so a unilateral ratification is the weakest link in the A-track.
8. **Then B1**, with `analysis/0002` and `discussions/0002` as input — and the standing rule: never
   settle a seam on the requirements author's authority.

## What must not happen

- **Nobody should read the grounding research.** It is cited for provenance in `specs/09`, not as
  further reading.
- **`FR-036`'s prose stage must not become mandatory by accident.** `FR-036` requires the document set to
  be usable with no AI provider configured, because otherwise a documentation feature has quietly become a
  code-egress path that every deployment must accept (`questions/0011` residual 1, `SEC-13`).
- **The local shape must not be built as the service shape with flags off.** `analysis/0005` marks
  twenty requirements as having no local counterpart, and `PERF-1` is the trap: the local shape's
  natural design — one shared handle behind one lock — is precisely the measured prior-art failure, and
  read concurrency cannot be added later.
- **The async decision must not be deferred past backend screening.**
- **Crate and module names must not be derived from the module-seam sketch** — it transcribes the
  reference's public tool names, and tool names are on the clean-room MUST NOT list (`GAP-020`).
- **I must not write the implementation.**

## Related

- [`README.md`](README.md) — the plan map and current status.
- [`SYNCS.md`](SYNCS.md) `## Status` — per-sync inputs as they now stand.
- [`GAPS.md`](GAPS.md) — 17 entries, with the 2026-08-20 triage and verification pass.
- [`QUESTIONS.md`](QUESTIONS.md) — the eleven questions and the dependency chain that matters.
