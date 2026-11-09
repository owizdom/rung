"""Charts in Free Systems house style (spec 0001 AT9, AT10). One command rebuilds them from coding/codes.csv.

Usage: python3 -m analysis.plot
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis" / "fs_kit" / "scripts"))
from fs_charts import GRAY, INK, MONO, PAPER, RED, RULE, Page  # noqa: E402

from analysis import tables  # noqa: E402
from analysis.ladder import LEVEL_NAMES  # noqa: E402
from coding.check import RISKS  # noqa: E402

OUT = ROOT / "analysis" / "out"
CELL_WORD = ["Not mentioned", "Mentioned", "Threshold", "Response", "Accountability"]
ALPHA = [0, 0.16, 0.42, 0.7, 1.0]


def cell(p, x, y, w, h, lv, small=False):
    import matplotlib.pyplot as plt

    p.rect(x + 2, y + 2, w - 4, h - 4, RULE)
    if lv > 0:
        p.ax.add_patch(plt.Rectangle((x + 2, p._y(y + 2)), w - 4, h - 4, color=RED, alpha=ALPHA[lv], lw=0, zorder=3.5))
    col = PAPER if lv >= 3 else (GRAY if lv == 0 else INK)
    p.text(x + w / 2, y + h / 2 - (8 if small else 10), CELL_WORD[lv], 13 if small else 16, col, anchor="middle")


def legend(p, x, y):
    w = 236
    for lv in range(5):
        cell(p, x + lv * w, y, w - 8, 40)
    p.text(x, y - 14, "Each step needs the steps before it. Accountability means a named decider, outside review and a stated consequence if the response fails.", 15, GRAY)


def latest(title: str, rows: list[dict], notes: list[str]):
    devs = sorted({r["developer"] for r in rows}, key=lambda d: (-sum(r["level"] for r in rows if r["developer"] == d), d))
    names = {r["developer"]: r["name"] for r in rows}
    n = len(devs)
    x0, y0, lw, cw, rh = 64, 330, 330, 236, 52
    p = Page(title, "How far each developer's current frontier safety framework goes on each risk, as of 31 October 2026",
             height=y0 + n * rh + 260)
    legend(p, x0 + lw - 330 + 330, 196)
    for j, risk in enumerate(RISKS):
        p.text(x0 + lw + j * cw + cw / 2, y0 - 22, tables.RISK_LABEL[risk], 19, INK, anchor="middle", weight=600)
    for i, d in enumerate(devs):
        y = y0 + i * rh
        p.text(x0 + lw - 18, y + rh / 2 - 12, names[d], 21, INK, anchor="end")
        for j, risk in enumerate(RISKS):
            lv = next(r["level"] for r in rows if r["developer"] == d and r["risk"] == risk)
            cell(p, x0 + lw + j * cw, y, cw, rh, lv)
    p.notes(notes)
    p.save(str(OUT / "01_latest"))


def write_csv(name: str, rows: list[dict]):
    OUT.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    rows = tables.latest()
    write_csv("latest.csv", rows)
    devs = {r["developer"] for r in rows}
    title = f"What {len(devs)} frontier safety frameworks commit to, risk by risk"
    latest(title, rows, [
        "Each cell is the highest step the developer's current framework reaches for that risk. Anthropic and OpenAI each have two current documents; a step counts if either reaches it.",
        "Coded from the framework text, tables and figures by two independent passes, disagreements adjudicated. Hedged verbs (may, consider, intend) do not count as a commitment.",
        "Source: published frontier safety frameworks of the Frontier AI Safety Commitments signatories, archived copies (Wayback Machine); METR framework list.",
    ])
    write_csv("versions.csv", tables.versions())
    write_csv("changes.csv", tables.changes())
    return 0


if __name__ == "__main__":
    sys.exit(main())
