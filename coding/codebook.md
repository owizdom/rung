# Codebook v1.2 (spec 0001)

You code one framework document at a time. For each of five risks you answer six yes-or-no questions (the rungs), and you back every yes with a quote. That gives 30 codes per document, plus a list of the other risks the document names. You do not compute levels; the analysis does that from your rungs.

## A. General rules

A1. Code only from this document: its text, tables, figures, footnotes, appendices and changelog. Use no outside knowledge of the developer or of other documents. If the document points to another document ("as set out in our security policy"), only what this document itself says counts.

A2. Read the whole document before coding. A 0 says the document does not contain something. You can only say that after reading all of it, including every table and figure.

A3. The developer's own voice. Only what the developer says about its own practice counts. A description of a law, of the Seoul commitments or of another company's practice counts only if the document adopts it as its own ("we follow ...").

A4. Binding language. The `response` rung and the three accountability rungs need a commitment:
- Counts: will, shall, must, commit(s) to, is required to, will not, does not (when stating a rule), and "would" in an if-then sentence about the developer's own action ("If a model reached X, we would not deploy it").
- Does not count: may, might, could, can, consider, aim, seek, strive, endeavour, hope, explore, expect, intend, plan, anticipate, "are working towards". A qualifier on the action itself also voids it: "as appropriate", "where feasible", "where possible", "if practicable".
- A sentence with both a binding verb and a voiding qualifier on the same action does not count. "We will implement appropriate safeguards" does count if "appropriate" describes safeguards that the document then names (rule C3). It does not count if nothing is named.

A5. Quotes. Every 1 needs one contiguous span copied exactly from the document, 10 to 400 characters, that supports the code by itself as far as possible. Copy it character for character: do not fix typos, do not join text from two places, do not paraphrase. If the support needs two passages, quote the one that carries the commitment and give the other passage's page in the note.

A6. Notes. Every 0 needs a short note saying why. Where the risk's words occur but do not meet the rung, say what you found and where ("cyber named p.3 only as a beneficial use"; "p.9 says 'may restrict access', hedged"). Notes for 1s are optional.

