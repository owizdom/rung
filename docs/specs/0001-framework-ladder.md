# Spec 0001: what frontier safety frameworks commit to, risk by risk

- Status: APPROVED 2026-11-09 (level 4 needs all three accountability parts; two Claude passes on every cell; latest versions first, then every earlier version; local commits on owizdom/rung-v1)
- Owner: architect (Opus 5.5)
- Brief: Challenge 3, "What do frontier safety frameworks actually commit to?"
- Builds on: Challenge 4 (owizdom/tide): same pipeline of pinned bytes, two quote-gated coding passes, claim checker and docx write-up

## 1. Objective

For every published frontier safety framework, record how far each one goes on five risks. The risks are cyber, bio/chem, AI R&D automation, autonomy and loss of control. The scale is the brief's coding ladder: not mentioned, mentioned, threshold defined, response specified, accountability named. The same rules apply to every developer and every risk.

Done means all of the following exist and pass section 5:

1. `frameworks/documents.csv`: every framework version in scope, with source URL, archive copy, publication date, sha256 and extracted text. Frozen and hashed before any coding pass starts.
2. `coding/codebook.md`: the codebook, frozen after a pilot and before the main passes.
3. `coding/codes.csv`: one row per document and risk, with each rung coded 0 or 1, a verbatim quote behind every 1 and a note behind every 0.
4. `analysis/out/01_latest.png`: a developer by risk heatmap of ladder levels for the latest versions, covering at least 8 frameworks (minimum output).
5. Stretch: `analysis/out/02_versions.png` and `analysis/out/changes.csv`, the same grid for every earlier version, with each change between consecutive versions labelled added, softened or removed.
6. `docs/methods.md` and a docx write-up in the brief's style. Every number in both is checked against the data by a script.

### 1.1 Which documents count (decided before coding, never changed after)

- Developers: the 20 signatories of the Frontier AI Safety Commitments (gov.uk list, fetched 2026-11-09). The original 16 are Amazon, Anthropic, Cohere, Google, G42, IBM, Inflection AI, Meta, Microsoft, Mistral AI, Naver, OpenAI, Samsung Electronics, Technology Innovation Institute, xAI and Zhipu.ai. Magic, Minimax, 01.ai and NVIDIA joined later. Google's framework is Google DeepMind's.
- A framework is a document the developer published to say how it will identify, assess and manage severe risks from its frontier models. That covers the Seoul "safety framework", an SB 53 "frontier AI framework" and any renamed successor. Blog posts announcing a framework, model or system cards, usage policies and general responsible-AI standards are not frameworks.
- Window: published on or before 2026-10-31.
- Versions: each published version is its own document. A rename starts no new line: Meta's Frontier AI Framework, Advanced AI Scaling Framework and Superintelligence Scaling Framework form one line, and xAI's Risk Management Framework and Frontier AI Framework form another. Following the brief, a renamed document still counts as a new version. Two files with identical extracted text count once.
- Lines: a developer can run two framework lines at once. Anthropic has the Responsible Scaling Policy and the Frontier Compliance Framework. OpenAI has the Preparedness Framework and the Frontier Governance Framework.
- Current set: the latest version of each line on 2026-10-31. A developer's cell in the minimum heatmap takes each rung from any document in its current set (section 1.3). Each document is also coded and reported on its own.
- Signatories with no framework: a logged search (company site, METR list, Wayback CDX, web search) records the result. "No framework found" is a finding, not a gap.

The METR list (metr.org/fsp, fetched 2026-11-09) links 34 versions from 12 developers, and the current set has 14 documents. A probe on 2026-11-09 downloaded 28 of them as PDFs, between 2,410 and 15,020 words each. Anthropic RSP v2.0, Meta's Advanced AI Scaling Framework v2.0 and Amazon's 2025 framework need archived copies. Anthropic's Frontier Compliance Framework sits on a trust portal.

### 1.2 The five risks

| Risk | Counts | Boundary |
|---|---|---|
| `cyber` | offensive cyber capability: attacks, vulnerability discovery, exploit development, cyber operations | cyber defence of the developer's own systems is security, not this risk |
| `biochem` | biological or chemical weapons, including CBRN named as one category | radiological or nuclear alone does not count |
| `ai_rnd` | automating or sharply accelerating AI research and development: ML R&D, AI self-improvement, recursive improvement | |
| `autonomy` | the model acting on its own in the world: autonomous replication and adaptation, resource acquisition, long-range autonomous tasks | a passage about both autonomy and loss of control is coded for both |
| `loss_of_control` | the model acting against its developer's or user's intent, or humans losing the ability to direct, correct or shut it down: misalignment, deceptive alignment, scheming, sandbagging, undermining oversight or safeguards, self-exfiltration | |

The brief lists "autonomy and loss of control" without a comma, so the two are coded apart and can be merged later without recoding. Other risks a framework names (harmful manipulation, persuasion, nuclear and radiological, and so on) go into a free-text field and are not scored.

