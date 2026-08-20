# SPEC 05 — Security requirements

> **Aspirational.** Status markers record justification strength, not implementation status.
> Vocabulary as ratified in [`GLOSSARY.md`](../GLOSSARY.md).

- **Date:** 2026-08-20
- **Applies to:** the **service shape** unless a requirement says otherwise. The local shape is a
  single user on their own machine with no network listener; see `SEC-14` for what that does and does
  not excuse.
- **Adversaries and assets** are in `analysis/0006-threat-model.md`. Security requirements without a
  stated adversary are unfalsifiable, which is why that document exists.

## Identity

### SEC-1 — Identity MUST be per-principal, never a shared secret. *(VERIFIED)* — **inherited-negative**

**MUST.** Every request carries an identity belonging to exactly one **principal** — one human or one
agent. A credential shared between callers does not satisfy this requirement at any strength.

Specifically, the credential MUST carry:

1. **A subject** identifying the principal.
2. **An expiry.** A credential with no expiry cannot be rotated in response to compromise; it can only
   be replaced everywhere at once.
3. **Claims** sufficient for the authorisation decision in `SEC-4`.

**Why this is evidenced:** the reference implementation's only credential was a **single static shared
token with no claims and no expiry**. It was validated at an edge proxy which then **deliberately
stripped the header before the upstream hop**, so the upstream service received no identity at all.
The question "which agent asked for this?" was therefore unanswerable **in principle**, not merely
unimplemented — there was nothing in the request to log.

**Verification:** a request bearing a credential for principal A is attributed to A and not to B, and
an expired credential is rejected. Asserted at the upstream service, not at any proxy in front of it —
because the measured failure was precisely that the proxy held the only identity.

### SEC-2 — Authentication MUST be delegatable to an external provider, and MUST validate the whole token. *(assumed)*

**MUST.** OAuth2 or JWT (`EXT-10`). Validation MUST include signature, expiry, issuer and audience. A
token that is merely well-formed is not authenticated.

**Verification:** a matrix of malformed, expired, wrong-issuer, wrong-audience and wrong-signature
tokens, each rejected with the correct distinct reason.

### SEC-3 — Every request MUST be attributable to exactly one principal, end to end. *(VERIFIED)* — **inherited-negative**

**MUST.** Attribution MUST survive every hop between the caller and the code that performs the action.
An intermediary MUST NOT be the only holder of the identity.

**MUST also:** a session identifier is not an identity (`IF-8`). The principal is carried
independently of any session, connection or transport artefact.

**Why this is evidenced:** as `SEC-1`. The identity terminated at a proxy and was removed before the
action, so the log of the action could not name its actor.

**Verification:** with 10,000 distinct principals in a load profile, a sampled action is traced to its
principal through every layer. The test that matters is the negative one: **remove the attribution at
any hop and the request MUST fail rather than proceed anonymously.**

## Authorisation

### SEC-4 — Every operation MUST be authorised against the principal's claims. *(assumed)*

**MUST.** Authorisation is checked for every operation on every surface, at the single termination
point required by `IF-3`. Read operations are authorised too — repository visibility is an
authorisation decision (`IF-9`), not a filter applied afterwards.

**Verification:** the executable route-enumeration check from `IF-3`, plus per-operation denial tests.

### SEC-5 — Authorisation MAY be delegated to an external decision point. *(assumed)*

**SHOULD.** RBAC, ABAC or ReBAC (`EXT-11`). Where delegated, the platform supplies the principal, the
action and the target; it does not embed policy.

**Verification:** a policy fixture; the same request is allowed and denied under two policies with no
platform change.

### SEC-6 — Every mutating and every security-relevant action MUST produce a durable audit record. *(assumed)*

**MUST.** The record names the **principal**, the action, the target, the outcome, the time and the
correlation identifier from `OPS-5`. Security-relevant includes authentication failures, authorisation
denials, and changes to provider or identity configuration (`IF-12`).

