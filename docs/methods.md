# What frontier safety frameworks commit to, risk by risk

Wisdom Okechukwu, November 2026. Data, code and every coded quote: github.com/owizdom/rung

## Question

Across published frontier safety frameworks, which of five risks does each one cover: cyber, bio and chem, AI R&D automation, autonomy, and loss of control? For each risk, does the framework only mention it, define a threshold, specify a response, or also name who is accountable?

## Short answer

Most frameworks that take a risk seriously enough to set a threshold also say what they will do when it is crossed. The drop-offs come before and after that point. Many frameworks name a risk without ever setting a level for it, and few close the loop with outside review.

- Of 13 developers with a published framework, 8 set a threshold for at least one of the five risks. Every one of those 8 also commits to a response.
- Only 4 reach full accountability on any risk: Amazon, Anthropic, G42 and OpenAI. Full accountability means a named decider, a commitment to outside review, and a stated consequence if the response fails.
- Outside review is the step most often missing. Of the 8 frameworks with a threshold and a response, 7 name a decider and 6 state a consequence, but only 5 commit to review from outside the company.
- Cyber and bio and chem are covered best: 7 developers set a threshold for each. AI R&D automation, autonomy and loss of control each get a threshold from only 5.
- Naver and Samsung Electronics publish frameworks that name none of the five risks.
- Across 40 versions, a risk's step went up 14 times and down 12 times between one version and the next.

## Findings

### 1. Naming a risk is common; setting a level for it is not

Cyber is named by 11 of the 13 frameworks, but only 7 define a cyber threshold. Bio and chem is named by 10 and gets a threshold from 7. Autonomy is named by 9 and gets a threshold from 5. Five frameworks never define a threshold for any of the five risks: Cohere, Magic, Naver, Samsung Electronics and xAI.

Magic's framework shows the pattern. It lists "Critical Capability Thresholds" for cyber, bio, AI R&D and autonomy, then calls them "high-level, illustrative capability levels". Under the codebook an illustration is not a threshold.

### 2. Where there is a threshold, there is a response

All 8 frameworks that define a threshold for a risk also commit to what they will do when it is reached: named safeguards, a security level, or holding back deployment or development. The step from threshold to response never fails in the current set.

The reverse happens. In 11 developer-and-risk cells a framework commits to a response with no threshold for that risk, across Cohere, Magic, Meta, Microsoft and xAI. xAI's June 2026 framework is the clearest case. It commits that "xAI will only proceed with the development, the making available on the market, and/or the use of the model, if the systemic risks stemming from the model are determined to be acceptable", but it defines no level for any risk. The ladder records these as gaps and does not credit the response.

### 3. Accountability stops at outside review

Among the 8 frameworks with a threshold and a response:

- 7 name who decides. Google DeepMind's v3.1 leaves the call to an unnamed "appropriate governance function".
- 6 say what happens if the response cannot be met. Google DeepMind and NVIDIA do not.
- 5 commit to review from outside the company. Meta, Microsoft and NVIDIA do not.

Under a looser rule, where a named decider plus either outside review or a stated consequence is enough, 6 developers reach the top step instead of 4: Meta and Microsoft join.

### 4. Anthropic's current policy no longer mentions cyber

Anthropic's Responsible Scaling Policy named cyber in versions 1.0 to 2.2. From version 3.0 (February 2026) it does not mention cyber at all. Anthropic's cyber coverage now comes only from its Frontier Compliance Framework, written for California's SB 53, which reaches the response step. The heatmap counts a step if either current document reaches it, so Anthropic's cyber cell shows a response.

## How commitments changed between versions

Of the 40 versions, 25 pairs are consecutive versions of one framework. Between them, a risk's step went up 14 times and down 12 times: 6 times softened, where the risk stays named but a step is lost, and 6 times removed, where the risk is no longer named. Every change was checked with both versions side by side (see Method).

Changes that lowered a step:

- OpenAI, Preparedness Framework beta to v2 (April 2025): autonomy and loss of control fall from accountability to mention. v2 moves them to "Research Categories" with no thresholds.
- Google DeepMind, Frontier Safety Framework v1.0 to v2.0 (February 2025): the autonomy risk domain is removed. v2.0 to v3.0 (September 2025): its misalignment levels become "illustrative only", so the loss of control threshold is lost. v3.1 (April 2026) restores a loss of control threshold and response.
- Anthropic, RSP v2.2 to v3.0: cyber removed (above).
- Amazon, February 2025 to September 2026: AI R&D automation stops being its own risk domain and drops from accountability to mention.
- xAI, December 2025 to June 2026: the numeric criteria for bio and chem and for dishonesty are removed, so both drop from response to mention. AI R&D is no longer named.
- Naver, v1.0 to v2.0 (July 2026): cyber, bio and chem, and loss of control are no longer named. v2.0 replaces risk categories with three protected values.

