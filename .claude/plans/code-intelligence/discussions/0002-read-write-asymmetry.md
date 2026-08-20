# Discussion 0002 — Is read/write asymmetry the primary seam?

- **Status:** open — multi-axis, not yet one decision
- **Date:** 2026-08-20
- **Audience:** the requirements author and the Software Architect, jointly
- **Feeds:** sync **B1** (seam pressure test), **B2** (abstractions), **B6** (library/SDK/binary split)

## Why this is a discussion and not a question

A question file records a fork with a decidable answer. This is not that: it is a claim with five
independent axes, several of which have no evidence yet, and the useful output is a shared
understanding of *what would settle it* rather than a decision.

It exists because the requester's own module-seam sketch raised it — *"read and write are not
separated… with a target profile of ~10 000 mostly read-only agents, read/write asymmetry is arguably
the primary seam, and the sketch does not draw it"* — and because the capability inventory turned out
to support the claim more strongly than the sketch's framing suggested.

## The evidence

From `analysis/0001-capabilities.md`, counted rather than asserted:

| | Read capabilities | Write capabilities |
|---|---:|---:|
| Agent (`G`) | 22 | 5 |
| Human user (`U`) | 21 | 4 |
| Admin (`A`) | 7 | **12** |
| Platform developer (`D`) | 11 | 8 |

And from the requester's stated profile: **~20–50 humans, up to ~10 000 agents, predominantly
read-only.**

Two asymmetries, not one:

1. **A capability asymmetry.** 27 of 60 capabilities are read-only; 5 write capabilities serve the
   fleet.
2. **A traffic asymmetry of a different order.** Roughly 200 agents per human, each read-heavy. If
   agents issue even a modest number of reads per task, read traffic exceeds write traffic by orders of
   magnitude, not by a factor.

**These are separate claims and only the first is measured.** The second is arithmetic over a
requester-supplied population estimate, and `SCALE-4` already records that the in-flight fraction — the
number that converts population into concurrency — is a guess that sizes everything.

## Why the asymmetry might be the primary seam

Five arguments, strongest first.

1. **The two sides have opposite non-functional profiles.** Reads are short, numerous,
   latency-sensitive, idempotent and horizontally scalable. Writes are long, rare, latency-tolerant,
   and need durability, cancellation and single-flight coalescing. Almost every requirement in
   `specs/03` applies to one side or the other, rarely both.
2. **A read-only deployment becomes a composition rather than a configuration.** If the seam is real,
   serving a fleet of read-only agents means assembling a binary that *contains no write path* — which
   is a much stronger guarantee than a flag, and it is what `IF-2`'s machine-readable read/write
   classification exists to make possible.
3. **The store requirements differ across it.** Writers need transactions, bulk load and generation
   advancement. Readers need isolation, concurrency and nothing else. A single store contract serving
   both is larger than either, and `analysis/0004`'s conformance suites would be simpler split.
4. **It aligns with the access-plane finding.** `analysis/0005` found that 20 requirements have no
   local counterpart and 17 of them form one coherent identity-and-authorisation block. Reads and
   writes are authorised differently — read entitlement is repository visibility, write entitlement is
   a materially stronger claim — so the access plane sits naturally against this seam.
5. **`PERF-1` lives entirely on the read side.** The read-concurrency property is the single most
   architecturally consequential requirement in the corpus, and it constrains only readers. A seam
   that isolates it makes it defensible; a design that mixes readers and writers behind shared mutable
   state is how the measured prior-art failure happened.

## Why it might not be

Four counter-arguments, and the first is serious enough to be decisive.

1. **Change detection may be a traversal.** `FR-011` requires the *compute* set to be decidable before
   the expensive work. If deciding it means walking the graph — following imports, inheritance and type
   relationships to find what a change reaches — then **the write path's hardest component is a
   traversal, which is the read path's core competence.** The seam would then cut through the most
   complex shared machinery in the system rather than around it.

   **This is unresolved and unresolvable from requirements alone.** `FR-011`'s expansion rule does not
   exist, and `analysis/0003` marks it `elevated` — no precedent anywhere. It is the highest-value thing
   to prototype, and it decides this discussion.

