"""AT11: every data-derived number in docs/methods.md (and the docx text) matches the data.

Each claim is a phrase built from analysis.facts; the check fails if a phrase is missing from the text,
so a changed number in the data breaks the build until the prose is updated.
Usage: python3 -m analysis.verify_claims [FILE]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from analysis.facts import facts

ROOT = Path(__file__).resolve().parents[1]


def _and(xs: list[str]) -> str:
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def claims(f: dict) -> list[str]:
    k = f["kappa"]
    src = f["source"]
    return [
        f"Of {f['n_devs']} developers with a published framework, {f['n_threshold_any']} set a threshold for at least one of the five risks",
        f"Every one of those {f['n_response_any']} also commits to a response",
        f"Only {f['n_acc_any']} reach full accountability on any risk: {_and(f['acc_devs'])}",
        f"Of the {f['n_with_resp']} frameworks with a threshold and a response, {f['n_acc_decider']} name a decider and {f['n_acc_unmet']} state a consequence, but only {f['n_acc_external']} commit to review from outside the company",
        f"Cyber and bio and chem are covered best: {f['cyber_threshold']} developers set a threshold for each",
        f"AI R&D automation gets a threshold from {f['ai_rnd_threshold']}, autonomy and loss of control from {f['autonomy_threshold']} each",
        f"{_and(f['zero_devs'])} publish frameworks that name none of the five risks",
        f"Across {f['n_versions']} versions, a risk's step went up {f['n_up']} times and down {f['n_down']} times",
        f"Cyber is named by {f['cyber_mention']} of the {f['n_devs']} frameworks, but only {f['cyber_threshold']} define a cyber threshold",
        f"Bio and chem is named by {f['biochem_mention']} and gets a threshold from {f['biochem_threshold']}",
        f"Autonomy is named by {f['autonomy_mention']} and gets a threshold from {f['autonomy_threshold']}",
        f"{WORDS[len(f['no_threshold_devs'])]} frameworks never define a threshold for any of the five risks: {_and(f['no_threshold_devs'])}",
        f"All {f['n_threshold_any']} frameworks that define a threshold for a risk also commit",
        f"In {f['gap_cells']} developer-and-risk cells a framework commits to a response with no threshold for that risk, across {_and(f['gap_devs'])}",
        f"Among the {f['n_with_resp']} frameworks with a threshold and a response",
        f"{f['n_acc_decider']} name who decides. {_and(f['missing_acc_decider'])} does not",
        f"{f['n_acc_unmet']} say what happens if the response cannot be met. {_and(f['missing_acc_unmet'])} do not",
        f"{f['n_acc_external']} commit to review from outside the company. {_and(f['missing_acc_external'])} do not",
        f"{f['n_acc_any_loose']} developers reach the top step instead of {f['n_acc_any']}: {_and(f['loose_join'])} join",
        f"Of the {f['n_versions']} versions, {f['n_pairs']} pairs are consecutive versions",
        f"went up {f['n_up']} times and down {f['n_down']} times: {f['n_softened']} times softened",
        f"and {f['n_removed']} times removed",
        f"there are {f['n_versions']} versions in all",
        f"The list has {f['n_metr_missed']} versions that METR's list does not carry as entries",
        f"{f['n_current']} documents",
        f"coded every one of the {f['n_cells']:,} cells",
        f"ruled on the {f['n_adjudicated']} cells where they disagreed",
        f"mentioned {k['mentioned']}, threshold {k['threshold']}, response {k['response']}, named decider {k['acc_decider']}, outside review {k['acc_external']}, consequence {k['acc_unmet']}",
        f"Weighted kappa on the overall level is {f['kappa_level']}",
        f"ruling {f['n_xv_cells']} cells",
        f"Of the {f['n_cells']:,} final cells, {src['agreed']} are as both coders agreed, {src['adjudicated']} as the adjudicator ruled, {src['cross-version']} as the cross-version check ruled and {src['consistency']} as the consistency pass ruled",
        f"{sum(f['verify'].values())} final codes, sampled 5 per step and value, against the documents before the consistency pass: {f['verify']['correct']} correct, {f['verify']['wrong']} wrong and {f['verify']['unsure']} unsure",
    ]


WORDS = {i: w for i, w in enumerate("Zero One Two Three Four Five Six Seven Eight Nine Ten".split())}


def check(text: str, f: dict) -> list[str]:
    norm = lambda s: re.sub(r"\s+", " ", s)
    t = norm(text)
    return [c for c in claims(f) if norm(c) not in t]


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    path = Path(argv[0]) if argv else ROOT / "docs" / "methods.md"
    missing = check(path.read_text(encoding="utf-8"), facts())
    for m in missing:
        print("MISSING:", m)
    print(f"{len(claims(facts())) - len(missing)}/{len(claims(facts()))} claims hold")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
