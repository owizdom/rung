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
ADJ_FIELDS = ["doc_id", "risk", "rung", "value", "quote", "page", "ruling"]
DIS_FIELDS = ["doc_id", "risk", "rung", "a_value", "a_quote", "a_page", "a_note", "b_value", "b_quote", "b_page", "b_note"]
CODE_FIELDS = ["doc_id", "risk"] + RUNGS + ["level", "level_loose", "gaps", "other_risks"]


def load_adj() -> dict:
    if not ADJ.exists():
        return {}
    return {(r["doc_id"], r["risk"], r["rung"]): r for r in csv.DictReader(ADJ.open(encoding="utf-8"))}


def merge_doc(a: dict, b: dict, adj: dict):
    did = a["doc_id"]
    dis, rows, quotes = [], [], []
    for risk in RISKS:
        vals = {}
        for g in RUNGS:
            ca, cb = a["risks"][risk][g], b["risks"][risk][g]
            if ca["value"] == cb["value"]:
                vals[g] = ca["value"]
                if ca["value"]:
                    quotes.append({"doc_id": did, "risk": risk, "rung": g, "quote": ca["quote"], "page": ca["page"], "source": "A (agreed)"})
            elif (did, risk, g) in adj:
                r = adj[(did, risk, g)]
                vals[g] = int(r["value"])
                if vals[g]:
                    quotes.append({"doc_id": did, "risk": risk, "rung": g, "quote": r["quote"], "page": r.get("page", ""), "source": "adjudicated"})
            else:
                dis.append({"doc_id": did, "risk": risk, "rung": g, "a_value": ca["value"], "a_quote": ca["quote"], "a_page": ca["page"],
                            "a_note": ca["note"], "b_value": cb["value"], "b_quote": cb["quote"], "b_page": cb["page"], "b_note": cb["note"]})
        if len(vals) == len(RUNGS):
            others = sorted(set(a.get("other_risks", [])) | set(b.get("other_risks", [])), key=str.lower)
            rows.append({"doc_id": did, "risk": risk, **vals, "level": level(vals), "level_loose": level(vals, "loose"),
                         "gaps": " ".join(gaps(vals)), "other_risks": "; ".join(others)})
    if dis:
        return None, dis
    merge_doc.quotes = quotes
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
    all_rows, all_dis, all_q = [], [], []
    for did in ids:
        rows, dis = merge_doc(A[did], B[did], adj)
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
    with (ROOT / "coding" / "codes.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CODE_FIELDS)
        w.writeheader()
        w.writerows(all_rows)
    with (ROOT / "coding" / "quotes.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["doc_id", "risk", "rung", "quote", "page", "source"])
        w.writeheader()
        w.writerows(all_q)
    print(f"codes.csv: {len(all_rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
