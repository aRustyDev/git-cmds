# Capability gaps — process and register

- **Date:** 2026-08-20 · **Status:** living document
- **Purpose:** record what the product cannot yet do, or what our design does not yet cover, with
  enough structure that gaps become backlog items rather than folklore — and a cycle that returns to
  them.

## Why this needs a process at all

A gap noticed in a sync and not written down is indistinguishable from a gap nobody noticed. The
failure mode is not forgetting that gaps exist; it is **remembering them as vague unease** — "I think
there was something about YAML" — which is unactionable and unassignable.

The second failure mode is subtler and worse: **acting on an unverified gap.** Building for something
absent that turns out to have been present all along is pure waste, and it is easy, because a gap
feels like knowledge. The register exists to keep confidence attached to every claim.

## The two dimensions

The requester's terms — *known, accepted, discovered, inferred, presumed, hypothetical* — are two
different things mixed together, and separating them is what makes the register queryable.
**`accepted` is a disposition; the rest are statements of confidence.** A gap can be *known and
accepted*, or *known and scheduled*, or *hypothetical and open* — and "show me every high-confidence
gap we have not dispositioned" is the question the register has to be able to answer.

### Confidence — how do we know this is a gap?

| Value | Means | Verified? |
|---|---|---|
| `known` | Someone looked, and it is absent. Names what was checked. | ✅ |
| `discovered` | Surfaced unexpectedly during other work, and confirmed. | ✅ |
| `inferred` | Not directly observed, but follows necessarily from a requirement or another gap. | ⚠️ derived |
| `presumed` | Believed absent; nobody has checked. | ❌ |
| `hypothetical` | Speculative. May not be a gap, or may not be wanted. | ❌ |

**The binding rule: nothing unverified gets scheduled.** A `presumed` or `hypothetical` gap must be
promoted to `known` — or `refuted` — before any work is scheduled against it. `inferred` may be
scheduled only when the inference chain is written down and its premise is itself verified.

This rule exists because of a measured failure in the prior grounding: a capability whose *name*
matched a backlog item was repeatedly taken as evidence the item was done, and adversarial refutation
overturned three of four such verdicts. The same trap runs in reverse — a capability whose absence is
*assumed* is not a gap until someone looks.

### Disposition — what are we doing about it?

| Value | Means | Requires |
|---|---|---|
| `open` | Recorded, not yet triaged. | — |
| `scheduled` | Accepted as work; on the backlog. | verified confidence + a backlog link |
| `accepted` | **Deliberate WON'T.** A known hole we are living with. | a reason **and** a revisit trigger |
| `refuted` | Investigated; not actually a gap. | what was checked |
| `closed` | Filled. | where it landed |

**`accepted` is not `closed`.** An accepted gap is a documented, deliberate hole — and it needs a
**revisit trigger** (a condition, not a date) or it becomes permanent by default, which is how "we
decided not to" silently becomes "nobody remembers deciding".

### Kind — what sort of gap is it?

One register, not three, because separate registers guarantee one gets forgotten.

| Kind | Means |
|---|---|
| `capability` | The product should be able to do something it cannot. |
| `coverage` | A required capability exists but our design has no home for it. |
| `verification` | We cannot currently prove a requirement is met. |
| `knowledge` | We do not know something we need to know to decide. |

## Entry format

```markdown
### GAP-nnn — <short title>
- **kind:** capability | coverage | verification | knowledge
- **confidence:** known | discovered | inferred | presumed | hypothetical
- **disposition:** open | scheduled | accepted | refuted | closed
- **source:** which sync, document, or conversation surfaced it (and the date)
- **missing:** what the system cannot do, stated as behaviour
- **consequence:** what goes wrong if this stays open
- **verification:** how we would confirm this is genuinely a gap — **required** when confidence is
  presumed or hypothetical
- **revisit:** the condition that reopens this — **required** when disposition is accepted
- **relates:** blocks / blocked by / sync that owns it / backlog link
```

Numbering is sequential and never reused. Gaps are not renumbered when refuted — a refuted gap is
evidence, and its number stays.