2. **Rename is both.** `FR-050` computes its edit set by reading the graph and then writes source and
   index. Splitting it puts a read dependency inside the write plane, or a write dependency inside the
   read plane. One capability is not much, but it is the one whose correctness clauses are most
   numerous.

3. **The wiki is both.** `FR-036` reads the graph and produces an artefact. Whether that artefact is
   persisted is `questions/0011`, and the answer moves the capability across the seam.

4. **A shared model is unavoidable.** Both sides need the node, edge, flow, cluster and identity
   definitions. So the seam cannot be a clean bisection — there is a third thing beneath both, which
   `analysis/0002` clustering B names explicitly as B1. A "primary seam" that requires a shared
   foundation is a weaker claim than it first sounds.

## The five axes

Stated separately because they can be answered independently, and conflating them is how this becomes
one undifferentiated argument.

| # | Axis | The question | Evidence available |
|---|---|---|---|
| 1 | **Capability partition** | Can every capability be assigned to exactly one side? | Mostly yes; three exceptions (change detection, rename, wiki) |
| 2 | **Store contract** | Do readers and writers need different store contracts, or one? | None. `analysis/0004` defines one profile per slot without asking. |
| 3 | **Deployability** | Must a read-only assembly be possible without the write path present? | Requirement-level yes (`IF-2`), design-level undecided |
| 4 | **Shared machinery** | How much does the write path need traversal? | **Unknown, and decisive.** Depends on `FR-011`. |
| 5 | **Model ownership** | Who owns the node/edge/identity definitions if both sides depend on them? | None. This is `B3`'s. |

**Axis 4 dominates.** Axes 1 and 3 lean toward the seam being real; axes 2 and 5 are unexamined; axis 4
could invalidate the whole framing.

## What would settle it

In order of value per unit of effort:

1. **Prototype the compute-set expansion rule for `FR-011`.** If it is a graph traversal, the seam is
   compromised and `analysis/0002` clustering A or C becomes more attractive. If it can be decided from
   file-level metadata plus a bounded dependency closure computed at write time, the seam holds. **This
   single experiment resolves axis 4 and therefore most of the discussion.**
2. **Draft the read-side store contract in isolation** and see whether it needs anything a writer
   provides. Resolves axis 2 cheaply, on paper.
3. **Decide `questions/0011`** (the wiki's output contract). Removes one of the three exceptions.
4. **Measure the in-flight read fraction** against a real agent workload, once one exists. Turns the
   traffic asymmetry from arithmetic into evidence, and it is `SCALE-4`'s premise as well.

## What must not happen

- **The seam must not be settled on the requirements author's authority.** It is a structural
  decision; the standing rule is that the requirements author brings requirements and the architect
  brings structure.
- **The three exceptions must not be assigned by convenience.** Change detection in particular: putting
  it on the write side because it is "part of indexing" would hide axis 4 rather than answer it.
- **A read/write split must not become two implementations of one behaviour.** `IF-1` and `COR-5` forbid
  it, and the prior art demonstrates the outcome — two entry points to nominally the same functionality
  with different authentication, different concurrency behaviour and different operation inventories.

## How we will know we got this wrong

- A read capability ends up importing something from the write path in order to answer a query.
- The "read-only assembly" turns out to be the full binary with a flag set, because a write-path type
  appears in a read-path signature.
- Change detection is implemented twice — once as an indexing concern and once as a traversal — which
  is `discussions/0001`'s failure mode transplanted into the write plane.
- Somebody asks which side the wiki is on and the answer depends on who is asked.

## Related

- `analysis/0001-capabilities.md` — the counts.
- `analysis/0002-feature-clusters.md` — clustering **B** is this discussion expressed as a candidate grouping.
- `analysis/0003-feature-gaps.md` — why `FR-011` is `elevated`, which is why axis 4 is unresolved.
- `analysis/0005-deployment-shape-contrast.md` — the access-plane block that argument 4 rests on.
- `discussions/0001-what-impact-analysis-means.md` — the same "two mechanisms, one name" failure this must avoid.
