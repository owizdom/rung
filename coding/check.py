"""Coding checks (spec 0001 AT5 to AT7).

A coding pass writes one JSON file per document to coding/passes/<pass>/<doc_id>.json:
  {"doc_id", "coder", "codebook", "coded_at", "other_risks": [...],
   "risks": {<risk>: {<rung>: {"value": 0|1, "quote": str, "page": str, "note": str, "from_image": bool?}}}}
Every 1 needs a verbatim quote from the document; every 0 needs a note.

Usage: python3 -m coding.check [--agreement A B]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from analysis.ladder import RUNGS, ACC, level

ROOT = Path(__file__).resolve().parents[1]
RISKS = ["cyber", "biochem", "ai_rnd", "autonomy", "loss_of_control"]

KEYWORDS = {
    "cyber": r"cyber|vulnerabilit|exploit|hacking|offensive security",
    "biochem": r"biolog|chemical|cbrn|bioweapon|pathogen|toxin",
    "ai_rnd": r"r&d|research and development|self-improv|automat\w* (?:of )?(?:ai|ml|machine learning) research|(?:ai|ml) research",
    "autonomy": r"autonom|self-replicat|replicat|resource acquisition|self-proliferat",
    "loss_of_control": r"loss of control|misalign|decept|scheming|sandbag|undermin|exfiltrat|human oversight|shut ?down|instrumental reasoning",
}


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("­", "").replace("ﬁ", "fi").replace("ﬂ", "fl")
    s = s.replace("–", "-").replace("—", "-").replace("‑", "-")
    s = re.sub("[​‌‍⁠﻿]", "", s)
    s = re.sub(r"-\s*\n\s*", "", s)  # hyphenated line breaks
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def quote_found(quote: str, text: str) -> bool:
    q = norm(quote)
    if not q:
        return False
    t = norm(text)
    if q in t:
        return True
    # pdftotext can drop the space or keep the hyphen at a line-broken word; compare without either
    squash = lambda x: re.sub(r"[\s\-]", "", x)
    return squash(q) in squash(t)


def zero_screen_text(text: str) -> dict[str, bool]:
    low = text.lower()
    return {k: bool(re.search(p, low)) for k, p in KEYWORDS.items()}


def kappa(a: list[int], b: list[int]) -> float:
    n = len(a)
    assert n == len(b) and n > 0
    po = sum(x == y for x, y in zip(a, b)) / n
    cats = sorted(set(a) | set(b))
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    if pe == 1:
        return 1.0 if po == 1 else 0.0
    return (po - pe) / (1 - pe)


def weighted_kappa(a: list[int], b: list[int], k: int = 5) -> float:
    """Quadratic-weighted kappa over ordinal levels 0..k-1."""
    n = len(a)
    assert n == len(b) and n > 0
    w = lambda i, j: ((i - j) ** 2) / ((k - 1) ** 2)
    obs = sum(w(x, y) for x, y in zip(a, b)) / n
    pa = [a.count(i) / n for i in range(k)]
    pb = [b.count(i) / n for i in range(k)]
    exp = sum(pa[i] * pb[j] * w(i, j) for i in range(k) for j in range(k))
    if exp == 0:
        return 1.0
    return 1 - obs / exp


def validate(rec: dict) -> list[str]:
    probs = []
    did = rec.get("doc_id", "?")
    risks = rec.get("risks", {})
    for risk in RISKS:
        cell = risks.get(risk)
        if cell is None:
            probs.append(f"{did}: missing risk {risk}")
            continue
        for g in RUNGS:
            c = cell.get(g)
            if c is None:
                probs.append(f"{did}: missing {risk}.{g}")
                continue
            if c.get("value") not in (0, 1):
                probs.append(f"{did}: {risk}.{g} value {c.get('value')!r} not in [0, 1]")
            elif c["value"] == 1 and not (c.get("quote") or "").strip():
                probs.append(f"{did}: {risk}.{g}=1 without a quote")
            elif c["value"] == 0 and not (c.get("note") or "").strip():
                probs.append(f"{did}: {risk}.{g}=0 without a note")
        if all(g in cell and cell[g].get("value") in (0, 1) for g in RUNGS):
            v = {g: cell[g]["value"] for g in RUNGS}
            if v["threshold"] and not v["mentioned"]:
                probs.append(f"{did}: {risk} threshold=1 but mentioned=0")
            if any(v[k] for k in ACC) and not (v["threshold"] or v["response"]):
                probs.append(f"{did}: {risk} accountability without threshold or response")
    return probs


def _note_key(s: str) -> str:
    return norm(s)


BOILERPLATE = {"not in text", "", "n/a", "none", "nothing to decide for this risk"}


def shared_notes(a: dict, b: dict) -> int:
    """Independence test: identical free-text notes across two passes on one document."""
    n = 0
    for risk in RISKS:
        for g in RUNGS:
            na = _note_key(a["risks"][risk][g].get("note", ""))
            nb = _note_key(b["risks"][risk][g].get("note", ""))
            if na and na == nb and na not in BOILERPLATE and len(na) > 25:
                n += 1
    return n


MANIFEST = ROOT / "frameworks" / "documents.csv"


def documents(manifest: Path | None = None) -> dict[str, dict]:
    m = manifest or MANIFEST
    return {r["doc_id"]: r for r in csv.DictReader(Path(m).open(encoding="utf-8"))}


def doc_text(d: dict) -> str:
    """Quotes may come from the plain or the layout text layer of the PDF."""
    out = []
    for k in ("text_path", "layout_path"):
        p = d.get(k)
        if p and Path(p).expanduser().exists():
            out.append(Path(p).expanduser().read_text(encoding="utf-8", errors="replace"))
    return "\n".join(out)


def load_pass(d: Path) -> dict[str, dict]:
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(d.glob("*.json"))}


def verify_pass(pass_dir: Path, manifest: Path | None = None) -> list[str]:
    """AT5 and AT6 over one pass on disk."""
    probs = []
    docs = documents(manifest)
    for did, rec in load_pass(pass_dir).items():
        probs += validate(rec)
        d = docs.get(did)
        if d is None:
            probs.append(f"{did}: not in documents.csv")
            continue
        text = doc_text(d)
        hits = zero_screen_text(text)
        for risk in RISKS:
            for g in RUNGS:
                c = rec["risks"].get(risk, {}).get(g, {})
                if c.get("value") == 1 and not c.get("from_image") and not quote_found(c.get("quote", ""), text):
                    probs.append(f"{did}: {risk}.{g} quote not found: {c.get('quote', '')[:90]!r}")
            m = rec["risks"].get(risk, {}).get("mentioned", {})
            if m.get("value") == 0 and hits[risk] and len((m.get("note") or "").strip()) < 15:
                probs.append(f"{did}: {risk}.mentioned=0 but keywords occur; needs a real note")
    return probs


def cells(rec: dict) -> dict[tuple[str, str], int]:
    return {(risk, g): rec["risks"][risk][g]["value"] for risk in RISKS for g in RUNGS}


def agreement(a_dir: Path, b_dir: Path) -> dict:
    a, b = load_pass(a_dir), load_pass(b_dir)
    common = sorted(set(a) & set(b))
    out = {"documents": len(common), "rungs": {}}
    for g in RUNGS:
        xa = [a[d]["risks"][r][g]["value"] for d in common for r in RISKS]
        xb = [b[d]["risks"][r][g]["value"] for d in common for r in RISKS]
        out["rungs"][g] = (round(kappa(xa, xb), 3), sum(x != y for x, y in zip(xa, xb)), len(xa))
    la = [level({g: a[d]["risks"][r][g]["value"] for g in RUNGS}) for d in common for r in RISKS]
    lb = [level({g: b[d]["risks"][r][g]["value"] for g in RUNGS}) for d in common for r in RISKS]
    out["level"] = (round(weighted_kappa(la, lb), 3), sum(x != y for x, y in zip(la, lb)), len(la))
    out["shared_notes"] = {d: shared_notes(a[d], b[d]) for d in common if shared_notes(a[d], b[d]) >= 3}
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("passes", nargs="*", default=["A", "B"])
    ap.add_argument("--agreement", action="store_true")
    ap.add_argument("--base", default="coding/passes", help="folder holding the pass folders")
    ap.add_argument("--manifest", default=None)
    a = ap.parse_args(argv)
    bad = 0
    base = ROOT / a.base
    for p in a.passes:
        d = base / p
        if not d.exists():
            continue
        for x in verify_pass(d, Path(a.manifest) if a.manifest else None):
            print(f"[{p}] {x}")
            bad += 1
    if a.agreement and len(a.passes) == 2:
        res = agreement(*(base / x for x in a.passes))
        print(f"documents {res['documents']}")
        for g, (k, dis, n) in res["rungs"].items():
            print(f"{g:14s} kappa {k:6.3f}  disagreements {dis}/{n}")
        k, dis, n = res["level"]
        print(f"{'level (qwk)':14s} kappa {k:6.3f}  disagreements {dis}/{n}")
        print("shared notes >= 3:", res["shared_notes"] or "none")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
