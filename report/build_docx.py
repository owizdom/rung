"""Build the Challenge 3 write-up as a .docx for upload to Google Docs.

A plain-language version of docs/methods.md. Every number comes from analysis.facts at build time,
and the shared sentences are asserted against analysis.verify_claims.

Usage: python3 -m report.build_docx [OUT.docx]
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

from analysis.facts import facts
from analysis.verify_claims import check

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "report" / "out" / "Challenge 3 - safety frameworks.docx"
FONT = "Arial"
GREY = RGBColor(0x59, 0x59, 0x59)
TITLE_FILL = "F1C232"
REPO = "https://github.com/owizdom/rung"

# ---------- low-level helpers ----------

def set_font(run, size=11, bold=None, color=None, italic=None):
    run.font.name = FONT
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), FONT)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color is not None:
        run.font.color.rgb = color
    return run


def shade_run(run, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    run._element.get_or_add_rPr().append(shd)


def shade_cell(cell, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    cell._tc.get_or_add_tcPr().append(shd)


def para(doc, text="", lead=None, size=11, style=None, after=10, color=None, align=None):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.15
    if align is not None:
        p.alignment = align
    if lead:
        set_font(p.add_run(lead + " "), size, bold=True, color=color)
    add_inline(p, text, size, color)
    return p


def add_inline(p, text, size=11, color=None):
    """Plain text; `code` spans never reach here (asserted in build)."""
    if text:
        set_font(p.add_run(text), size, color=color)


def link(p, text, url, size=11):
    part = p.part
    rid = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    h = OxmlElement("w:hyperlink")
    h.set(qn("r:id"), rid)
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    for k in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        fonts.set(qn(k), FONT)
    rpr.append(fonts)
    col = OxmlElement("w:color")
    col.set(qn("w:val"), "1155CC")
    rpr.append(col)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rpr.append(u)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(size * 2))
    rpr.append(sz)
    r.append(rpr)
    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    r.append(t)
    h.append(r)
    p._p.append(h)


def heading(doc, text):
    h = doc.add_heading(level=1)
    set_font(h.add_run(text), 14, bold=True, color=RGBColor(0, 0, 0))
    pf = h.paragraph_format
    pf.space_before, pf.space_after, pf.keep_with_next = Pt(18), Pt(6), True
    return h


def picture(doc, path, alt):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    p.add_run().add_picture(str(path), width=Inches(5.5))
    docpr = p._p.xpath(".//wp:docPr")[0]
    docpr.set("descr", alt)
    docpr.set("title", Path(path).stem)


def table_widths(table, widths_dxa):
    table.autofit = False
    tblpr = table._tbl.tblPr
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblpr.append(lay)
    for i, w in enumerate(widths_dxa):
        table.columns[i].width = Inches(w / 1440)
    for row in table.rows:
        for i, c in enumerate(row.cells):
            c.width = Inches(widths_dxa[min(i, len(widths_dxa) - 1)] / 1440)


def cell_text(cell, text, size=8, bold=False, color=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    set_font(p.add_run(text), size, bold=bold, color=color)


def repeat_header(row):
    trpr = row._tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader")
    h.set(qn("w:val"), "true")
    trpr.append(h)


# ---------- content ----------

STEPS = [
    ("Not mentioned", "The framework does not name the risk."),
    ("Mentioned", "The framework names the risk as one the company considers, tests for or tracks."),
    ("Threshold", "It also defines a specific level for that risk, in terms of what a model could do, at which the company will act differently."),
    ("Response", "It also commits to what the company will do when the level is reached: named safeguards or security measures, or holding back release or development. \"May\", \"consider\", \"intend\" and \"as appropriate\" do not count, and nor does anything the framework calls illustrative."),
    ("Accountability", "It also names who decides, commits to review by someone outside the company (not just \"as needed\"), and says what happens if the response cannot be met. All three are needed."),
]
RISKS = [
    ("Cyber", "Helping carry out cyberattacks: finding or exploiting vulnerabilities, malware, attacks on infrastructure."),
    ("Bio and chem", "Helping make or use biological or chemical weapons, including CBRN named as one group."),
    ("AI R&D automation", "Automating or greatly speeding up AI research itself, including AI improving AI."),
    ("Autonomy", "The model acting on its own in the world: copying itself, gathering resources, long tasks without people."),
    ("Loss of control", "The model working against its developer's intent, or people losing the ability to correct or shut it down: misalignment, deception, sabotage, escaping oversight."),
]


def _and(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def short(name):
    return name.replace(" Electronics", "")


def doc_claims(F):
    """Sentences the docx must contain, built from the data (AT11 for the docx)."""
    return [
        f"Of {F['n_devs']} companies with a published framework, {F['n_threshold_any']} set a specific danger level",
        f"Only {F['n_acc_any']} ({_and(F['acc_devs'])}) {'goes' if F['n_acc_any'] == 1 else 'go'} all the way on any risk",
        f"only {F['n_acc_external']} commit to any binding review from outside the company",
        f"Cyber is named by {F['cyber_mention']} of the {F['n_devs']} frameworks, but only {F['cyber_threshold']} set a cyber danger level",
        f"in {F['gap_cells']} cases a framework commits to a response",
        f"{_and(F['missing_acc_external'])} make no binding commitment",
        f"{F['n_acc_any_loose']} companies would reach the top step instead of {F['n_acc_any']}",
        f"a risk went up a step {F['n_up']} times and down {F['n_down']} times",
        f"scored all {F['n_cells']:,} cells",
        f"settled the {F['n_adjudicated']} disagreements",
        f"{F['verify']['correct']} correct, {F['verify']['wrong']} wrong and {F['verify']['unsure']} unsure",
    ]


def build(out: Path) -> None:
    F = facts()
    methods = (ROOT / "docs" / "methods.md").read_text(encoding="utf-8")
    assert check(methods, F) == [], "methods.md claims do not match the data"
    k = F["kappa"]
    v = F["verify"]

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, side, Inches(1))
    for sname in ("Normal", "List Bullet", "List Number"):
        st = doc.styles[sname]
        st.font.name = FONT
        st.font.size = Pt(11)
        st.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), FONT)

    t = doc.add_paragraph()
    t.paragraph_format.space_after = Pt(6)
    shade_run(set_font(t.add_run("Challenge 3: What do frontier safety frameworks actually commit to?"), 20, bold=True), TITLE_FILL)
    para(doc, "Wisdom Okechukwu · 9 November 2026", size=10, color=GREY, after=12)

    para(doc, f"Less than they appear to. Of {F['n_devs']} companies with a published framework, {F['n_threshold_any']} set a specific danger level "
              f"for at least one of the five risks, and every one of those also says what it will do when that level is reached. "
              f"Only {F['n_acc_any']} ({_and(F['acc_devs'])}) {'goes' if F['n_acc_any'] == 1 else 'go'} all the way on any risk: naming who decides, committing to outside review, and saying "
              f"what happens if safeguards fall short. The missing piece is outside review. "
              f"{_and([short(x) for x in F['zero_devs']])} publish frameworks that name none of the five risks.", lead="Short answer.", after=8)

    para(doc, "Each framework is scored on five risks. For each risk it climbs a ladder, and a step counts only if every step below it is also met:", after=4)
    for name, txt in STEPS[1:]:
        para(doc, txt, lead=name + ".", style="List Bullet", after=2)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.add_run().add_picture(str(ROOT / "analysis" / "out" / "01_latest.png"), width=Inches(4.1))
    p.runs[0]._r.xpath(".//wp:docPr")[0].set("descr",
        f"Heatmap of {F['n_devs']} companies by 5 risks showing the highest step each current framework reaches. {_and(F['acc_devs'])} reach accountability on at least one risk; "
        f"{_and(F['zero_devs'])} name none of the five risks.")

    heading(doc, "What we found")
    para(doc, f"Cyber is named by {F['cyber_mention']} of the {F['n_devs']} frameworks, but only {F['cyber_threshold']} set a cyber danger level. "
              f"Bio and chem: named by {F['biochem_mention']}, a level from {F['biochem_threshold']}. AI R&D automation gets a level from {F['ai_rnd_threshold']}, "
              f"autonomy and loss of control from {F['autonomy_threshold']} each. {len(F['no_threshold_devs'])} frameworks never set a level for any risk: "
              f"{_and([short(x) for x in F['no_threshold_devs']])}. Magic's has a table headed \"Critical Capability Threshold\", then calls the rows \"illustrative\".",
         lead="1. Naming a risk is easy; setting a level is not.")
    para(doc, f"Every framework that sets a level also commits to a response. Some go the other way: in {F['gap_cells']} cases a framework commits to a response "
              "for a risk it never sets a level for. xAI's June 2026 framework says it \"will only proceed\" if risks are \"determined to be acceptable\", "
              "but defines no level for any risk, so the promise has nothing to measure against.", lead="2. Where there is a level, there is a response.")
    para(doc, f"Of the {F['n_with_resp']} frameworks with a level and a response, {F['n_acc_decider']} name who decides ({_and(F['missing_acc_decider'])} do not) and {F['n_acc_unmet']} say what happens "
              f"if the response fails, but only {F['n_acc_external']} commit to any binding review from outside the company. "
              f"{_and(F['missing_acc_external'])} make no binding commitment. Most mention outside experts, but on the company's terms: Google DeepMind involves them "
              "\"as needed\", Amazon runs external evaluations \"as appropriate\", and OpenAI's third-party audits sit in an appendix it calls \"illustrative\". "
              f"If a named decider plus one of the other two parts were enough, {F['n_acc_any_loose']} companies would reach the top step instead of {F['n_acc_any']}.",
         lead="3. Almost nobody commits to outside review.")
    para(doc, "Anthropic's Responsible Scaling Policy named cyber in every version up to 2.2. From version 3.0 (February 2026) it does not mention cyber at all. "
              "Anthropic still covers cyber in a second document written for California's SB 53 law, which is why its cyber cell shows a response.",
         lead="4. Anthropic's main policy dropped cyber.")

    heading(doc, "How the frameworks changed")
    para(doc, f"All {F['n_versions']} published versions were scored the same way. Between one version and the next, a risk went up a step {F['n_up']} times "
              f"and down {F['n_down']} times. The drops:", after=6)
    for txt in [
        "OpenAI (April 2025) turned its binding third-party audits into an illustrative appendix, and moved autonomy and loss of control out of its tracked risks into \"research categories\" with no danger levels.",
        "Google DeepMind removed autonomy in February 2025 and marked its misalignment levels \"illustrative only\" in September 2025.",
        "Anthropic removed cyber from its main policy in February 2026.",
        "Amazon (September 2026) changed outside evaluation from a commitment to \"as appropriate\".",
        "xAI (June 2026) removed its numeric limits for bio and chem and for model dishonesty, and stopped naming AI R&D.",
        "Naver (July 2026) replaced its named risks with three \"protected values\"; cyber, bio and chem, and loss of control are no longer named.",
    ]:
        para(doc, txt, style="List Bullet", after=4)
    para(doc, "Anthropic's February 2026 rewrite also dropped autonomy from full accountability to a threshold, because its only commitment there depends on Anthropic being ahead of competitors. "
              "Some steps went up too: Anthropic added a loss of control level in February 2026, Google DeepMind in April 2026, Meta in its April 2026 framework "
              "and Amazon in September 2026. Every change was checked with both versions side by side. Appendix A shows every version.", after=10)

    heading(doc, "How it was done")
    for lead, txt in [
        ("Which frameworks.", f"Every framework published by the 20 companies that signed the 2024 Seoul safety commitments, up to 31 October 2026: {F['n_versions']} versions from "
                              f"{F['n_devs']} companies. The other seven were searched and have none: Mistral, TII, MiniMax and 01.AI publish nothing; IBM, Inflection and Zhipu publish only general material."),
        ("Which version.", f"Every file was downloaded and fingerprinted, and archived copies were checked for files replaced in place. The list has {F['n_metr_missed']} versions METR's list does not, including OpenAI's original v2 file: the copy METR links is a quiet re-issue that dropped a safeguard but kept its original date."),
        ("Coding.", f"Two AI coders, Claude Opus 5.5 and Claude Sonnet 5.5, each read every page of every document separately and scored all {F['n_cells']:,} cells. "
                    f"Every \"yes\" had to quote the document word for word, checked by a script. Separate Claude instances settled the {F['n_adjudicated']} disagreements, "
                    "re-checked every change between versions with both versions open, and applied three rules added after a review to every document."),
        ("Agreement.", f"Before the disagreements were settled, the two coders agreed well on most steps (Cohen's kappa, where 1 is perfect: mentioned {k['mentioned']}, threshold {k['threshold']}, "
                       f"decider {k['acc_decider']}, outside review {k['acc_external']}, consequence {k['acc_unmet']}). They agreed less on the response step ({k['response']}), "
                       "so that step leans most on the later rulings."),
        ("Check.", f"Before the last rule changes, another Claude instance re-checked {sum(v.values())} codes, drawn at random 5 per step and per yes or no, against the documents: {v['correct']} correct, {v['wrong']} wrong and {v['unsure']} unsure."),
        ("Yardstick.", "What counts as a specified response follows the EU General-Purpose AI Code of Practice, Safety and Security chapter."),
    ]:
        para(doc, txt, lead=lead, style="List Bullet", after=6)

    heading(doc, "Limits")
    para(doc, "Gaps in the public record.", after=4).runs[0].bold = True
    for txt in [
        "One version could not be found: Anthropic's compliance framework v1.2 (June 2026) was replaced online and never archived.",
        "A few dates rest on archive captures and file data rather than a printed date: OpenAI's governance framework (May 2026), Microsoft's February 2026 update, and the quiet re-issues by OpenAI and Meta.",
    ]:
        para(doc, txt, style="List Bullet", after=4)
    para(doc, "Choices in this study.", after=4).runs[0].bold = True
    for txt in [
        "The brief asks for two people to code at least a quarter of the cells. Here two AI coders coded all of them and no human audited the codes. Two coders from one model family can share blind spots.",
        "The top step needs all three parts of accountability, and outside review must be a commitment, not \"as needed\". Both are strict readings; the looser result is given above.",
        "Where a company has two current documents (Anthropic and OpenAI), a step counts if either reaches it.",
        "Samsung is included because its \"AI Safety Framework\" is the document it published for the Seoul commitments, even though it covers only on-device AI.",
    ]:
        para(doc, txt, style="List Bullet", after=4)

    heading(doc, "Sources and data")
    p = para(doc, "", after=6)
    add_inline(p, "Framework documents from each company and the ")
    link(p, "Wayback Machine", "https://web.archive.org/")
    add_inline(p, "; ")
    link(p, "METR's list of frontier AI safety policies", "https://metr.org/fsp")
    add_inline(p, " and its ")
    link(p, "Common Elements", "https://metr.org/common-elements")
    add_inline(p, " report; the ")
    link(p, "Frontier AI Safety Commitments", "https://www.gov.uk/government/publications/frontier-ai-safety-commitments-ai-seoul-summit-2024/frontier-ai-safety-commitments-ai-seoul-summit-2024")
    add_inline(p, "; the ")
    link(p, "EU Code of Practice", "https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai")
    add_inline(p, " Safety and Security chapter.")
    p = para(doc, "", lead="Data and code.")
    add_inline(p, "Every document's fingerprint and source, both coders' files, every quote, the full method and the code behind each chart: ")
    link(p, REPO, REPO)
    add_inline(p, ".")

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    heading(doc, "Appendix A. Every version")
    para(doc, "Each row is one published version, scored on its own.")
    p = doc.add_paragraph()
    p.add_run().add_picture(str(ROOT / "analysis" / "out" / "02_versions.png"), height=Inches(8.3))
    p.runs[0]._r.xpath(".//wp:docPr")[0].set("descr", f"Heatmap of all {F['n_versions']} framework versions by 5 risks, grouped by company, oldest first.")

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    heading(doc, "Appendix B. Definitions")
    tc = doc.add_table(rows=1, cols=2)
    tc.style = "Table Grid"
    for c, h in zip(tc.rows[0].cells, ["Term", "Meaning"]):
        cell_text(c, h, size=9, bold=True)
        shade_cell(c, "D9D9D9")
    repeat_header(tc.rows[0])
    for group, rows in (("The five risks", RISKS), ("The steps", STEPS)):
        rc = tc.add_row().cells
        m = rc[0].merge(rc[1])
        cell_text(m, group, size=9, bold=True)
        shade_cell(m, "FFF2CC")
        for name, txt in rows:
            cells = tc.add_row().cells
            cell_text(cells[0], name, size=9)
            cell_text(cells[1], txt, size=9)
    table_widths(tc, [2400, 6960])

    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out)
    text = " ".join(p.text for p in Document(str(out)).paragraphs)
    missing = [c for c in doc_claims(F) if c not in text]
    assert not missing, f"docx text does not carry: {missing}"


def main(argv=None) -> int:
    out = Path(argv[0]) if argv else OUT
    build(out)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
