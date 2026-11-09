"""Tables behind the charts and the write-up, all derived from coding/codes.csv."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from analysis.ladder import RUNGS, change_label, gaps, level, union
from coding.check import RISKS
from frameworks.census import SIGNATORIES

ROOT = Path(__file__).resolve().parents[1]
RISK_LABEL = {"cyber": "Cyber", "biochem": "Bio and chem", "ai_rnd": "AI R&D automation",
              "autonomy": "Autonomy", "loss_of_control": "Loss of control"}


def documents() -> dict[str, dict]:
    return {r["doc_id"]: r for r in csv.DictReader((ROOT / "frameworks" / "documents.csv").open(encoding="utf-8"))}


def codes() -> dict[tuple[str, str], dict]:
    out = {}
    for r in csv.DictReader((ROOT / "coding" / "codes.csv").open(encoding="utf-8")):
        out[(r["doc_id"], r["risk"])] = {g: int(r[g]) for g in RUNGS}
    return out


def latest(c=None, docs=None) -> list[dict]:
    """One row per developer and risk: rungs taken from any document in its current set."""
    c, docs = c or codes(), docs or documents()
    by_dev = defaultdict(list)
    for d in docs.values():
        if d["current"] == "1":
            by_dev[d["developer"]].append(d["doc_id"])
    rows = []
    for dev, ids in by_dev.items():
        for risk in RISKS:
            have = [c[(i, risk)] for i in ids if (i, risk) in c]
            if len(have) != len(ids):
                continue
            u = union(have)
            rows.append({"developer": dev, "name": SIGNATORIES[dev], "docs": " + ".join(sorted(ids)), "risk": risk, **u,
                         "level": level(u), "level_loose": level(u, "loose"), "gaps": " ".join(gaps(u))})
    return rows


def versions(c=None, docs=None) -> list[dict]:
    c, docs = c or codes(), docs or documents()
    rows = []
    for (did, risk), v in c.items():
        d = docs[did]
        rows.append({"doc_id": did, "developer": d["developer"], "line": d["line"], "published": d["published"],
                     "risk": risk, **v, "level": level(v)})
    first = {}
    for d in docs.values():
        k = (d["developer"], d["line"])
        first[k] = min(first.get(k, d["published"]), d["published"])
    return sorted(rows, key=lambda r: (r["developer"], first[(r["developer"], r["line"])], r["published"], RISKS.index(r["risk"])))


def changes(c=None, docs=None) -> list[dict]:
    c, docs = c or codes(), docs or documents()
    lines = defaultdict(list)
    for d in docs.values():
        lines[(d["developer"], d["line"])].append(d)
    out = []
    for (dev, line), ds in lines.items():
        ds = sorted(ds, key=lambda d: d["published"])
        for a, b in zip(ds, ds[1:]):
            for risk in RISKS:
                if (a["doc_id"], risk) not in c or (b["doc_id"], risk) not in c:
                    continue
                va, vb = c[(a["doc_id"], risk)], c[(b["doc_id"], risk)]
                la, lb = level(va), level(vb)
                moved = [g for g in RUNGS if va[g] != vb[g]]
                out.append({"developer": dev, "line": line, "from_doc": a["doc_id"], "to_doc": b["doc_id"], "risk": risk,
                            "level_from": la, "level_to": lb, "change": change_label(la, lb),
                            "rungs_added": " ".join(g for g in moved if vb[g]), "rungs_removed": " ".join(g for g in moved if va[g])})
    return out
