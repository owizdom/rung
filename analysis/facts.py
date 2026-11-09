"""Every number the methods note and the write-up use, computed from the data (spec 0001 AT11)."""
from __future__ import annotations

import csv
from pathlib import Path

from analysis import tables
from analysis.ladder import RUNGS, level
from coding.check import RISKS, agreement, load_pass

ROOT = Path(__file__).resolve().parents[1]
# Versions in documents.csv that METR's list (metr.org/fsp, fetched 2026-11-09) does not carry as an entry:
# METR links one FCF entry (now v2), the April 28 re-issue of Preparedness v2, Meta's March 2025 text,
# Magic's live page, and has no Samsung entry. Checked against frameworks/discovery/census_agent.csv notes.
METR_MISSED = ["anthropic-fcf-1.0", "anthropic-fcf-1.1", "openai-pf-2.0", "meta-scaling-2025.02", "magic-agi-1.0", "samsung-asf-2025.02"]
WORD = {i: w for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen".split())}


def facts() -> dict:
    f = {}
    docs = tables.documents()
    c = tables.codes()
    L = tables.latest(c, docs)
    devs = sorted({r["developer"] for r in L})
    top = {d: max(r["level"] for r in L if r["developer"] == d) for d in devs}
    top_loose = {d: max(r["level_loose"] for r in L if r["developer"] == d) for d in devs}
    f["n_versions"] = len(docs)
    f["n_current"] = sum(d["current"] == "1" for d in docs.values())
    f["n_devs"] = len(devs)
    f["n_threshold_any"] = sum(v >= 2 for v in top.values())
    f["n_response_any"] = sum(v >= 3 for v in top.values())
    f["n_acc_any"] = sum(v == 4 for v in top.values())
    f["n_acc_any_loose"] = sum(v == 4 for v in top_loose.values())
    f["acc_devs"] = sorted(tables.SIGNATORIES[d] for d, v in top.items() if v == 4)
    f["zero_devs"] = sorted(tables.SIGNATORIES[d] for d, v in top.items() if v == 0)
    for k in RISKS:
        lv = [r["level"] for r in L if r["risk"] == k]
        for s, name in ((1, "mention"), (2, "threshold"), (3, "response"), (4, "acc")):
            f[f"{k}_{name}"] = sum(x >= s for x in lv)
    with_resp = [d for d in devs if any(r["response"] and r["threshold"] for r in L if r["developer"] == d)]
    f["n_with_resp"] = len(with_resp)
    for g in ("acc_decider", "acc_external", "acc_unmet"):
        f[f"n_{g}"] = sum(1 for d in with_resp if any(r[g] and r["response"] and r["threshold"] for r in L if r["developer"] == d))
    name = lambda d: tables.SIGNATORIES[d]
    for g in ("acc_decider", "acc_external", "acc_unmet"):
        f[f"missing_{g}"] = sorted(name(d) for d in with_resp
                                   if not any(r[g] and r["response"] and r["threshold"] for r in L if r["developer"] == d))
    f["loose_join"] = sorted(name(d) for d in devs if top_loose[d] == 4 and top[d] < 4)
    f["no_threshold_devs"] = sorted(name(d) for d in devs if top[d] < 2)
    f["gap_cells"] = sum(1 for r in L if "response" in r["gaps"].split())
    f["gap_devs"] = sorted({tables.SIGNATORIES[r["developer"]] for r in L if "response" in r["gaps"].split()})
    ch = tables.changes(c, docs)
    f["n_up"] = sum(x["change"] == "added" for x in ch)
    f["n_down"] = sum(x["change"] in ("softened", "removed") for x in ch)
    f["n_softened"] = sum(x["change"] == "softened" for x in ch)
    f["n_removed"] = sum(x["change"] == "removed" for x in ch)
    f["n_pairs"] = len({(x["from_doc"], x["to_doc"]) for x in ch})
    adj = list(csv.DictReader((ROOT / "coding" / "adjudication.csv").open(encoding="utf-8")))
    f["n_adjudicated"] = len(adj)
    f["n_cells"] = len(docs) * len(RISKS) * len(RUNGS)
    ag = agreement(ROOT / "coding" / "passes" / "A", ROOT / "coding" / "passes" / "B")
    f["kappa"] = {g: v[0] for g, v in ag["rungs"].items()}
    f["kappa_level"] = ag["level"][0]
    f["n_disagree"] = sum(v[1] for v in ag["rungs"].values())
    xv = list(csv.DictReader((ROOT / "coding" / "cross_version.csv").open(encoding="utf-8")))
    f["n_xv_cells"] = len(xv)
    q = list(csv.DictReader((ROOT / "coding" / "quotes.csv").open(encoding="utf-8")))
    f["source"] = {s: sum(r["source"].startswith(s) for r in q) for s in ("agreed", "adjudicated", "cross-version", "consistency")}
    f["n_metr_missed"] = len(METR_MISSED)
    assert set(METR_MISSED) <= set(docs), "METR_MISSED names a document not in the list"
    vr = ROOT / "coding" / "verify_results.csv"
    if vr.exists():
        v = list(csv.DictReader(vr.open(encoding="utf-8")))
        f["verify"] = {k: sum(r["verdict"] == k for r in v) for k in ("correct", "wrong", "unsure")}
    return f


if __name__ == "__main__":
    import json
    print(json.dumps(facts(), indent=1))
