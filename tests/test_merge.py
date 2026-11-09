"""Merge of two passes plus adjudication into final codes."""
from analysis.ladder import RUNGS
from coding.check import RISKS
from coding.merge import merge_doc


def rec(vals=None, coder="A"):
    vals = vals or {}
    return {"doc_id": "d-x-1", "coder": coder, "other_risks": ["persuasion"] if coder == "A" else ["privacy"],
            "risks": {r: {g: {"value": vals.get((r, g), 0), "quote": f"q {r} {g}" if vals.get((r, g)) else "",
                              "page": "p.1", "note": "" if vals.get((r, g)) else "none here"} for g in RUNGS}
                      for r in RISKS}}


def test_agreement_passes_through():
    a = rec({("cyber", "mentioned"): 1})
    b = rec({("cyber", "mentioned"): 1}, "B")
    rows, dis = merge_doc(a, b, {})
    assert not dis
    row = [r for r in rows if r["risk"] == "cyber"][0]
    assert row["mentioned"] == 1 and row["level"] == 1 and row["other_risks"] == "persuasion; privacy"


def test_disagreement_needs_adjudication():
    a = rec({("cyber", "mentioned"): 1})
    b = rec({}, "B")
    rows, dis = merge_doc(a, b, {})
    assert [(d["risk"], d["rung"]) for d in dis] == [("cyber", "mentioned")]
    assert rows is None
    rows, dis = merge_doc(a, b, {("d-x-1", "cyber", "mentioned"): {"value": "0", "quote": "", "ruling": "background only"}})
    assert not dis and [r for r in rows if r["risk"] == "cyber"][0]["mentioned"] == 0


def test_cross_version_ruling_overrides():
    a = rec({("cyber", "mentioned"): 1})
    b = rec({("cyber", "mentioned"): 1}, "B")
    rows, _ = merge_doc(a, b, {}, {("d-x-1", "cyber", "mentioned"): {"value": "0", "quote": "", "page": ""}})
    assert [r for r in rows if r["risk"] == "cyber"][0]["mentioned"] == 0
