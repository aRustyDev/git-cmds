#!/usr/bin/env python3
"""Corpus audit for .claude/plans/code-intelligence.

Checks the nine criteria the requester will judge by, mechanically.
Run:  python3 audit.py <plan-dir>
"""
import re
import sys
import pathlib
import collections

PLAN = pathlib.Path(sys.argv[1])
SPECS = sorted((PLAN / "specs").glob("*.md"))
FEATURES = PLAN / "FEATURES.md"
ANALYSIS = sorted((PLAN / "analysis").glob("*.md"))

REQ_PREFIXES = "BR|FR|PERF|SCALE|COR|OPS|REV|IF|EXT|SEC|CON|QA"
REQ_HEADING = re.compile(rf"^### ((?:{REQ_PREFIXES})-\d+) — ", re.M)
STORY_HEADING = re.compile(r"^### (US-[ADGN]-\d+) — ", re.M)
UC_HEADING = re.compile(r"^### (UC-\d+) — ", re.M)
REQ_REF = re.compile(rf"`((?:{REQ_PREFIXES})-\d+)`")
FEAT_HEADING = re.compile(r"^\| (FEAT-\d+) \|", re.M)

failures = []
notes = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


# ---------------------------------------------------------------- 1. declared requirements
declared = set()
per_file = {}
for f in SPECS:
    ids = set(REQ_HEADING.findall(f.read_text()))
    per_file[f.name] = ids
    declared |= ids
print(f"\n[requirements] {len(declared)} declared across {len(SPECS)} spec files")
for n, ids in per_file.items():
    print(f"    {n}: {len(ids)}")

# ---------------------------------------------------------------- 2. two-way traceability
feat_text = FEATURES.read_text()
feat_ids = set(FEAT_HEADING.findall(feat_text))
# only the forward tables (before the reverse index) count as a feature naming a requirement
forward = feat_text.split("## Reverse index")[0]
referenced = set(REQ_REF.findall(forward))

orphan_reqs = declared - referenced
phantom_refs = referenced - declared
check("every requirement is named by a feature", not orphan_reqs,
      f"orphans: {sorted(orphan_reqs)}" if orphan_reqs else f"{len(declared)} covered")
check("every requirement referenced by a feature exists", not phantom_refs,
      f"phantom: {sorted(phantom_refs)}" if phantom_refs else f"{len(referenced)} refs resolve")

# every feature row must name at least one requirement
featureless = []
for line in forward.splitlines():
    m = re.match(r"^\| (FEAT-\d+) \|", line)
    if m and not REQ_REF.search(line):
        featureless.append(m.group(1))
check("every feature names a requirement", not featureless,
      f"featureless: {featureless}" if featureless else f"{len(feat_ids)} features")

# ---------------------------------------------------------------- 3. user-story minimums
stories = collections.Counter()
for f in SPECS:
    for sid in STORY_HEADING.findall(f.read_text()):
        stories[sid.split("-")[1]] += 1
mins = {"A": 5, "D": 10, "G": 10, "N": 3}
for k, need in mins.items():
    check(f"user stories US-{k}- >= {need}", stories[k] >= need, f"found {stories[k]}")

# ---------------------------------------------------------------- 4. inherited negatives
INHERITED = [
    "PERF-1", "SCALE-3", "FR-068", "FR-011", "FR-018", "SEC-1", "SEC-3",
    "SEC-7", "FR-050", "FR-071", "FR-073",
]
spec_all = "\n".join(f.read_text() for f in SPECS)
missing_inh = [i for i in INHERITED if i not in declared]
check("all 11 canonical inherited-negatives declared", not missing_inh,
      f"missing: {missing_inh}" if missing_inh else "11/11")

# each must be tagged and marked (VERIFIED)
untagged = []
for i in INHERITED:
    m = re.search(rf"^### {re.escape(i)} — .*$", spec_all, re.M)
    if not m or "inherited-negative" not in m.group(0) or "(VERIFIED)" not in m.group(0):
        untagged.append(i)
check("each inherited-negative is (VERIFIED) and tagged", not untagged,
      f"untagged: {untagged}" if untagged else "11/11")

# every MUST requirement needs a verification method somewhere in its section
sections = re.split(r"^### ", spec_all, flags=re.M)
no_verif = []
for sec in sections:
    m = re.match(rf"((?:{REQ_PREFIXES})-\d+) — ", sec)
    if not m:
        continue
    if "**Verification:**" not in sec and "**Verification —" not in sec and "**Verification " not in sec:
        no_verif.append(m.group(1))
check("every requirement states a verification method", not no_verif,
      f"missing: {sorted(no_verif)}" if no_verif else f"{len(declared)} checked")