A7. Pages. Give the page as `p.N` using the PDF page number (the viewer's page index, not the printed folio). For HTML documents give the nearest heading.

A8. Figures and tables. If the support is only in an image with no selectable text, quote what the image says as exactly as you can, set `"from_image": true`, and give the page. The adjudicator checks these against the page image.

A9. One passage can support several risks or rungs. Cite it each time. A framework-wide rule ("for every capability threshold in this framework we will ...") applies to each risk that has a threshold in the framework.

A10. A changelog or version-history passage counts only for what this version does. "We removed X" is not a mention of X as a risk this version covers.

## B. The five risks

| Risk key | Counts | Does not count |
|---|---|---|
| `cyber` | offensive cyber capability: cyberattacks, cyber operations, finding or exploiting vulnerabilities, malware, attacks on critical infrastructure | securing the developer's own systems or weights; the model's use for cyber defence; generic "cybersecurity" practices |
| `biochem` | biological or chemical weapons or attacks; CBRN named as one category; biosecurity or chemical security threats | radiological or nuclear alone; medical advice; general "harmful content" |
| `ai_rnd` | the model automating or greatly speeding up AI or ML research and development; AI self-improvement; recursive improvement; automating AI researchers' work | AI used as a coding assistant with no research-acceleration framing |
| `autonomy` | the model acting on its own in the world: autonomous replication and adaptation, self-proliferation, acquiring resources, long-range or long-horizon autonomous task execution | agentic product features described as benefits |
| `loss_of_control` | the model acting against the intent of its developer or user, or humans losing the ability to direct, correct or shut it down: misalignment, deceptive alignment, scheming, sandbagging, undermining oversight or safeguards, self-exfiltration, resisting shutdown or modification, "loss of control" | ordinary errors or hallucinations; misuse by humans |

Boundary rules:
- B1. A passage about two risks is coded for both. "Autonomous replication to evade shutdown" is `autonomy` and `loss_of_control`.
- B2. A threshold counts for a risk when the document presents it as marking that risk. A threshold for ML R&D capability is an `ai_rnd` threshold. It is also a `loss_of_control` threshold only if its own text is about misalignment or loss of control.
- B3. Record every other risk the document names as in scope in `other_risks`, as short labels: "harmful manipulation", "persuasion", "nuclear and radiological", "privacy", and so on.

## C. The six rungs

Answer each question for one risk at a time.

### C1. `mentioned`: does the document name this risk as one the developer considers?

1 when the document names the risk, or a clear equivalent from the table, as something the developer considers, assesses, evaluates, monitors, tracks or researches.

0 when the risk appears only in a citation, a quoted law, a list of beneficial uses or an example unrelated to risk, or when the document says it is out of scope. Write "explicitly out of scope" in the note for that last case.

Example 1: "We evaluate each new model for capabilities that could assist cyberattacks." This is a mention.

Example 0: "Our models help security teams defend networks." This is a beneficial use, not a risk.

### C2. `threshold`: does the document define a specific level for this risk at which what the developer does changes?

1 when the document itself defines at least one capability or risk level for this risk that triggers a change in what the developer does. That change can be more evaluation, safeguards, or a halt. The level is specific when it says what a model could do in this domain, or gives a quantitative criterion for this domain. Examples: "can give meaningful uplift to a person with basic training in creating a known biological weapon"; "scores above 40% on benchmark Z"; "can fully automate the work of an entry-level AI researcher".

A named level ("High", "Critical", "Level 3", a "critical capability level") counts only when the document says what it means for this risk. Early-warning or alert levels count if they trigger a change in what the developer does.

0 when the only levels are generic ("severe risk", "unacceptable risk", "significant harm") with nothing specific to this domain. It is also 0 when thresholds are promised for the future ("we will develop thresholds for ...") or are given only as illustrations ("for example, a threshold might be ...").

### C3. `response`: does the document commit to what the developer will do when this risk's threshold is reached?

1 when the document commits, in binding language (A4), to at least one of these for when the threshold is reached, crossed or forecast to be crossed:
- (a) named safeguards or security measures. Named means specific enough to check: a standard the document itself defines (a named deployment or security standard with its measures listed), or concrete measures such as restricting access to vetted users, removing the capability, classifiers on the domain, or a stated security level with its measures.
- (b) not deploying, restricting deployment, or pausing or stopping development, until the risk is reduced. "We will only deploy if safeguards reduce the risk below the threshold" counts.

If the risk has no threshold but the document commits to such a response for the risk anyway, code 1. The analysis records this as a gap in the ladder.

0 for: "appropriate", "commensurate" or "proportionate" safeguards with nothing named; more evaluation, monitoring, reporting or notification alone; any hedged verb.

### C4. `acc_decider`: does the document name who decides?

1 when the document names a specific role or body with a formal part in deciding whether this risk's threshold is reached, whether the response is adequate, or whether to proceed. A formal part means it decides, approves, or can overrule. Examples: a named officer such as a "Responsible Scaling Officer", a named committee or council, the CEO, the board or a named board committee. A generic label ("Leadership") counts only if the document defines it as specific roles.

0 for "leadership", "senior management", "relevant teams", "the company", "an appropriate governance body" with no name, or a body that only advises.

Code 1 only if the decision covers this risk's threshold or response. If the risk has neither a threshold nor a response, code 0 with the note "nothing to decide for this risk".

### C5. `acc_external`: does the document commit to review from outside the company?

1 when the document commits, in binding language, to review by a party outside the developer. The review can cover the model's capabilities on this risk (third-party evaluation, government pre-deployment testing), the threshold or safeguards decision (external expert review), or the developer's adherence to the framework (external audit or review). Committed bug bounties or red-teaming by outsiders count when they test the safeguards for this risk.

0 for "may seek", "where appropriate" or "could involve" external input; for notifying or sharing information with a government without it testing or reviewing anything; for publishing results.

Same scope rule as C4: code 1 only if it covers this risk's threshold, response or safeguards. A framework-wide external review of adherence covers every risk that has a threshold or response.

### C6. `acc_unmet`: does the document say what happens if the response is not met?

1 when the document says, in binding language, what the developer will do if it cannot put the required response in place, or if the response or framework is not followed. Either:
- (a) pause, delay, restrict, or not proceed with deployment or development until the response is in place, or withdraw the model; or
- (b) a stated non-compliance procedure: non-compliance is reported to a named body, investigated, or disclosed.

The same passage can support both `response` and `acc_unmet`. Same scope rule as C4.

0 when the document never says what happens if the response fails, or says it only with hedged verbs.

## D. Output

One JSON file per document, at `coding/passes/<A or B>/<doc_id>.json`:

```
{"doc_id": "<id>", "coder": "<A|B>", "codebook": "v1.1", "coded_at": "<UTC ISO time>",
 "other_risks": ["<label>", ...],
 "risks": {
   "cyber": {
     "mentioned":    {"value": 1, "quote": "<verbatim>", "page": "p.3", "note": ""},
     "threshold":    {"value": 0, "quote": "", "page": "", "note": "<why>"},
     "response":     {...}, "acc_decider": {...}, "acc_external": {...}, "acc_unmet": {...}
   },
   "biochem": {...}, "ai_rnd": {...}, "autonomy": {...}, "loss_of_control": {...}
 }}
```

Add `"from_image": true` to a code only when rule A8 applies.

## E. Rulings from the pilot (v1.1)

E1. Present tense. A present-tense sentence counts as binding when it states a rule tied to a condition ("When a model reaches the threshold, we apply X"; "Models above this level are deployed only with Y"). It does not count when it describes current practice with no condition ("We apply classifiers to our products").

E2. "As needed" and "as necessary". They set how far a named action goes ("we will delay development as needed to achieve this"), so they do not void it. "As appropriate", "where feasible", "where possible" and "if practicable" still void the action (A4).

E3. Generic acceptance gate. "We will only proceed if the risks are determined to be acceptable" counts for `response` under C3(b) for each risk the gate covers. That holds even when "acceptable" is undefined and the risk has no threshold; the analysis records the missing threshold as a gap.

E4. `acc_unmet` versus the gate. `acc_unmet` needs a statement about what happens when a response the document requires (named safeguards, a security standard, a mitigation) cannot be met or is not followed. A gate like E3, whose only condition is the risk being acceptable, does not also count for `acc_unmet`. "We will not deploy unless the ASL-N safeguards are in place" counts for both rungs, because the safeguards are the required response.

E5. Thresholds that trigger reporting or analysis. A level that triggers extra analysis, a risk report or more evaluation still counts for `threshold` (C2). Reporting alone is not a `response` (C3).

E6. Protections already in place. A commitment to keep named protections in place for models at or above this risk's threshold counts for `response`.

E7. Approaches the document describes but does not adopt (for example "one approach in the industry is ...") count for nothing (A3).

## F. Rulings from the review (v1.2)

These three rules settle patterns the first coding applied unevenly across developers. They apply to every document and every risk.

F1. Illustrative sections. Text inside a section, appendix or table that the document itself labels illustrative, an example, or "not a definitive or comprehensive list" counts for nothing on any rung, even when a sentence in it uses "will" or "require". This extends C2 ("given only as illustrations") from thresholds to every rung.

F2. Discretionary outside review. `acc_external` needs a commitment that an outside party will review in the cases the document covers. It does not count when the document leaves whether outsiders take part to the developer's discretion: "as needed", "where appropriate", "when available and feasible", "if warranted", or "the decision to involve external experts is made by" the developer. This overrides E2 for this rung only. A present-tense description of practice with no condition does not count either (E1).

F3. A threshold that describes two risks. A threshold counts for each of the five risks whose capability its own definition describes, including examples given inside the definition itself ("including ... the research, development and deployment of frontier models" describes AI R&D). An "associated risk" column, a rationale or a list of consequences beside the threshold is not its definition. This refines B2.