**MUST:** audit records are **append-only** and are **authoritative data** — they cannot be
reconstructed by reindexing (`01-personas-and-flows.md` §D4, `EXT-3`). They must survive upgrade and
must be backed up.

**Verification:** every mutating operation, exercised once, produces exactly one record with all
fields populated. Asserted as a coverage check over the mutating-operation set derived from `IF-2`,
so a new mutating operation without an audit record fails the build rather than shipping quietly.

### SEC-7 — Authorisation MUST fail closed. *(VERIFIED)* — **inherited-negative**

**MUST.** Every one of these MUST result in denial:

1. Authentication is not configured.
2. A credential is absent, malformed or expired.
3. The external decision point is unreachable or times out.
4. A lock, lease or coordination primitive protecting a decision cannot be acquired.

**Unset configuration MUST authorise nothing.** A deployment that has not been configured is not
open — it is unusable, and that is the correct behaviour.

**Why this is evidenced:** two measured failures, in the same direction. First, in the reference
implementation an **unset token authorised every request** — the validation function returned true when
no token was configured. Second, a contended global registry lock **degraded to unlocked** after a
timeout, with a logged warning and an acknowledged possibility of a lost update. Both fail open, and
both do so quietly.

**Verification:** each of the four conditions above, provoked individually, yields a denial. The
unconfigured case is the important one and MUST be asserted explicitly, because it is the one that
looks like it works.

**The consequence we dislike:** a first-run experience in the service shape that refuses everything
until identity is configured. That is worse onboarding and it is the right trade, because the
alternative is a deployment that was open for the period between starting and being configured.

### SEC-8 — The unit of authorisation MUST be specified before authorisation is implemented. *(operational)*

**MUST.** Repository, path within a repository, or graph node — these are materially different
designs, and node-level authorisation in particular changes every traversal, because a traversal that
must not reveal an unauthorised node cannot simply filter its output.

**This SPEC does not decide it.** Filed as `questions/0007`.

**Verification:** an accepted decision record exists before the first authorisation implementation
commit. Checkable from history.

**Why it is called out:** if the answer is per-node, then `FR-024`'s blast radius must be able to
return `undetermined` because a path passed through a node the caller may not see — which is a
**functional** requirement that does not exist yet. The authorisation unit is not only a security
decision.

## Abuse and resource protection

### SEC-9 — Expensive operations MUST be bounded and MUST be attributable to a principal for the purpose of limiting. *(assumed)*

**MUST.** An unbounded transitive traversal over a large graph is expensive and reachable by any
caller (`PERF-5`). With up to 10,000 agents, bounding is a capacity-planning requirement, not only a
correctness one.

**MUST:** limits are applied per **principal**, not per source address. A fleet of agents behind one
egress address is one address and thousands of principals; a per-address limit would either throttle
them all as one or be useless.

**Verification:** a per-principal limit is enforced with many principals sharing a source address, and
with one principal arriving from many addresses.

### SEC-10 — Caller-supplied paths and locations MUST be validated against a server-side policy. *(VERIFIED)*

**MUST.**

1. **File paths** derived from caller input MUST be confined to the repository they claim, resolved
   through symbolic links rather than by string prefix. A lexical prefix check passes a symlink that
   points outside.
2. **Repository locations** submitted for acquisition MUST be admitted only by an
   operator-configured allowlist, never by a caller-supplied flag (`EXT-12`).
3. **Admitting internal hostnames is a deliberate decision with a cost.** It is what makes the
   service usable on internal remotes, and it is also what widens server-side request forgery reach.
   The decision MUST be recorded, and the mitigation MUST be the allowlist rather than a
   name-pattern heuristic.

**Why this is evidenced:** the grounding recorded prior art whose path checks were **lexical, with no
link resolution**, so a symlink inside an indexed repository pointing outside would pass; and whose
location guard blocked literal private addresses but performed **no name resolution at all**, so an
internal hostname resolving to a private address was admitted unconditionally. Both are the same
class of error — validating the string rather than the destination.