## The cycle

Four rhythms, deliberately different in frequency.

### 1. File on sight — continuous
Anyone who notices a gap files it immediately with whatever confidence is honest, including
`hypothetical`. **A low-confidence entry is far better than a missing one**, because the register can
raise confidence later and cannot invent an entry nobody wrote.

### 2. Triage — at the start of every sync
New entries since the last sync get a `kind`, a `confidence` and a `disposition`. This is fast — a few
minutes — and its only job is that nothing sits `open` and unclassified for two syncs running.

### 3. Verification pass — before each track boundary
Every `presumed` and `hypothetical` entry either gets verified (→ `known` or `refuted`) or gets a dated
"still unverified" stamp. **An entry carrying three unverified stamps is escalated**: either someone
verifies it, or it is explicitly `accepted` with a revisit trigger. Drifting indefinitely is the one
outcome not allowed.

### 4. Sweep — at each track boundary (end of A, B, C, D)
Full register review:
- Re-check every `accepted` entry against its revisit trigger. Triggers fire silently; nothing else
  will notice.
- Re-check `inferred` entries whose premise has since changed — an inference is only as good as what
  it rested on.
- Escalate entries unchanged across two sweeps.
- Confirm every `scheduled` entry still has a live backlog link.

## Backlog integration

A `scheduled` gap becomes an item in the project's work register. **Which register that is has not been
decided** — see `questions/0002-where-does-the-backlog-live.md`. Whatever it turns out to be, it must
support:

- **A bidirectional link.** The gap names the item; the item names the gap. One-way links rot.
- **Confidence and disposition surviving the handoff.** A backlog item that has lost the fact it came
  from a `presumed` gap will get worked on faith.
- **A queryable revisit trigger**, so accepted gaps can be swept without reading every entry.

Until that is decided, `scheduled` entries carry their acceptance criteria inline here, so the
handoff is a copy rather than a reconstruction.

## Register

Seeded 2026-08-20 to demonstrate each confidence level. Not exhaustive — the A-track syncs will fill
it out substantially, and A4 exists specifically to generate `hypothetical` entries.

### GAP-001 — TUI surface is unspecified
- **kind:** capability · **confidence:** `discovered` · **disposition:** `open`
- **source:** requester instruction, 2026-08-20, adding a TUI to the named interface set
- **missing:** a terminal user interface. The original capability list names a web UI, a CLI and an
  agent protocol; a TUI appeared later and has no requirements at all.
- **consequence:** an interface with no requirements gets built to whatever the implementer assumed,
  or silently dropped. It also changes B5's answer — four surfaces over a shared contract is a
  different design from three.
- **relates:** owned by **B5**. Decide: specify it, or decline it explicitly.

### GAP-002 — The relational store has no home in the design
- **kind:** coverage · **confidence:** `known` · **disposition:** `open`
- **source:** review of the requester's module-seam sketch, 2026-08-19
- **missing:** the requirements demand a relational store that swaps between embedded and server
  deployments. The sketch's only SQL-shaped component is marked out of scope and described as an ORM
  for a different product, so the required store is unplaced.
- **consequence:** either a required capability is missing, or two unrelated concerns get merged into
  one component because they share the word "SQL".
- **relates:** owned by **B1**, then **B3** for placement. Blocks the placement table.

### GAP-003 — Change→symbol mapping may need a structural diff
- **kind:** capability · **confidence:** `inferred` · **disposition:** `open`
- **source:** inferred from the diff-impact accuracy requirement, `discussions/0001` axis 5
- **missing:** mapping a **line**-based diff onto symbols is lossy — a moved function reads as a large
  deletion and an unrelated insertion. Accurate diff impact plausibly needs a **syntax-aware** diff.
- **consequence:** if this is real and unaddressed, diff impact is inaccurate in exactly the case it
  is most wanted: a refactor that moved code.
- **verification:** the inference rests on the premise that line-diff→symbol mapping loses accuracy on
  moves and reformatting. Confirm with a worked example before scheduling.
