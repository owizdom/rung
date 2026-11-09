"""Spec 0001 AT5, AT6, AT7 helpers."""
import pytest

from coding.check import (RISKS, quote_found, validate, kappa, weighted_kappa, zero_screen_text,
                          shared_notes)
from analysis.ladder import RUNGS


def rec(over=None):
    risks = {k: {g: {"value": 0, "quote": "", "page": "", "note": "not in text"} for g in RUNGS} for k in RISKS}
    for (risk, rung), v in (over or {}).items():
        risks[risk][rung] = v
    return {"doc_id": "x-y-1", "coder": "A", "codebook": "v1", "coded_at": "2026-11-10T00:00:00Z",
            "risks": risks, "other_risks": []}


def test_risks():
    assert RISKS == ["cyber", "biochem", "ai_rnd", "autonomy", "loss_of_control"]


def test_quote_found_normalises():
    text = "We will  not deploy\nthe model until ASL-3 safe-\nguards are in place."
    assert quote_found("we will not deploy the model until ASL-3 safeguards are in place", text)
    assert quote_found("We will not deploy the model", "We will not deploy the model.")
    assert quote_found("the model’s weights", "the model's weights")
    assert not quote_found("we may pause", text)
    assert not quote_found("", text)


def test_valid_record_passes():
    assert validate(rec()) == []


def test_one_without_quote_fails():
    probs = validate(rec({("cyber", "mentioned"): {"value": 1, "quote": "", "page": "2", "note": ""}}))
    assert any("without a quote" in p for p in probs)


def test_zero_without_note_fails():
    probs = validate(rec({("cyber", "mentioned"): {"value": 0, "quote": "", "page": "", "note": ""}}))
    assert any("without a note" in p for p in probs)


def test_bad_value_and_missing_rung():
    bad = rec({("ai_rnd", "threshold"): {"value": 2, "quote": "x" * 20, "page": "1", "note": ""}})
    assert any("not in [0, 1]" in p for p in validate(bad))
    miss = rec()
    del miss["risks"]["autonomy"]["acc_unmet"]
    assert any("missing autonomy.acc_unmet" in p for p in validate(miss))


Q = {"value": 1, "quote": "a quote of reasonable length here", "page": "3", "note": ""}


def test_threshold_without_mention_is_inconsistent():
    probs = validate(rec({("cyber", "threshold"): Q}))
    assert any("threshold=1 but mentioned=0" in p for p in probs)


def test_accountability_needs_threshold_or_response():
    probs = validate(rec({("cyber", "mentioned"): Q, ("cyber", "acc_decider"): Q}))
    assert any("accountability without threshold or response" in p for p in probs)
    ok = rec({("cyber", "mentioned"): Q, ("cyber", "response"): Q, ("cyber", "acc_decider"): Q})
    assert not any("accountability" in p for p in validate(ok))


def test_kappa_values():
    assert kappa([1, 1, 0, 0], [1, 1, 0, 0]) == 1.0
    assert kappa([1, 0, 1, 0], [0, 1, 0, 1]) == pytest.approx(-1.0)
    # po = 0.8, pe = 0.5 -> 0.6
    a = [1] * 5 + [0] * 5
    b = [1, 1, 1, 1, 0, 0, 0, 0, 1, 0]
    assert kappa(a, b) == pytest.approx(0.6)


def test_weighted_kappa():
    assert weighted_kappa([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]) == pytest.approx(1.0)
    near = weighted_kappa([0, 1, 2, 3, 4, 4], [0, 1, 2, 3, 3, 4])
    far = weighted_kappa([0, 1, 2, 3, 4, 4], [0, 1, 2, 3, 0, 4])
    assert 0 < far < near < 1


def test_zero_screen_text():
    hits = zero_screen_text("Models could provide uplift to cyberattacks and misaligned behaviour.")
    assert hits["cyber"] and hits["loss_of_control"] and not hits["biochem"]
    assert zero_screen_text("CBRN weapons")["biochem"]
    assert zero_screen_text("automate AI research and development")["ai_rnd"]
    assert zero_screen_text("autonomous replication")["autonomy"]


def test_shared_notes_flags_copying():
    a, b = rec(), rec()
    for k in ("cyber", "biochem", "ai_rnd"):
        a["risks"][k]["threshold"]["note"] = f"no {k} threshold; only general risk language on p.4"
        b["risks"][k]["threshold"]["note"] = f"no {k} threshold; only general risk language on p.4"
    assert shared_notes(a, b) >= 3
    assert shared_notes(rec(), rec()) == 0  # boilerplate default notes are ignored


def test_bidi_marks_ignored():
    assert quote_found("we will pause training", "\u202dwe will\u202c \u202dpause training\u202c")