**Verification:** a symlink escape fixture is refused; a non-allowlisted host is refused; a
caller-supplied parameter cannot extend the allowlist. Each with a positive control proving the
same operation succeeds for a legitimate target.

### SEC-11 — A configured credential MUST NOT be readable back through any surface. *(assumed)*

**MUST.** Provider credentials, remote credentials and identity secrets are write-only through every
interface. A configuration read returns presence and metadata, never the value.

**MUST also:** runtime provider configuration (`IF-12`) is the highest-risk write in the system,
because it accepts a credential and may redirect where code text is sent. It MUST be restrictable to
absence (`IF-13`), MUST be audited (`SEC-6`), and MUST require an authorisation distinct from ordinary
read access.

**Verification:** a configuration read after a credential write returns no secret material; a
principal with read entitlement cannot perform the write.

### SEC-12 — A credential MUST NOT appear in an argument list, a log, an error or a response. *(VERIFIED)*

**MUST.** See `FR-046`. Process argument lists are readable by any local process, so passing a secret
in one exposes it to every process on the host. Diagnostic and trace facilities that would echo a
credential MUST be suppressed rather than captured.

**Why this is evidenced:** this estate has measured argument-list exposure directly, and the grounding
recorded prior art that specifically scrubbed transport-trace environment variables because inheriting
them dumps request headers — including an injected credential — into captured output.

**Verification:** a secret-scanning assertion over all captured output from a credentialed operation,
**with a positive control** proving the scan detects the secret when it is deliberately leaked. A scan
that cannot fail proves nothing.

### SEC-13 — Source code MUST be treated as confidential, and its egress MUST be enumerable. *(operational)*

**MUST.** The platform's assets are the organisation's source code and everything derived from it.
Every path by which code text or an embedding of it leaves the deployment MUST be enumerable from
configuration:

1. The embedding provider (`EXT-7`).
2. Any AI provider configured at runtime (`IF-12`).
3. Telemetry, which MUST NOT carry code text (`OPS-6`).
4. Error reports and diagnostics.

**Verification:** a restricted-network test asserts no outbound connection to any host other than
those the configuration names. This is the same test as `EXT-7`'s and is the only way to establish
the enumeration is complete rather than merely written down.

**Note for the local shape:** the client-side path is where this bites hardest. If a browser-based
surface is ever given a provider credential directly, code text leaves the machine under a per-user
key with no audit trail. That would be a deliberate decision and it is not currently specified.

### SEC-14 — The local shape MUST NOT listen on a network interface, and MUST NOT rely on that for its security. *(assumed)*

**MUST.** The local shape has no network listener and therefore no authentication. Both halves matter:

1. It MUST NOT open a listening socket. If it ever needs one — to serve the web UI locally, for
   instance — then `SEC-1` through `SEC-7` apply to it, and it is no longer the local shape as
   specified here.
2. **Binding to a loopback address MUST NOT be treated as a security control** for anything reachable.
   A loopback bind is a deployment accident away from a public one.

**Why the second clause exists:** the grounding recorded prior art whose in-code justification for
having no authentication was that it *"has been safe only because it bound loopback"* — and whose
running deployment was then observed bound to all interfaces and reachable from the local network,
with an invalid credential returning success because the header was not read at all. The control and
the assumption drifted apart silently.

**Verification:** the local binary opens no listening socket, asserted by inspection of its sockets
during a full operation. Separately, an executable check asserts that any code path capable of
binding a non-loopback address requires authentication to be configured.

### SEC-15 — Transport security and browser-facing controls MUST be specified rather than defaulted. *(operational)*

**MUST.** For the service shape:

1. Transport MUST be encrypted, and the platform MUST NOT assume an intermediary provides it.
2. Cross-origin policy MUST be operator-configured. **No third-party origin may be present by
   default** — a hardcoded external origin in an allowlist is a standing grant nobody reviewed.
