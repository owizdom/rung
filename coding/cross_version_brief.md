# Cross-version brief (codebook v1.1)

Each framework was coded one version at a time. Between consecutive versions of the same framework, some rungs move from 0 to 1 or from 1 to 0. A move is either a real change in the document, or the same wording coded two ways. Your job is to settle each move with both versions open side by side, so the final data shows only real changes.

1. Read /Users/macbook/Desktop/code/rung/coding/codebook.md in full (v1.1 with section E) and apply it literally.
2. Your moves are the rows of /Users/macbook/Desktop/code/rung/coding/change_flags.csv for the lines named in your task message. Each row gives the two versions, the risk, the rung, the value in each, and the quote behind the 1 (`quote_in_other` = 1 means that exact quote was also found in the version coded 0).
3. For each move, open both documents (paths in /Users/macbook/Desktop/code/rung/frameworks/documents.csv; ~ means /Users/macbook). Find the passage behind the 1, then look for the same or equivalent passage in the other version: search the text file, then read the surrounding pages in the PDF (Read tool, `pages` parameter) so tables are seen.
4. Decide the correct value for this risk and rung in EACH version, each from its own text under the codebook. If the governing wording is the same in both versions (allowing for trivial edits), the two values must be the same. A change is real only when the document's wording changed in a way the codebook cares about: a risk added or dropped, a threshold defined or withdrawn, a binding verb hedged or made binding, a named decider or outside review added or removed.
5. Write one row per document cell to your own output file (named in your task message), header:
   `doc_id,risk,rung,value,quote,page,ruling,change_real`
   - Write BOTH cells of every move (the from version and the to version). If a cell appears in two moves (a middle version), write it once, consistent with both.
   - `quote`: for a 1, one verbatim span from that document's text file (10 to 400 characters, copied exactly). For a 0, empty.
   - `ruling`: one or two sentences: what the governing wording is in each version and which codebook rule decides.
   - `change_real`: `yes` if the wording really changed between the two versions for this cell's move, `no` if it is the same wording.
   Use Python's csv module.
6. Check your quotes before finishing, from /Users/macbook/Desktop/code/rung:
   `python3 -c "import csv,sys; from coding.check import quote_found, documents, doc_text; D=documents(); [print('NOT FOUND', r['doc_id'], r['risk'], r['rung']) for r in csv.DictReader(open(sys.argv[1])) if r['value']=='1' and not quote_found(r['quote'], doc_text(D[r['doc_id']]))]" <your output file>`
   and fix anything it prints.
7. Write nothing else. Do not edit coders' files, adjudication.csv, or other agents' output files.

Report back in under 300 words: how many moves you judged real and how many coding inconsistencies; the real changes in one line each; any codebook rule that was unclear (quote the rule and the passage); and the model you ran as.
