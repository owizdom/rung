"""Spec 0001 AT8 (ladder) and AT10 (change labels)."""
from analysis.ladder import RUNGS, level, gaps, union, change_label

FULL = dict(mentioned=1, threshold=1, response=1, acc_decider=1, acc_external=1, acc_unmet=1)


def r(**kw):
    d = {k: 0 for k in RUNGS}
    d.update(kw)
    return d


def test_rung_order():
    assert RUNGS == ["mentioned", "threshold", "response", "acc_decider", "acc_external", "acc_unmet"]


def test_levels_cumulative():
    assert level(r()) == 0
    assert level(r(mentioned=1)) == 1
    assert level(r(mentioned=1, threshold=1)) == 2
    assert level(r(mentioned=1, threshold=1, response=1)) == 3
    assert level(dict(FULL)) == 4


def test_level4_strict_needs_all_three_parts():
    for k in ("acc_decider", "acc_external", "acc_unmet"):
        assert level({**FULL, k: 0}) == 3


def test_level4_loose_sensitivity():
    assert level({**FULL, "acc_external": 0}, rule="loose") == 4
    assert level({**FULL, "acc_unmet": 0}, rule="loose") == 4
    assert level({**FULL, "acc_external": 0, "acc_unmet": 0}, rule="loose") == 3
    assert level({**FULL, "acc_decider": 0}, rule="loose") == 3


def test_ladder_stops_at_first_gap():
    assert level(r(mentioned=1, response=1, acc_decider=1, acc_external=1, acc_unmet=1)) == 1
    assert level(r(mentioned=1, threshold=1, acc_decider=1, acc_external=1, acc_unmet=1)) == 2


def test_gaps_reported():
    assert gaps(r(mentioned=1, response=1)) == ["response"]
    assert gaps(r(mentioned=1, threshold=1, acc_unmet=1)) == ["acc_unmet"]
    assert gaps(dict(FULL)) == []
    assert gaps(r(mentioned=1, threshold=1, response=1, acc_external=1)) == []  # partial accountability is not a gap


def test_union_takes_each_rung_from_any_document():
    a = r(mentioned=1, threshold=1, response=1)
    b = r(mentioned=1, acc_decider=1, acc_external=1, acc_unmet=1)
    u = union([a, b])
    assert u == FULL and level(u) == 4
    assert union([r(), r()]) == r()


def test_change_labels():
    assert change_label(2, 3) == "added"
    assert change_label(3, 1) == "softened"
    assert change_label(3, 0) == "removed"
    assert change_label(2, 2) == "unchanged"
    assert change_label(0, 0) == "unchanged"
