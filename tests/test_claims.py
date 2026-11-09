"""AT11: claims in the methods note match the data."""
from pathlib import Path

from analysis.facts import facts
from analysis.verify_claims import check

ROOT = Path(__file__).resolve().parents[1]


def test_methods_claims_hold():
    assert check((ROOT / "docs" / "methods.md").read_text(encoding="utf-8"), facts()) == []


def test_checker_catches_a_wrong_number():
    text = (ROOT / "docs" / "methods.md").read_text(encoding="utf-8")
    assert check(text.replace("went up 15 times", "went up 16 times"), facts())


def test_readme_claims_hold():
    from analysis.verify_claims import _and
    f = facts()
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    for c in [f"of {f['n_devs']} developers with a published framework, {f['n_threshold_any']} set a threshold",
              f"Only {f['n_acc_any']} reach full accountability on any risk: {_and(f['acc_devs'])}",
              f"only {f['n_acc_external']} commit to review from outside the company",
              f"went up {f['n_up']} times and down {f['n_down']} times",
              f"ruled on the {f['n_adjudicated']} disagreements"]:
        assert c in text, c


def test_docx_claims_hold(tmp_path):  # AT11 for the docx
    from report.build_docx import build
    build(tmp_path / "x.docx")  # raises if any data-derived sentence is missing