Changes that raised a step:

- Anthropic, RSP v1.0 to v2.0 (October 2024): bio and chem and AI R&D gain specific thresholds and the full accountability step, with an annual third-party review of compliance.
- Meta, Frontier AI Framework to Advanced AI Scaling Framework v2.0 (April 2026): AI R&D and loss of control gain thresholds and responses.
- Amazon, September 2026: a new loss of control domain covers autonomy and loss of control at the accountability step.
- xAI, draft to August 2025: bio and chem and loss of control gain numeric deployment criteria.

## Method

Universe. The 20 signatories of the Frontier AI Safety Commitments (AI Seoul Summit, 2024). A framework is a document the developer published to say how it will identify, assess and manage severe risks from its frontier models, including SB 53 frontier AI frameworks and renamed successors. Every published version up to 31 October 2026 counts. 13 developers have one, and there are 40 versions in all. The remaining 7 were searched across company sites, Chinese-language queries, the Wayback Machine and six trackers, with every search logged. IBM has only a governance blog post. Inflection has only a 2023 UK summit policy page. Zhipu has co-authored a general framework that commits nothing about its own models. Mistral, TII, MiniMax and 01.AI have none.

Versions. Each document was downloaded, hashed (sha256) and dated from the document itself, the announcement, or the METR list. The Wayback Machine history of every framework URL was checked for files replaced in place. Seven versions METR's list misses were found this way, including a re-issue of OpenAI's Preparedness Framework v2 that keeps the release date but drops a safeguard row. The current set is the latest version of each framework on 31 October 2026: 15 documents. Anthropic and OpenAI each run two.

Codebook. Each document is coded on five risks and six yes-or-no steps: mentioned, threshold, response, named decider, outside review, and a stated consequence if the response fails. A step needs binding language. "May", "consider", "intend" and "as appropriate" do not count. The EU General-Purpose AI Code of Practice, Safety and Security chapter, is the yardstick for what counts as specified. The codebook was piloted on 3 documents and frozen before coding.

Coding. Two independent coders, both Claude models, coded every one of the 1,200 cells. Each read every page, tables and figures included, and backed every yes with a quote that a script found verbatim in the document. A fresh adjudicator ruled on the 95 cells where they disagreed. Agreement before adjudication, as Cohen's kappa: mentioned 0.95, threshold 0.868, response 0.663, named decider 0.82, outside review 0.793, consequence 0.88. Weighted kappa on the overall level is 0.885. The response step falls below the 0.7 bar the study set, so a single coder's reading of it would be unreliable. Every response code in the final data was either agreed by both coders or ruled by the adjudicator.

Changes between versions. Coding one version at a time makes the same wording look like a change if two coders read it differently. So every step that moved between consecutive versions was re-checked with both versions open, ruling 232 cells. Of the 118 moves first found, 22 were the same wording coded two ways and were corrected. That exposed 5 more moves next to them, 2 of which were also inconsistencies. All remaining moves are changes in the documents' wording.

## Limits

Gaps in the public record:
- Anthropic's Frontier Compliance Framework v1.2 (June 2026) could not be obtained. It was replaced on Anthropic's trust portal and never archived.
- Some dates rest on indirect sources. OpenAI's Frontier Governance Framework announcement page is blocked to automated access, so its May 2026 date comes from the METR list and the first archive capture. Microsoft's February 2026 version prints no day. The dates of OpenAI's and Meta's silent re-issues come from file metadata and first archive captures.
- Seven signatories have no framework, so they cannot appear on the heatmap.

Choices in this study:
- Both coders, the adjudicators and the cross-version checkers are Claude models. The brief asks for two people to code at least 25% of cells; here two model coders coded all of them, and no human audited the codes.
- Level 4 needs all three accountability parts. The looser rule is reported above.
- A developer's cell takes each step from any current document, which matters for Anthropic (RSP and Compliance Framework) and OpenAI (Preparedness and Governance Frameworks). Each document is also reported on its own in the data.
- Autonomy and loss of control are coded as two risks. Merging them would not change any developer's top level.
- Samsung Electronics is included because its "AI Safety Framework" is its Seoul-commitment document, even though it covers on-device AI and names none of the five risks.

## Sources

METR, Frontier AI Safety Policies (metr.org/fsp) and Common Elements of Frontier AI Safety Policies (December 2025); UK Government, Frontier AI Safety Commitments, AI Seoul Summit 2024; European Commission, General-Purpose AI Code of Practice, Safety and Security chapter (July 2025); California SB 53; SaferAI Frontier Risk Management Tracker; FLI AI Safety Index (Summer 2026); the 40 framework documents and their Wayback Machine archives.
