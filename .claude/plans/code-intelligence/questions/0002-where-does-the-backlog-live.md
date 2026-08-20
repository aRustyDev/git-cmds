# Question 0002 — Where does the backlog live?

- **Status:** open
- **Date:** 2026-08-20
- **Blocks:** `scheduled` gaps in [`GAPS.md`](../GAPS.md) cannot be handed off. Not blocking the
  requirements work itself — the register carries acceptance criteria inline until this is decided.

## The question

`GAPS.md` defines a gap lifecycle that ends in a `scheduled` disposition, which means "on the
backlog". **There is no backlog.** This repository has no issue tracker configured, no `.beads/`
directory, and no Plane project has been named for it.

## What the register needs from whatever is chosen

Not a preference — these are requirements that fall out of the gap process:

1. **Bidirectional linking.** The gap names the item and the item names the gap. One-way links rot,
   and a backlog item that has lost its provenance gets worked on faith.
2. **Confidence and disposition survive the handoff.** An item that no longer records that it came
   from a `presumed` gap has lost the single most important thing about it.
3. **The revisit trigger is queryable.** Accepted gaps are swept by checking triggers; if that means
   reading every entry by hand, it will stop happening.
4. **Agent-legible.** A meaningful share of the work will be done by agents, so items need hard
   acceptance criteria and named files rather than motivational prose.

## Options

### A. A Plane project
The estate uses Plane as the human-first register, one project per effort, with goals and intent
written for people.

**For:** matches house practice; good for the human narrative — why scope changed, what the goal is.
**Against:** a separate system to keep in sync; weaker for agent consumption; needs a project created
and its identifier recorded.

### B. A beads database
The estate uses beads as the agent-first register — token-efficient, explicitly instructed, hard
acceptance criteria, each item naming the files it touches and the command that proves it done.

**For:** built for exactly the agent-legibility requirement; dependencies are first-class, which suits
a gap register where entries block each other.
**Against:** needs a database provisioned, and — learned the hard way in a sibling effort — **a new
beads database must be added to the backup list or it has no backup at all.** That provisioning is
infrastructure work owned elsewhere, not something to create as a side effect.

### C. Both, as the estate does elsewhere
Plane for humans, beads for agents, linked both ways.

**For:** each register does what it is good at; this is the established pattern.
**Against:** two systems and a synchronisation obligation. Worth it at scale, heavy for a plan that
has not started.

### D. GitHub issues on this repository
**For:** zero provisioning; adjacent to the code; PRs close issues natively.
**Against:** diverges from house practice; weaker dependency modelling; and it is public if the
repository is.

### E. Keep the register as the backlog until there is real volume
Treat `GAPS.md` itself as the backlog — `scheduled` entries carry acceptance criteria inline, and no
external system exists.

**For:** no provisioning, no synchronisation, and the provenance cannot be lost because there is no
handoff. Honest for a plan with eight entries.
**Against:** does not scale past a few dozen items; poor for parallel work; no dependency queries.

## Recommendation

**E now, with a trigger to revisit.** The register has eight entries and the requirements work has not
started; standing up a tracker for that is ceremony. Revisit when either **the register passes ~25
entries** or **more than one person or agent is working items concurrently** — at which point B or C,
matching house practice.

Recording this as a decision rather than a drift matters: option E is only defensible *with* the
trigger. Without one it is just "we never set up a backlog".

## Notes

Whichever is chosen, `GAPS.md` remains the register of record for *gaps*. The backlog tracks *work*.
A gap and its work item are different objects with different lifecycles — a gap can be refuted, which
is not a state a work item has.
