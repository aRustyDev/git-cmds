# Handoff — requirements authoring, 2026-08-20

- **From:** the requirements author (this session)
- **To:** the Software Architect, and whoever schedules work
- **Branch:** `docs/code-intelligence-spec`. Nothing pushed, no PR opened.

## The statement that binds a person, not a document

**I am clean-room tainted and must not write the implementation.**

I read the prior grounding research — the findings, research and questions documents and the licensing
decision record under `~/repos/woven/forks/gitnexus/.claude/plans/hosted-service/`. Those documents
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
3. **Ask the requester `questions/0007`'s sub-question:** is the target corpus many repositories or one
   large monorepo? It may eliminate three of four authorisation options at no cost.
4. **Hold A1 and A3.** The inputs are ready and the corpus is unreviewed.
5. **Hold A2 properly.** The glossary is ratified for this corpus and not jointly. It is the document
   every later one depends on, so a unilateral ratification is the weakest link in the A-track.
6. **Then B1**, with `analysis/0002` and `discussions/0002` as input — and the standing rule: never
   settle a seam on the requirements author's authority.

## What must not happen

- **Nobody should read the grounding research.** It is cited for provenance in `specs/09`, not as
  further reading.
- **`FR-036` must not ship as generated prose** because that was the easiest thing to build. That would
  add an AI-provider code-egress path through a documentation feature (`questions/0011`, `GAP-016`).
- **The local shape must not be built as the service shape with flags off.** `analysis/0005` marks
  twenty requirements as having no local counterpart, and `PERF-1` is the trap: the local shape's
  natural design — one shared handle behind one lock — is precisely the measured prior-art failure, and
  read concurrency cannot be added later.
- **The async decision must not be deferred past backend screening.**
- **I must not write the implementation.**

## Related

- [`README.md`](README.md) — the plan map and current status.
- [`SYNCS.md`](SYNCS.md) `## Status` — per-sync inputs as they now stand.
- [`GAPS.md`](GAPS.md) — 17 entries, with the 2026-08-20 triage and verification pass.
- [`QUESTIONS.md`](QUESTIONS.md) — the eleven questions and the dependency chain that matters.