### 1.3 The ladder

Each document and risk gets four rungs, coded 0 or 1. Accountability splits into three parts, as the brief lists them.

| Rung | 1 when the document | EU Code benchmark |
|---|---|---|
| `mentioned` | names the risk as one the developer considers, assesses, monitors or researches, in its own voice | Measure 2.1, Appendix 1.4 |
| `threshold` | defines for this risk at least one specific capability or risk level at which what the developer does changes (a threshold, tier, CCL, "High" level). A generic "severe risk" with no risk-specific level does not count | Measure 4.1: tiers defined in terms of model capabilities |
| `response` | commits to what it will do when that threshold is reached or forecast: named safeguards or security measures, or not deploying, restricting deployment or pausing development until the risk is mitigated | Measure 1.1 (2)(b) and Measure 4.2 |
| `acc_decider` | names the role or body that decides whether the threshold is reached or the response is adequate (a Responsible Scaling Officer, Safety Advisory Group, CEO, board committee). "Leadership", "the company" or an unnamed governance body does not count | Commitment 8 |
| `acc_external` | commits to review from outside the company of the model, the threshold call, the safeguards or the developer's adherence: third-party evaluation or audit, external expert review, government testing. Notification alone does not count | Measure 1.1 (2)(d), Appendix 3.5 |
| `acc_unmet` | says what happens if the response cannot be met or is not followed: a pause or restriction until it is, or a stated non-compliance procedure | Measure 4.2 |

Binding language. A rung needs a commitment in the developer's own voice: will, shall, must, commit, will not, or "would" in an if-then about its own action. Hedged verbs (may, might, could, consider, aim, seek, strive, explore, intend, plan) and qualifiers on the action itself ("as appropriate", "where feasible") do not count for `response` or any accountability rung. This is the brief's pitfall about vague verbs, written as a rule.

Level for the heatmap is the highest step reached with every step below it also met:

- 0: not mentioned
- 1: mentioned
- 2: plus threshold
- 3: plus response
- 4: plus accountability, meaning all three accountability parts (Wisdom, 2026-11-09)

Gaps in the ladder, such as a response with no threshold, are counted and reported. The sensitivity version of level 4 needs a named decider plus one of the other two parts, and it is computed from the same codes.

A framework-wide passage, for example who decides for every threshold, applies to each risk whose threshold it governs. Coders cite it once per risk.

### 1.4 Changes between versions (stretch)

For each pair of consecutive versions in one line and each risk:

- added: the level rose
- softened: the level fell but the risk is still mentioned
- removed: the level fell to 0
- unchanged: the level stayed the same

Rung-level changes are listed too, with both quotes side by side, so a reader can see the exact wording that moved. Risks outside the five, such as OpenAI's persuasion category, are tracked through the free-text field.

### 1.5 Coding

- Pilot: both coders code 3 documents of different styles. The codebook is fixed from what the pilot shows, then frozen and hashed.
- Main passes: two independent passes over every document and risk, which is 100% of cells; the brief asks for at least 25%. Pass A runs on Opus 5.5 and pass B on Sonnet 5.5. Each coder reads the whole document, PDF pages included, so tables and figures are seen, and never sees the other pass. Each coder has its own scratch folder. An independence test flags identical quote sets.
- Disagreements: a fresh Opus adjudicator rules on every one, with both quotes and the page in front of it.
- Check: an independent instance verifies a stratified sample of 60 final codes against the source pages.

## 2. Non-goals

- Whether a threshold is set at the right level, or whether a safeguard would work.
- Whether a developer followed its framework. This study reads what the documents commit to.
- Legal compliance with SB 53 or the EU AI Act. The EU Code is a yardstick for "specified", nothing more.
- A composite score or ranking of developers.
- Scoring risks beyond the five. They are listed, not scored.
- Model cards, safety cases and transparency reports.

## 3. Stack

New local repository `~/Desktop/code/rung` with flat domain folders. Document bytes live in a gitignored cache, `~/.rung-cache/`. Only manifests, hashes and extracted text paths are committed.

```
frameworks/  universe.yaml, census.py, fetch.py, documents.csv, search_log.csv
coding/      codebook.md, check.py, passes/A, passes/B, adjudication.csv, codes.csv
analysis/    ladder.py, plot.py, changes.py, verify_claims.py, out/
report/      build_docx.py
docs/        specs/, TASKS.md, JOURNAL.md, methods.md
tests/
```

Reused from tide: quote normalisation, the verbatim check and Cohen's kappa from `coding/check.py`, and the Wayback CDX and raw-capture helpers from `cards/fetch.py`. Pinned reference: EU Code of Practice, Safety and Security chapter, sha256 `d879f9b5…fa2f4a`.

## 4. Seam contract

