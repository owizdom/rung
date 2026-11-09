# Adjudicator brief (codebook v1.1)

Two independent coders coded each framework document. You rule on the cells where they disagree. You did not code anything yourself, and you must decide from the document, not from either coder's confidence.

1. Read /Users/macbook/Desktop/code/rung/coding/codebook.md in full (v1.1, including section E). Apply it literally.
2. Your disagreements are the rows of /Users/macbook/Desktop/code/rung/coding/disagreements.csv for the doc_ids named in your task message. Each row gives the risk, the rung, and each coder's value, quote, page and note.
3. For each row, open the document (its `cache_path` and `text_path` in /Users/macbook/Desktop/code/rung/frameworks/documents.csv; ~ means /Users/macbook). Read the cited pages AND any other part of the document needed to rule: for a 0-versus-1 split on `mentioned`, `threshold` or a scope question, search the whole text, and read the surrounding section in the PDF pages (Read tool, `pages` parameter) so you see tables and figures.
4. Decide the value under the codebook. For a 1, give one verbatim quote from the text file (10 to 400 characters, copied exactly; it may be one of the coders' quotes) and its page. For a 0, leave the quote empty.
5. Append one row per disagreement to /Users/macbook/Desktop/code/rung/coding/adjudication.csv with header `doc_id,risk,rung,value,quote,page,ruling` (create the file with that header if it does not exist; use Python's csv module). `ruling` is one or two sentences naming the codebook rule that decides it.
6. Write nothing else. Do not edit either coder's files.

Report back in under 300 words: how many rows you ruled, how many went to A's value and how many to B's, any ruling where the codebook itself was unclear (quote the rule and the passage), and the model you ran as.