# ---------------------------------------------------------------- 5. no structure pre-empted
STRUCTURE = [
    (r"Cargo\.toml", "Cargo.toml"),
    (r"\bcrates/", "crates/ path"),
    (r"[a-z0-9]-core\b", "-core suffix"),
]
# CON-8 and its own verification text NAME the tokens this check looks for, so the section that
# defines the check is excluded. The exclusion is printed, never silent — a silent exclusion is how
# a check stops discriminating without anyone noticing.
SELF_REF = re.compile(
    r"^### CON-8 —.*?(?=^### |\Z)|^\| `CON-8` \|.*$|^- \*\*`CON-8`.*$",
    re.M | re.S,
)
hits = []
excluded = 0
audited = SPECS + ANALYSIS + [FEATURES]
for f in audited:
    t = f.read_text()
    stripped, n = SELF_REF.subn("", t)
    excluded += n
    for pat, label in STRUCTURE:
        for mm in re.finditer(pat, stripped):
            hits.append(f"{f.name}: {label} ({mm.group(0)!r})")
check("no module structure pre-empted", not hits,
      "; ".join(hits) if hits else f"clean ({excluded} CON-8 self-reference blocks excluded)")

# Control: the check must still fire on a real pre-emption.
probe = "we will create crates/engine with a Cargo.toml and an engine-core crate"
control_hits = [lbl for pat, lbl in STRUCTURE if re.search(pat, probe)]
check("structure check discriminates (control must fire)", len(control_hits) == 3,
      f"control matched {control_hits}")

# ---------------------------------------------------------------- 6. verification sections
missing_verif_section = []
for f in SPECS:
    t = f.read_text()
    if "## Verification" not in t or "### What is proven" not in t or "### What is NOT proven" not in t:
        missing_verif_section.append(f.name)
check("every SPEC file ends with a proven/not-proven split", not missing_verif_section,
      f"missing: {missing_verif_section}" if missing_verif_section else f"{len(SPECS)}/{len(SPECS)}")

# ---------------------------------------------------------------- 7. laundering denylist
# Reference-internal identifiers and carried constants seen in the grounding research.
DENY = [
    # engine / product internals
    "lbug", "ladybug", "LadybugDB", "kuzu", "Kuzu",
    "repo-manager", "registry.json", "index-lock", "pool-adapter", "lbug-adapter",
    "local-backend", "run-analyze", "parse-cache", "subgraph-extract", "escalation-gate",
    "CodeEmbedding", "CodeRelation", "SCHEMA_FINGERPRINT", "PARSE_CACHE_VERSION",
    "SupportedLanguages", "LanguageProvider", "cluster-enricher", "hybrid-search.ts",
    "detect_changes", "group_sync", "list_repos", "route_map", "GITNEXUS_",
    "gitnexus", "GitNexus", "Akon Labs", "abhigyanpatwari", "PolyForm-Noncommercial",
    "docker-server.mjs", "sessionLock", "withConnLock", "STEP_IN_PROCESS",
    "Leiden", "leiden", "snowflake-arctic", "MAX_POOL_SIZE", "EMBEDDING_DIMS",
    "RRF_K", "entryPointMultiplier", "analyze.lock", "meta.json",
]
# constants that must not be carried
DENY_CONST = [
    r"\bK\s*=\s*60\b", r"\bRRF\b", r"\b384\b", r"\b50_?000\b", r"\b10_?000 rows\b",
    r"\b600,?000 ms\b", r"\b2\.1 KB/node\b", r"\bfive resident\b", r"\b5 resident\b",
]
launder_hits = []
# GitNexus/PolyForm are permitted ONLY in 06-constraints.md (licence provenance)
PROVENANCE_OK = {"06-constraints.md", "09-references-and-appendices.md"}
for f in SPECS + ANALYSIS + [FEATURES]:
    t = f.read_text()
    for term in DENY:
        if term in t:
            if term in ("gitnexus", "GitNexus", "PolyForm-Noncommercial", "Akon Labs") and f.name in PROVENANCE_OK:
                notes.append(f"{f.name}: '{term}' present (permitted: licence provenance)")
                continue
            launder_hits.append(f"{f.name}: {term!r}")
    for pat in DENY_CONST:
        for mm in re.finditer(pat, t):
            launder_hits.append(f"{f.name}: constant {mm.group(0)!r}")
check("laundering: no reference-internal identifier or carried constant", not launder_hits,
      "; ".join(launder_hits) if launder_hits else f"{len(DENY)} terms + {len(DENY_CONST)} patterns clean")

# ---------------------------------------------------------------- 8. AGPL constraints present
con = (PLAN / "specs" / "06-constraints.md").read_text()
check("AGPL linkability consequence stated", "link" in con and "AGPL-3.0" in con)
check("AGPL section 13 consequence stated", "§13" in con)

# ---------------------------------------------------------------- 9. naming discipline
name_hits = []
for f in SPECS + ANALYSIS + [FEATURES]:
    t = f.read_text()
    if re.search(r"`git-graph`", t):
        name_hits.append(f"{f.name}: rejected name git-graph")
check("engine name left unresolved as <ENGINE>", not name_hits and "<ENGINE>" in spec_all,
      "; ".join(name_hits) if name_hits else "placeholder intact")

# ---------------------------------------------------------------- summary
print()
if notes:
    print("notes:")
    for n in sorted(set(notes)):
        print(f"    {n}")
    print()
print(f"{'ALL CHECKS PASSED' if not failures else f'{len(failures)} FAILED: ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