3. Security-relevant response headers MUST be set on API responses, not only on the surfaces that
   serve documents.
4. Where the platform sits behind a proxy, the number of trusted hops MUST be configured explicitly.
   Trusting a caller-supplied forwarding header unconditionally makes the client the author of its own
   apparent identity; trusting none of it collapses every caller into one, which turns a per-caller
   limit into a single global one. **Both failure directions MUST be considered**, and the second is
   the one that fails quietly.

**Verification:** a configuration test per clause. Clause 2 is asserted as the **absence** of any
default origin — a grep-level check, because the failure is a literal in a list.

## Privacy

### SEC-16 — Telemetry, logs and audit records MUST NOT contain source code or embeddings. *(operational)*

**MUST.** They may contain identifiers, counts, durations, repository identities and principals. They
MUST NOT contain code text, query text that embeds code, or vectors.

**Verification:** a scanning assertion over emitted signals for a fixture whose code contains a unique
marker; the marker appears in no signal, with a positive control proving the scan works.

### SEC-17 — A principal's queries MUST NOT be visible to another principal. *(assumed)*

**MUST.** With ~10,000 agents and 20–50 humans sharing a deployment, one caller's query history is
another caller's intelligence about what is being worked on.

**Verification:** no surface exposes another principal's requests, results or history; audit access is
itself an authorised operation.

## Verification

### What is proven

- **Three inherited negatives are carried here** — `SEC-1`, `SEC-3`, `SEC-7` — each tagged and each
  naming the measured failure. `SEC-10`, `SEC-12` and `SEC-14` additionally cite measured prior-art
  failures without being on the canonical inherited-negative list.
- **`SEC-7` enumerates four fail-open conditions rather than stating a principle**, because the
  measured failures were specific: an unset credential authorising everything, and a contended lock
  degrading to unlocked.
- **Every "MUST NOT leak" requirement specifies a positive control** (`SEC-12`, `SEC-13`, `SEC-16`).
  A scan that cannot fail is not evidence, and this estate has measured verification tooling passing
  against deliberately wrong inputs.
- **`SEC-8` identifies a functional consequence of a security decision** — per-node authorisation
  would require blast radius to return `undetermined` on an unauthorised path, which is a functional
  requirement that does not yet exist.

### What is NOT proven

- **The authorisation unit is undecided** (`questions/0007`), so `SEC-4` cannot be implemented and
  `SEC-8` is the gate. This is the largest open question in this file.
- **No threat model has been reviewed.** `analysis/0006-threat-model.md` is the requirements author's
  draft; nobody with a security remit has read it.
- **`SEC-9`'s per-principal limiting has no capacity model behind it.** The limit values are not set
  here, because `SCALE-4`'s in-flight fraction is itself an assumption.
- **`SEC-13`'s enumeration is only as complete as the configuration surface**, and the configuration
  surface is not designed yet. A future feature that calls out will be a new egress path, and nothing
  currently forces it to be declared.
- **`SEC-14`'s local-shape exemption rests on "no listener".** If a local web UI is ever wanted — and
  it plausibly is, since the web UI is the primary human surface — this requirement is where that
  decision surfaces, and it is not decided.
- **Nothing here addresses a compromised agent.** With 10,000 agent principals, one of them behaving
  badly with legitimate credentials is the likeliest incident, and the only requirements that bear on
  it are `SEC-6` (it is recorded) and `SEC-9` (it is bounded). Detection and response are unspecified.

## Amendments

- **2026-08-20** — Created.

## Related

- `analysis/0006-threat-model.md` — assets, principals, trust boundaries per shape, out-of-scope adversaries.
- [`04-interfaces-and-external-systems.md`](04-interfaces-and-external-systems.md) — `IF-3`, `IF-8`, `IF-9`, `IF-13`, `EXT-10`–`EXT-12`.
- `questions/0007-what-is-the-unit-of-authorisation.md` — the decision `SEC-8` defers.
