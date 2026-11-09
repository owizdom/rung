# Consistency pass brief (codebook v1.2, section F)

A review found that three patterns were coded unevenly across developers. Codebook v1.2 adds rules F1 to F3 to settle them. You apply ONE of these rules (named in your task message) to every document in the study, so the rule lands the same way for every developer.

1. Read /Users/macbook/Desktop/code/rung/coding/codebook.md in full, including sections E and F.
2. Current final codes are in /Users/macbook/Desktop/code/rung/coding/codes.csv (one row per document and risk, six rungs) and the quote behind every 1 is in coding/quotes.csv. Documents: frameworks/documents.csv (cache_path, text_path; ~ means /Users/macbook). There are 40 documents; some are versions of the same framework, and identical wording must get the same ruling in every version.
3. For your rule, find every cell in all 40 documents that the rule governs (your task message says how), read the governing passage in its page context (PDF via the Read tool's `pages` parameter), and decide the value under the codebook with your rule applied.
4. Write a row ONLY for cells whose value should change from codes.csv, to your own output file (named in your task message), header:
   `doc_id,risk,rung,value,quote,page,ruling`
   For a new 1, `quote` is one verbatim span from that document's text file (10 to 400 characters). For a new 0, leave it empty. `ruling` names the rule and the passage in one or two sentences. Use Python's csv module.
5. Check your quotes: `python3 -c "import csv,sys; from coding.check import quote_found, documents, doc_text; D=documents(); [print('NOT FOUND', r['doc_id'], r['risk'], r['rung']) for r in csv.DictReader(open(sys.argv[1])) if r['value']=='1' and not quote_found(r['quote'], doc_text(D[r['doc_id']]))]" <your file>` from /Users/macbook/Desktop/code/rung, and fix anything it prints.
6. Write nothing else.

Report in under 300 words: how many cells you examined, how many changed (to 1 and to 0), the changes grouped by document in one line each, any case where the rule itself was unclear (quote the rule and the passage), and the model you ran as.
