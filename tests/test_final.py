"""Acceptance tests on the final data (spec 0001 AT5, AT6, AT9, AT10)."""
import csv
from pathlib import Path

from analysis import tables
from analysis.ladder import RUNGS
from coding.check import RISKS, doc_text, documents, quote_found

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "out"


def _q():
    return list(csv.DictReader((ROOT / "coding" / "quotes.csv").open(encoding="utf-8")))


def test_every_cell_present_once():
    q = _q()
    keys = [(r["doc_id"], r["risk"], r["rung"]) for r in q]
    assert len(keys) == len(set(keys)) == len(documents()) * len(RISKS) * len(RUNGS)


def test_final_quotes_verbatim():  # AT5
    D = documents()
    texts = {}
    bad = []
    for r in _q():
        if r["value"] == "1":
            t = texts.setdefault(r["doc_id"], doc_text(D[r["doc_id"]]))
            if not quote_found(r["quote"], t):
                bad.append((r["doc_id"], r["risk"], r["rung"], r["quote"][:60]))
    assert bad == []


def test_every_zero_has_a_note():  # AT6
    assert [(r["doc_id"], r["risk"], r["rung"]) for r in _q() if r["value"] == "0" and not r["note"].strip()] == []


def test_codes_match_quotes():
    q = {(r["doc_id"], r["risk"], r["rung"]): int(r["value"]) for r in _q()}
    for (did, risk), v in tables.codes().items():
        for g in RUNGS:
            assert v[g] == q[(did, risk, g)], (did, risk, g)


def _csv(name):
    return [{k: str(v) for k, v in r.items()} for r in csv.DictReader((OUT / name).open(encoding="utf-8"))]


def test_outputs_rebuild_from_codes():  # AT9, AT10
    for name, rows in (("latest.csv", tables.latest()), ("versions.csv", tables.versions()), ("changes.csv", tables.changes())):
        assert _csv(name) == [{k: str(v) for k, v in r.items()} for r in rows], name


def test_minimum_output_has_eight_frameworks():  # AT9
    assert len({r["developer"] for r in tables.latest()}) >= 8
    assert (OUT / "01_latest.png").exists() and (OUT / "02_versions.png").exists()


def test_change_labels_follow_levels():  # AT10
    for c in tables.changes():
        a, b = c["level_from"], c["level_to"]
        assert c["change"] == ("added" if b > a else "removed" if b < a and b == 0 else "softened" if b < a else "unchanged")