```
frameworks/documents.csv  doc_id, developer, line, title, version, published, source_url, archive_url, capture_ts, sha256, pages, words, text_path, current
frameworks/search_log.csv developer, where, query, date, result
coding/codes.csv          doc_id, risk, mentioned, threshold, response, acc_decider, acc_external, acc_unmet, level, other_risks
coding/quotes.csv         doc_id, risk, rung, value, quote, page, note, pass
analysis/out/changes.csv  line, from_doc, to_doc, risk, level_from, level_to, change
```

`doc_id` is `<developer>-<line>-<version>` and never changes once the list is frozen.

## 5. Acceptance tests

T means an automated test. L means a live run with a recorded artifact.

| # | Test | Type | Passes when |
|---|---|---|---|
| AT1 | Document list frozen first | T | the JOURNAL freeze entry and the hash of `documents.csv` predate every coding pass file |
| AT2 | Every signatory accounted for | T | each of the 20 has at least one document or a search log covering its site, the METR list, Wayback and web search |
| AT3 | Bytes match | T | re-hashing every cached file reproduces `sha256` |
| AT4 | Dates are sourced | T | every `published` date comes from the document itself, the METR list or an announcement, and the source is recorded |
| AT5 | No invented evidence | T | every rung coded 1 has a quote found verbatim (whitespace-normalised) in that document's text, or is marked as read from a page image and confirmed by the adjudicator |
| AT6 | Zeros are checked | T | a 0 on `mentioned` where the risk's keywords occur in the text carries a note |
| AT7 | Agreement reported | L | kappa per rung and weighted kappa on level, over 100% of cells. A rung below 0.7 is reported as unreliable, not hidden |
| AT8 | Ladder is right | T | unit tests on level derivation, gaps, the sensitivity rule and the union over a current set |
| AT9 | Minimum output | T | one command rebuilds `01_latest.png` from `codes.csv`, with at least 8 frameworks |
| AT10 | Stretch output | T | `changes.csv` and `02_versions.png` rebuild from the codes, and each change label follows section 1.4 |
| AT11 | Claims match data | T | `verify_claims.py` asserts every number in `methods.md` and the docx |
| AT12 | Tripwire | T | the suite fails on 0 tests run or any skip |

## 6. Tracks

| Track | Owns | Depends on | AT |
|---|---|---|---|
| A census | `frameworks/universe.yaml`, `census.py`, `search_log.csv` | approval | AT2, AT4 |
| B capture | `frameworks/fetch.py`, `documents.csv` | A | AT1, AT3 |
| C coding | `coding/` | B frozen; pilot first | AT5, AT6, AT7 |
| D analysis and write-up | `analysis/`, `report/`, `docs/methods.md` | C | AT8 to AT11 |

The current set (14 documents) runs through C and D first, so the minimum output exists early. The 20 or so earlier versions follow as the stretch.

## 7. Pre-mortem: "it shipped and nobody trusted it; why?"

| # | Failure | Mitigation in this spec |
|---|---|---|
| 1 | Readers think a lab scored high because it writes long documents | the ladder asks for specific content, never length. A long hedged document scores low |
| 2 | "Response specified" is a matter of taste | binding-language rule with a verb list, EU Code yardstick, quotes behind every 1, agreement reported per rung |
| 3 | The wrong version was coded (a live page edited after the date we claim) | archived bytes with sha256, a publication date from a stated source, and Wayback raw captures for old versions |
| 4 | A framework was missed, so a lab looks absent | all 20 signatories searched and logged (AT2), and METR's list cross-checked |
| 5 | Coding was only Claude, and Claude checked Claude | two passes on different models, an independence test, a fresh adjudicator, and a sample check. The brief asks for two people; the write-up says plainly that both coders are models |
| 6 | Framework-wide governance makes every risk look accountable | accountability is coded per risk, and only where the framework ties its governance to that risk's threshold |
| 7 | A table or figure holds the threshold and the text layer misses it | coders read PDF pages, not only extracted text (the Challenge 4 lesson) |
| 8 | Merging two lines (RSP plus FCF) inflates a developer | both documents are reported on their own beside the merged cell |
| 9 | Usage limits stop the passes midway (it happened in Challenge 4) | waves of at most 3 coders, one document per agent for long ones, progress kept in files |

## 8. Rollout, rollback, removal

- Rollout: local repository, small commits on `owizdom/rung-v1` after Wisdom's go. No push or publication without his explicit OK. The Free Systems chart kit stays local and gitignored, as in tide.
- Rollback: every output regenerates from the pinned bytes and the codes. Deleting `analysis/out/` and `coding/codes.csv` returns to the frozen list.
- Removal: none planned.

## Approval questions

1. Level 4: all three accountability parts (proposed), or a named decider plus one other part.
2. Coders: two Claude passes on every cell as in Challenge 4, or the same plus Wisdom hand-coding 25% of cells as the brief literally asks.
3. Scope: latest versions first and then every earlier version (proposed), or latest versions only.
