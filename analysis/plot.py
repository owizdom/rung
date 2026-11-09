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
WORD = {i: w for i, w in enumerate("Zero One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve Thirteen".split())}
SHORT = {'anthropic-rsp-1.0': 'RSP v1.0 · Sep 2023', 'anthropic-rsp-2.0': 'RSP v2.0 · Oct 2024', 'anthropic-rsp-2.1': 'RSP v2.1 · Mar 2025', 'anthropic-rsp-2.2': 'RSP v2.2 · May 2025', 'anthropic-rsp-3.0': 'RSP v3.0 · Feb 2026', 'anthropic-rsp-3.1': 'RSP v3.1 · Apr 2026', 'anthropic-rsp-3.2': 'RSP v3.2 · Apr 2026', 'anthropic-rsp-3.3': 'RSP v3.3 · May 2026', 'anthropic-rsp-3.4': 'RSP v3.4 · Jul 2026', 'anthropic-fcf-1.0': 'Compliance Framework v1 · Dec 2025', 'anthropic-fcf-1.1': 'Compliance Framework v1.1 · Mar 2026', 'anthropic-fcf-2.0': 'Compliance Framework v2 · Jul 2026', 'openai-pf-beta': 'Preparedness beta · Dec 2023', 'openai-pf-2.0': 'Preparedness v2 · Apr 2025', 'openai-pf-2.0r': 'Preparedness v2 re-issue · Apr 2025', 'openai-fgf-2026.05': 'Governance Framework · May 2026', 'google-fsf-1.0': 'FSF v1.0 · May 2024', 'google-fsf-2.0': 'FSF v2.0 · Feb 2025', 'google-fsf-3.0': 'FSF v3.0 · Sep 2025', 'google-fsf-3.1': 'FSF v3.1 · Apr 2026', 'meta-scaling-2025.02': 'Frontier AI Framework · Feb 2025', 'meta-scaling-2025.03': 'Frontier AI Framework · Mar 2025', 'meta-scaling-2.0': 'Advanced AI Scaling v2.0 · Apr 2026', 'meta-scaling-2.1': 'Superintelligence Scaling v2.1 · Oct 2026', 'microsoft-fgf-2025.02': 'Governance Framework · Feb 2025', 'microsoft-fgf-2026.02': 'Governance Framework · Feb 2026', 'amazon-fmsf-2025.02': 'Model Safety Framework · Feb 2025', 'amazon-fmsf-2026.09': 'Model Safety Framework · Sep 2026', 'xai-framework-draft': 'Risk Mgmt draft · Feb 2025', 'xai-framework-2025.08': 'Risk Mgmt Framework · Aug 2025', 'xai-framework-2025.12': 'Frontier AI Framework · Dec 2025', 'xai-framework-2026.06': 'Frontier AI Framework · Jun 2026', 'nvidia-fara-2025.02': 'Frontier AI Risk Assessment · Feb 2025', 'magic-agi-1.0': 'AGI Readiness v1.0 · Jul 2024', 'magic-agi-1.0r': 'AGI Readiness, "outdated" note · Sep 2026', 'naver-asf-1.0': 'AI Safety Framework v1.0 · Jun 2024', 'naver-asf-2.0': 'AI Safety Framework v2.0 · Jul 2026', 'g42-fsf-2025.02': 'Frontier AI Safety Framework · Feb 2025', 'cohere-fmf-2025.02': 'Frontier Model Framework · Feb 2025', 'samsung-asf-2025.02': 'AI Safety Framework · Feb 2025'}
CELL_WORD = ["Not mentioned", "Mentioned", "Threshold", "Response", "Accountability"]
ALPHA = [0, 0.16, 0.42, 0.7, 1.0]


def cell(p, x, y, w, h, lv, small=False):
    import matplotlib.pyplot as plt

    p.rect(x + 2, y + 2, w - 4, h - 4, RULE)
    if lv > 0:
        p.ax.add_patch(plt.Rectangle((x + 2, p._y(y + 2)), w - 4, h - 4, color=RED, alpha=ALPHA[lv], lw=0, zorder=3.5))
    col = PAPER if lv >= 3 else (GRAY if lv == 0 else INK)
    p.text(x + w / 2, y + h / 2 - (8 if small else 10), CELL_WORD[lv], 13 if small else 16, col, anchor="middle")


