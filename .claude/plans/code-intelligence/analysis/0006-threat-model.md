# Analysis 0006 — Threat model

- **Date:** 2026-08-20 · **Status:** draft by the requirements author. **Nobody with a security remit
  has reviewed this.**
- **Purpose:** the security requirements in `specs/05` are unfalsifiable without stated adversaries and
  assets. This document supplies them, and nothing more — it is deliberately short.
- **Vocabulary:** [`GLOSSARY.md`](../GLOSSARY.md)

## Assets

Ranked by what their loss costs, not by how much of the system they occupy.

| # | Asset | Why it matters | Where it lives |
|---|---|---|---|
| A1 | **Source code, and everything derived from it** | The organisation's intellectual property. An embedding is a lossy but real derivative; a graph is a structural description precise enough to reconstruct architecture. | graph, vector, text-search stores; every response |
| A2 | **The audit trail** | The only record of who did what, and **the only asset no amount of reindexing can recover** | relational store |
| A3 | **Credentials** — remote git, embedding and AI providers, identity secrets | Each grants access to something outside this system | configuration; relational store |
| A4 | **Job state** | Authoritative, unrecoverable, and the thing an operator plans capacity against | relational store |
| A5 | **Query history per principal** | With ~10 000 agents and 20–50 humans sharing a deployment, what one principal is asking is intelligence about what is being worked on | logs, audit trail |
| A6 | **Availability of the read surface** | An agent fleet blocked is a fleet idle | serving stage |

**A1 is the asset, and its most under-appreciated property is that it leaves the system by design** —
to an embedding provider, to a configured AI provider, and in every response. `SEC-13` exists because
the interesting question is not whether code egresses but whether the egress paths are enumerable.

## Principals and their trust level

| Principal | Trust | Notes |
|---|---|---|
| **Platform administrator** | high | Can configure providers, acquire repositories, change identity integration. Compromise is total. |
| **Human developer** | medium | Entitled to some repositories. Authenticated. |
| **Agent** | medium, and **numerous** | Same entitlement class as a developer, ~200× the population, acting autonomously. |
| **Unauthenticated caller** | none | Should reach nothing in the service shape. |
| **A configured provider** (embedding, AI) | **medium, and outside the boundary** | Receives A1 by design. Trusted not to retain or leak it, on contractual rather than technical grounds. |
| **A git remote** | low | Supplies untrusted input (source) and receives a credential. |

## Trust boundaries, per shape

### Service shape

```text
     unauthenticated network
  ─────────────────────────────  B1: authentication and authorisation terminate here
     authenticated principals (humans, agents)
  ─────────────────────────────  B2: repository entitlement per principal
     serving stage
  ─────────────────────────────  B3: store access (network hop per store)
     graph · vector · relational · optional slots
  ─────────────────────────────  B4: egress to providers and remotes
     embedding provider · AI provider · git remotes
```

| Boundary | Requirements | The failure to design out |
|---|---|---|
| **B1** | `SEC-1`, `SEC-2`, `SEC-7`, `IF-3` | Terminating identity at an intermediary that strips it before the action, so the action cannot be attributed. Measured in prior art. |
| **B2** | `SEC-4`, `SEC-8`, `IF-9` | Entitlement resolved per process rather than per request, so one deployment cannot serve two audiences. Measured in prior art. |
| **B3** | `OPS-7`, `COR-4` | A store failure answered from whatever remained, presented as complete. |
| **B4** | `SEC-13`, `EXT-7`, `EXT-12` | An egress path nobody enumerated. A caller-supplied location becoming a server-side fetch. |

### Local shape

```text
     the user's own machine — one user, no listener
  ─────────────────────────────  B4 only: egress to providers
     embedding provider · AI provider
```

**There is exactly one boundary locally, and it is B4.** No B1, because there are no principals; no B2,
because there is one user; B3 collapses to file access.

**Consequence, and it is the counter-intuitive one:** the local shape is *less* secure at B4 in the
ways that matter, because a provider credential there sends A1 off the machine with **no operator, no
audit trail and no egress policy**. `analysis/0005` records the same finding. The instinct that "local
is safer" holds for B1–B3 and fails for B4.

## Adversaries in scope

