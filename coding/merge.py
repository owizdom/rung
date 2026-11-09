"""Final codes from pass A, pass B and the adjudication file.

Usage: python3 -m coding.merge [--docs ID ...]
  writes coding/disagreements.csv (cells the passes split on and that have no ruling yet)
  and, when nothing is unresolved, coding/codes.csv and coding/quotes.csv.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from analysis.ladder import RUNGS, gaps, level
from coding.check import RISKS, load_pass

ROOT = Path(__file__).resolve().parents[1]
ADJ = ROOT / "coding" / "adjudication.csv"
XV = ROOT / "coding" / "cross_version.csv"
ADJ_FIELDS = ["doc_id", "risk", "rung", "value", "quote", "page", "ruling"]
DIS_FIELDS = ["doc_id", "risk", "rung", "a_value", "a_quote", "a_page", "a_note", "b_value", "b_quote", "b_page", "b_note"]
CODE_FIELDS = ["doc_id", "risk"] + RUNGS + ["level", "level_loose", "gaps", "other_risks"]


def load_adj() -> dict:
    if not ADJ.exists():
        return {}
    return {(r["doc_id"], r["risk"], r["rung"]): r for r in csv.DictReader(ADJ.open(encoding="utf-8"))}


def load_consistency() -> dict:
    """Codebook v1.2 section F rulings, applied to every document; they override all earlier values."""
    out = {}
    # Rounds apply in order (F1, F1b, F2, F3, then F4, the ruling after the second review); a later round wins.
    for f in sorted((ROOT / "coding").glob("consistency_F*.csv")):
        for r in csv.DictReader(f.open(encoding="utf-8")):
            out[(r["doc_id"], r["risk"], r["rung"])] = {**r, "rule": f.stem.split("_")[1]}
    return out


def load_xv() -> dict:
    """Cross-version rulings: made with both versions side by side; they override earlier values."""
    if not XV.exists():
        return {}
    return {(r["doc_id"], r["risk"], r["rung"]): r for r in csv.DictReader(XV.open(encoding="utf-8"))}


def merge_doc(a: dict, b: dict, adj: dict, xv: dict | None = None, cons: dict | None = None):
    """Final value of every cell. Precedence: consistency ruling > cross-version ruling > adjudication > agreement."""
    did = a["doc_id"]
    xv, cons = xv or {}, cons or {}
    dis, rows, cells = [], [], []
    for risk in RISKS:
        vals = {}
        for g in RUNGS:
            ca, cb = a["risks"][risk][g], b["risks"][risk][g]
            k = (did, risk, g)
            if k in cons:
                r, src = cons[k], f"consistency {cons[k]['rule']}"
            elif k in xv:
                r, src = xv[k], "cross-version"
            elif ca["value"] == cb["value"]:
                r, src = {"value": ca["value"], "quote": ca["quote"], "page": ca["page"], "ruling": ca["note"]}, "agreed"
            elif k in adj:
                r, src = adj[k], "adjudicated"
            else:
                dis.append({"doc_id": did, "risk": risk, "rung": g, "a_value": ca["value"], "a_quote": ca["quote"], "a_page": ca["page"],
                            "a_note": ca["note"], "b_value": cb["value"], "b_quote": cb["quote"], "b_page": cb["page"], "b_note": cb["note"]})
                continue
            vals[g] = int(r["value"])
            cells.append({"doc_id": did, "risk": risk, "rung": g, "value": vals[g], "quote": r.get("quote", "") if vals[g] else "",
                          "page": r.get("page", "") if vals[g] else "", "note": r.get("ruling", r.get("note", "")) if (not vals[g] or src != "agreed") else "",
                          "source": src})
        if len(vals) == len(RUNGS):
            others = sorted(set(a.get("other_risks", [])) | set(b.get("other_risks", [])), key=str.lower)
            rows.append({"doc_id": did, "risk": risk, **vals, "level": level(vals), "level_loose": level(vals, "loose"),
                         "gaps": " ".join(gaps(vals)), "other_risks": "; ".join(others)})
    if dis:
        return None, dis
    merge_doc.quotes = cells
    return rows, dis


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", nargs="*")
    a = ap.parse_args(argv)
    A, B = load_pass(ROOT / "coding" / "passes" / "A"), load_pass(ROOT / "coding" / "passes" / "B")
    ids = sorted(set(A) & set(B))
    if a.docs:
        ids = [i for i in ids if i in a.docs]
    adj = load_adj()
    xv = load_xv()
    cons = load_consistency()
    all_rows, all_dis, all_q = [], [], []
    for did in ids:
        rows, dis = merge_doc(A[did], B[did], adj, xv, cons)
        all_dis += dis
        if rows:
            all_rows += rows
            all_q += merge_doc.quotes
    with (ROOT / "coding" / "disagreements.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=DIS_FIELDS)
        w.writeheader()
        w.writerows(all_dis)
    print(f"documents {len(ids)}, unresolved disagreements {len(all_dis)}")
    if all_dis:
        return 1
    if a.docs:
        print("subset run: codes.csv not written (run without --docs for the final merge)")
        return 0
    with (ROOT / "coding" / "codes.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CODE_FIELDS)
        w.writeheader()
        w.writerows(all_rows)
    with (ROOT / "coding" / "quotes.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["doc_id", "risk", "rung", "value", "quote", "page", "note", "source"])
        w.writeheader()
        w.writerows(all_q)
    print(f"codes.csv: {len(all_rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
