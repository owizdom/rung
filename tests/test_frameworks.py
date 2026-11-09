"""Spec 0001 AT1 to AT4 over the frozen document list."""
import csv
import hashlib
import re
from pathlib import Path

import yaml

from frameworks.census import SIGNATORIES, load_universe, current_set, WINDOW_END

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "frameworks" / "documents.csv"
LOG = ROOT / "frameworks" / "search_log.csv"


def test_twenty_signatories():
    assert len(SIGNATORIES) == 20 and len(set(SIGNATORIES)) == 20


def test_universe_schema():
    u = load_universe()
    ids = [d["doc_id"] for d in u]
    assert len(ids) == len(set(ids))
    for d in u:
        assert d["developer"] in SIGNATORIES, d["doc_id"]
        assert re.fullmatch(r"[a-z0-9]+-[a-z0-9]+-[a-z0-9.]+", d["doc_id"]), d["doc_id"]
        for k in ("line", "title", "version", "published", "published_source", "url"):
            assert str(d.get(k, "")).strip(), (d["doc_id"], k)
        assert str(d["published"]) <= WINDOW_END, d["doc_id"]


def test_current_set_is_latest_per_line():
    u = load_universe()
    cur = current_set(u)
    lines = {(d["developer"], d["line"]) for d in u}
    assert {(d["developer"], d["line"]) for d in cur} == lines
    for d in cur:
        same = [x for x in u if (x["developer"], x["line"]) == (d["developer"], d["line"])]
        assert str(d["published"]) == max(str(x["published"]) for x in same)


def _docs():
    return list(csv.DictReader(DOCS.open(encoding="utf-8")))


def test_every_universe_doc_captured():
    have = {r["doc_id"] for r in _docs()}
    want = {d["doc_id"] for d in load_universe()}
    assert want == have, (want - have, have - want)


def test_bytes_match_sha256():  # AT3
    for r in _docs():
        p = Path(r["cache_path"]).expanduser()
        assert p.exists(), r["doc_id"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == r["sha256"], r["doc_id"]
        t = Path(r["text_path"]).expanduser()
        assert t.exists() and int(r["words"]) > 500, r["doc_id"]


def test_dates_sourced():  # AT4
    for r in _docs():
        assert r["published"] and r["published_source"], r["doc_id"]


def test_every_signatory_accounted_for():  # AT2
    with_docs = {d["developer"] for d in load_universe()}
    log = list(csv.DictReader(LOG.open(encoding="utf-8")))
    for s in SIGNATORIES:
        if s in with_docs:
            continue
        wheres = {row["where"] for row in log if row["developer"] == s}
        assert {"company site", "metr list", "wayback", "web search"} <= wheres, (s, wheres)
