"""Stratified sample of final codes for an independent check (spec 0001 section 1.5).

5 cells per rung and value (6 rungs x {0, 1} = 60), drawn with a fixed seed from coding/codes.csv.
Usage: python3 -m coding.verify_sample  -> coding/verify_sample.csv
"""
from __future__ import annotations

import csv
import random
import sys
from pathlib import Path

from analysis.ladder import RUNGS

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261109


def main() -> int:
    codes = list(csv.DictReader((ROOT / "coding" / "codes.csv").open(encoding="utf-8")))
    quotes = {(r["doc_id"], r["risk"], r["rung"]): r for r in csv.DictReader((ROOT / "coding" / "quotes.csv").open(encoding="utf-8"))}
    rng = random.Random(SEED)
    out = []
    for g in RUNGS:
        for v in ("0", "1"):
            pool = [r for r in codes if r[g] == v]
            for r in rng.sample(pool, min(5, len(pool))):
                q = quotes.get((r["doc_id"], r["risk"], g), {})
                out.append({"doc_id": r["doc_id"], "risk": r["risk"], "rung": g, "value": v,
                            "quote": q.get("quote", ""), "page": q.get("page", "")})
    with (ROOT / "coding" / "verify_sample.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} cells sampled")
    return 0


if __name__ == "__main__":
    sys.exit(main())