def legend(p, x, y, w=234):
    for lv in range(5):
        cell(p, x + lv * w, y, w - 8, 40, lv)
    p.text(x, y - 14, "Each step needs the steps before it. Accountability means a named decider, outside review and a stated consequence if the response fails.", 15, GRAY)


def latest(title: str, rows: list[dict], notes: list[str]):
    devs = sorted({r["developer"] for r in rows}, key=lambda d: (-sum(r["level"] for r in rows if r["developer"] == d), d))
    names = {r["developer"]: r["name"] for r in rows}
    n = len(devs)
    x0, y0, lw, cw, rh = 64, 380, 300, 234, 52
    p = Page(title, "How far each developer's current frontier safety framework goes on each risk, as of 31 October 2026",
             height=y0 + n * rh + 200)
    legend(p, x0 + lw, 250)
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


def version_label(d: dict) -> str:
    return f"{d['title_short']}  {d['published'][:7]}"


def versions(title: str, rows: list[dict], docs: dict, notes: list[str]):
    from frameworks.census import SIGNATORIES

    order = []
    for r in rows:
        if r["doc_id"] not in order:
            order.append(r["doc_id"])
    devs = []
    for did in order:
        if docs[did]["developer"] not in devs:
            devs.append(docs[did]["developer"])
    x0, lw, cw, rh, gap = 64, 400, 210, 34, 22
    y0 = 360
    n_gap = len(devs) - 1
    p = Page(title, "Every published version of each framework, coded the same way. Lines are listed oldest first.",
             height=y0 + len(order) * rh + n_gap * gap + 230)
    legend(p, x0 + lw, 250, cw)
    for j, risk in enumerate(RISKS):
        p.text(x0 + lw + j * cw + cw / 2, y0 - 20, tables.RISK_LABEL[risk], 17, INK, anchor="middle", weight=600)
    y = y0
    prev = None
    for did in order:
        d = docs[did]
        if prev and d["developer"] != prev:
            y += gap
        if d["developer"] != prev:
            p.text(x0, y + rh / 2 - 10, SIGNATORIES[d["developer"]].replace(" Electronics", ""), 17, INK, weight=600)
        prev = d["developer"]
        p.text(x0 + lw - 14, y + rh / 2 - 10, SHORT.get(did, did), 15, GRAY, anchor="end")
        for j, risk in enumerate(RISKS):
            lv = next(r["level"] for r in rows if r["doc_id"] == did and r["risk"] == risk)
            cell(p, x0 + lw + j * cw, y, cw, rh, lv, small=True)
        y += rh
    p.notes(notes)
    p.save(str(OUT / "02_versions"))


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
    top = {d: max(r["level"] for r in rows if r["developer"] == d) for d in devs}
    n_thr = sum(v >= 2 for v in top.values())
    n_acc = sum(v == 4 for v in top.values())
    title = (f"{WORD[n_thr]} of {len(devs)} safety frameworks set risk thresholds. {WORD[n_acc]} {'says' if n_acc == 1 else 'say'} who\n"
             f"decides, who checks from outside and what happens if safeguards fail")
    latest(title, rows, [
        "Each cell is the highest step the developer's current framework reaches for that risk. Anthropic and OpenAI each have two current documents; a step counts if either reaches it.",
        "Coded from the framework text, tables and figures by two independent passes, disagreements adjudicated. Hedged verbs (may, consider, as needed) and illustrative text do not count.",
        "Source: published frontier safety frameworks of the Frontier AI Safety Commitments signatories, archived copies (Wayback Machine); METR framework list.",
    ])
    vrows = tables.versions()
    write_csv("versions.csv", vrows)
    write_csv("changes.csv", tables.changes())
    if len({r["doc_id"] for r in vrows}) > len({r["docs"] for r in rows}) + 5:
        docs = tables.documents()
        ch = tables.changes()
        moved = [c for c in ch if c["change"] != "unchanged"]
        vtitle = (f"Across {len(vrows) // 5} versions, risk commitments went up a step {sum(c['change'] == 'added' for c in moved)} times\n"
                  f"and down {sum(c['change'] in ('softened', 'removed') for c in moved)} times")
        versions(vtitle, vrows, docs, [
            "Each row is one published version, coded on its own. A step counts only when the version itself states it; hedged verbs do not count.",
            "Every change between consecutive versions was re-read with both versions side by side, and the same wording gets the same code in every version.",
            "Source: published frontier safety frameworks and their archived earlier versions (Wayback Machine); METR framework list.",
        ])
    return 0


if __name__ == "__main__":
    sys.exit(main())
