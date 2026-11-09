"""Verify every change between consecutive versions before it is reported (spec 0001 section 1.4).

A rung that moves 0 -> 1 or 1 -> 0 between two versions of one line is either a real change in the
document or a coding inconsistency. For each move, the quote behind the 1 is looked up in the text of
the version coded 0. If the same passage is there, the move is flagged for a cross-version ruling.

Usage: python3 -m coding.change_check   -> coding/change_flags.csv
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

from analysis import tables
from analysis.ladder import RUNGS
from coding.check import doc_text, quote_found

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "coding" / "change_flags.csv"
FIELDS = ["line", "from_doc", "to_doc", "risk", "rung", "from_value", "to_value", "quote", "page", "quote_in_other"]


def main() -> int:
    docs = tables.documents()
    c = tables.codes()
    q = {(r["doc_id"], r["risk"], r["rung"]): r for r in csv.DictReader((ROOT / "coding" / "quotes.csv").open(encoding="utf-8"))}
    out = []
    for ch in tables.changes(c, docs):
        va, vb = c[(ch["from_doc"], ch["risk"])], c[(ch["to_doc"], ch["risk"])]
        for g in RUNGS:
            if va[g] == vb[g]:
                continue
            has, lacks = (ch["to_doc"], ch["from_doc"]) if vb[g] else (ch["from_doc"], ch["to_doc"])
            qr = q.get((has, ch["risk"], g), {})
            found = quote_found(qr.get("quote", ""), doc_text(docs[lacks])) if qr.get("quote") else False
            out.append({"line": f"{ch['developer']}-{ch['line']}", "from_doc": ch["from_doc"], "to_doc": ch["to_doc"],
                        "risk": ch["risk"], "rung": g, "from_value": va[g], "to_value": vb[g],
                        "quote": qr.get("quote", ""), "page": qr.get("page", ""), "quote_in_other": int(found)})
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} rung moves, {sum(r['quote_in_other'] for r in out)} with the same passage in the other version")
    return 0


if __name__ == "__main__":
    sys.exit(main())
