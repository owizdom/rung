"""The framework universe (spec 0001 section 1.1).

frameworks/universe.yaml lists every framework version in scope, written by hand from the
census (METR list, the census search, the Wayback history of each URL). This module loads it
and derives each developer's current set.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "frameworks" / "universe.yaml"
WINDOW_END = "2026-10-31"

# The 20 signatories of the Frontier AI Safety Commitments (gov.uk page, fetched 2026-11-09).
SIGNATORIES = {
    "amazon": "Amazon", "anthropic": "Anthropic", "cohere": "Cohere", "google": "Google DeepMind",
    "g42": "G42", "ibm": "IBM", "inflection": "Inflection AI", "meta": "Meta", "microsoft": "Microsoft",
    "mistral": "Mistral AI", "naver": "Naver", "openai": "OpenAI", "samsung": "Samsung Electronics",
    "tii": "Technology Innovation Institute", "xai": "xAI", "zhipu": "Zhipu AI", "magic": "Magic",
    "minimax": "MiniMax", "01ai": "01.AI", "nvidia": "NVIDIA",
}


def load_universe(path: Path = UNIVERSE) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    out = []
    for d in data["documents"]:
        d = {k: (str(v) if v is not None else "") for k, v in d.items()}
        out.append(d)
    return out


def current_set(docs: list[dict]) -> list[dict]:
    """Latest version of each (developer, line) published by WINDOW_END."""
    best: dict[tuple[str, str], dict] = {}
    for d in docs:
        if d["published"] > WINDOW_END:
            continue
        k = (d["developer"], d["line"])
        if k not in best or d["published"] > best[k]["published"]:
            best[k] = d
    return sorted(best.values(), key=lambda d: (d["developer"], d["line"]))