| # | Adversary | Capability | Primary mitigations |
|---|---|---|---|
| T1 | **Unauthenticated network caller** | Reach the service's listening port | `SEC-1`, `SEC-7` — and specifically the unconfigured case, which is the one that looks like it works |
| T2 | **Authenticated principal exceeding entitlement** | Valid credential, requests a repository they may not see | `SEC-4`, `IF-9`, and `SEC-8`'s unresolved unit |
| T3 | **Compromised or misbehaving agent** | Valid credential, high volume, autonomous | `SEC-6` (recorded), `SEC-9` (bounded per principal). **Detection and response are unspecified — see the gap below.** |
| T4 | **Malicious repository content** | Controls the source the parser reads | `COR-7`, `QA-5`. A parser is an untrusted-input boundary. |
| T5 | **Caller-supplied location or path** | Controls a string that becomes a fetch or a file read | `SEC-10`, `EXT-12`. Operator allowlist, link-resolved paths. |
| T6 | **Local process on the host** | Reads argument lists and environment | `SEC-12`. Credentials never in argv. |
| T7 | **Curious insider** | Legitimate access, wants to see others' activity | `SEC-17`, `SEC-6` (audit access is itself authorised) |
| T8 | **Browser-based attacker** | Cross-origin request from a page the user visits | `SEC-15` — and no third-party origin present by default |

## Adversaries explicitly out of scope

Stated so their absence is a decision:

- **A hostile platform administrator.** Compromise is total by construction; nothing here mitigates it.
- **A hostile provider.** A configured embedding or AI provider receives source-derived data by design.
  The control is contractual and the choice of provider; not technical.
- **A hostile store operator**, in the service shape. The stores hold A1 in the clear.
- **Nation-state or supply-chain compromise of dependencies.** Track **D3** covers signing, provenance
  and SBOM as engineering practice; this model does not treat it as an adversary.
- **Physical access** to a developer's machine in the local shape.
- **Side channels** — timing, cache, or inference of A1 from response latencies.

## The gap this model surfaces

**T3 is the likeliest incident and the least mitigated.** With up to ~10 000 agent principals acting
autonomously, one of them behaving badly with a legitimate credential is a routine expectation, not a
tail risk. The corpus offers two requirements against it — the action is recorded (`SEC-6`) and it is
bounded (`SEC-9`) — and **nothing about detecting it or responding to it**:

- No anomaly signal. `OPS-6` forbids per-principal metric labels for cardinality reasons, which is
  correct and also removes the obvious detection surface.
- No credential revocation requirement beyond `SEC-1`'s expiry.
- No rate-limit response policy — what happens after the limit is hit, and whether repeated limiting
  escalates.

`specs/05` records this in its own not-proven section. It is filed as `GAP-013`, and it is the single
most substantive thing this threat model found that the requirements do not cover.

## Verification

### What is proven

- **Every asset, boundary and adversary maps to at least one requirement**, or is explicitly listed as
  out of scope. There is no adversary in the in-scope table without a mitigation.
- **Four of the eight in-scope adversaries are mitigated by requirements whose need was *measured***
  in prior art rather than imagined — T1, T2, T6, and B3's degradation failure.
- **The local shape's single boundary is identified as its weak one**, contradicting the intuition that
  a local tool has a smaller attack surface in every respect.

### What is NOT proven

- **No security reviewer has read this.** It is a requirements author's model and should be treated as a
  first draft.
- **T3 is under-mitigated and the model says so.** `GAP-013`.
- **The asset ranking is judgement.** In particular, whether A1 or A2 ranks first depends on whether the
  organisation's concern is confidentiality or accountability, and nobody has been asked.
- **The out-of-scope list is not risk-accepted by anyone.** It records the author's scoping, not a
  decision with an owner.
- **No boundary has been tested**, because nothing exists. Every mitigation is a requirement, not a
  control.

## Amendments

- **2026-08-20** — Created.

## Related

- `specs/05-security-requirements.md` — the requirements every mitigation column cites.
- `analysis/0005-deployment-shape-contrast.md` — the same local-shape counter-finding, from applicability.
- `GAPS.md` — `GAP-013`, the T3 detection-and-response gap this document surfaced.
