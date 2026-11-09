"""The coding ladder (spec 0001 section 1.3) and change labels (section 1.4)."""
from __future__ import annotations

RUNGS = ["mentioned", "threshold", "response", "acc_decider", "acc_external", "acc_unmet"]
ACC = ["acc_decider", "acc_external", "acc_unmet"]
LEVEL_NAMES = ["Not mentioned", "Mentioned", "Threshold defined", "Response specified", "Accountability named"]


def level(r: dict, rule: str = "strict") -> int:
    """Highest step reached with every step below it met. Strict level 4 needs all three
    accountability parts; the loose sensitivity rule needs a named decider plus one other part."""
    if not r["mentioned"]:
        return 0
    if not r["threshold"]:
        return 1
    if not r["response"]:
        return 2
    if rule == "strict":
        return 4 if all(r[k] for k in ACC) else 3
    if rule == "loose":
        return 4 if r["acc_decider"] and (r["acc_external"] or r["acc_unmet"]) else 3
    raise ValueError(rule)


def gaps(r: dict) -> list[str]:
    """Rungs coded 1 above a missing step (a response with no threshold, say).
    Accountability parts are judged against the response step, not against each other."""
    out = []
    if r["mentioned"]:
        if not r["threshold"] and r["response"]:
            out.append("response")
        if not (r["threshold"] and r["response"]):
            out += [k for k in ACC if r[k]]
    return out


def union(rows: list[dict]) -> dict:
    """A developer's current set: each rung from any of its documents."""
    return {k: int(any(x[k] for x in rows)) for k in RUNGS}


def change_label(a: int, b: int) -> str:
    if b > a:
        return "added"
    if b < a:
        return "removed" if b == 0 else "softened"
    return "unchanged"
