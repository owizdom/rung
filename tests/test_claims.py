"""AT11: claims in the methods note match the data."""
from pathlib import Path

from analysis.facts import facts
from analysis.verify_claims import check

ROOT = Path(__file__).resolve().parents[1]


def test_methods_claims_hold():
    assert check((ROOT / "docs" / "methods.md").read_text(encoding="utf-8"), facts()) == []


def test_checker_catches_a_wrong_number():
    text = (ROOT / "docs" / "methods.md").read_text(encoding="utf-8")
    assert check(text.replace("went up 14 times", "went up 15 times"), facts())