- **relates:** owned by **C3**; gates **A5**.

### GAP-004 — Several non-functional requirements are unverifiable
- **kind:** verification · **confidence:** `known` · **disposition:** `open`
- **source:** requirements-coverage review, 2026-08-19
- **missing:** no telemetry. The read-concurrency property, the n95 latency budget and index staleness
  are all requirements with no means of measurement.
- **consequence:** unverifiable requirements are wishes. They also cannot appear under
  `### What is proven` in any SPEC verification section, which makes the SPEC dishonest by omission.
- **relates:** owned by **D1**. This is why D1 is the one Track-D sync that is not merely practice.

### GAP-005 — Declarative infrastructure configuration is not analysable
- **kind:** capability · **confidence:** `known` · **disposition:** `open`
- **source:** grounding of the prior art, 2026-08-19
- **missing:** analysis of declarative infrastructure and configuration formats — infrastructure-as-code
  and container-orchestration manifests. No surveyed prior art covers these well, and they are a large
  share of what agents in this environment actually work on.
- **consequence:** the graph is blind to a substantial fraction of the target corpus, so impact and
  search answers are confidently incomplete for it.
- **relates:** owned by **C1**. Note these formats are declarative, so most of a
  general-purpose language-extraction contract is meaningless for them — a lighter path may be the
  right shape.

### GAP-006 — The write side is barely explored
- **kind:** capability · **confidence:** `hypothetical` · **disposition:** `open`
- **source:** A4 framing, 2026-08-20
- **missing:** beyond a single rename operation, the surveyed prior art is overwhelmingly read-only.
  Codemods, mechanical migrations and multi-step refactors guided by the graph may be a significant
  opportunity — or may be out of scope entirely.
- **consequence:** if it is an opportunity, we will not notice while specifying a read-only product.
- **verification:** **speculative — do not schedule.** A4 should develop or kill it. Promote only with
  a concrete named capability and a consumer who wants it.
- **relates:** owned by **A4**.

### GAP-007 — Derived graph structures may need stable identities across runs
- **kind:** capability · **confidence:** `inferred` · **disposition:** `open`
- **source:** inferred from the grounding, 2026-08-19
- **missing:** structures derived by whole-graph algorithms — clusters and derived flows — are
  recomputed wholesale. If their identifiers are also part of the query surface, then recomputation
  changes answers rather than merely costing time, and any stored reference to them breaks.
- **consequence:** cached results, saved views, agent-held references and cross-run comparison all
  become unreliable, silently.
- **verification:** confirm that derived identifiers are (or will be) externally visible. If they are
  purely internal, this is refuted.
- **relates:** owned by **B3**; interacts with **A5** and the incrementality requirements.

### GAP-008 — No confidence model for contract-inferred cross-repository edges
- **kind:** knowledge · **confidence:** `presumed` · **disposition:** `open`
- **source:** cross-repository requirements review, 2026-08-19
- **missing:** an edge inferred from a declared contract between repositories is weaker evidence than
  a call observed in code, and we presume no surveyed prior art offers a usable confidence model for
  the distinction.
- **consequence:** cross-repo impact answers mix observed and inferred edges at equal weight, which
  either overstates blast radius or hides real reach — and the caller cannot tell which.
- **verification:** **unverified.** Nobody has surveyed prior art for cross-repo edge confidence.
  Check before treating this as a gap.
- **relates:** owned by **B4**; interacts with **A5** axis 3 (edge admissibility).

## How we will know this process failed

- A sync produces a gap that never reaches the register.
- An entry sits `open` and unclassified across two syncs.
- Work gets scheduled against a `presumed` or `hypothetical` entry.
- An `accepted` entry has no revisit trigger, or has one that has fired unnoticed.
- The register and the backlog disagree about what is scheduled.
- Somebody asks "did we ever decide about X?" and the answer requires reading old transcripts.

## Amendments

- **2026-08-20** — Created. Split the requester's six-term taxonomy into orthogonal `confidence` and
  `disposition` axes, added `kind`, and seeded eight entries covering every confidence level.
