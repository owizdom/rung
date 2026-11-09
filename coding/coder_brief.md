# Coder brief (codebook v1.1)

You are one of two independent coders (A or B) in a content analysis of frontier AI safety frameworks. The other coder codes the same documents without seeing your work, and you must not see theirs.

1. Read /Users/macbook/Desktop/code/rung/coding/codebook.md in full and apply it literally. Its rules override your own judgement and anything you know about these companies.
2. Your documents are listed in your task message, with the row for each in the manifest named there (columns `doc_id`, `cache_path`, `text_path`, `pages`). For each document:
   - Read the source file at `cache_path` in full. For a PDF, use the Read tool with the `pages` parameter in chunks of at most 20 pages until you have seen every page, so you see tables and figures as well as text. For an HTML file, read the text file instead.
   - Use the text file at `text_path` to copy quotes exactly. Search it only to find exact wording after your full read, never in place of one.
3. Code only from the document (codebook A1). A 0 is a claim that the document lacks something, so you must have read all of it first.
4. Write one JSON file per document in your output folder, in the format of codebook section D. Put the UTC time in `coded_at`. Include all 5 risks and all 6 rungs.
5. Before finishing, run this from /Users/macbook/Desktop/code/rung, with your folder and manifest filled in:
   `python3 -m coding.check <LETTER> --base <OUTPUT_BASE> --manifest <MANIFEST>`
   Fix whatever it prints for your own files. Fix a quote by copying it exactly. Change a value only if the evidence is really not in the document.
6. Write nothing outside your own output folder, except helper scripts in your own scratch folder, named in your task message. Never open the other coder's folder or scratch folder, or any adjudication file.

Report back in under 300 words: the doc_ids you wrote; any page or figure you could not read and why; every codebook rule you found ambiguous, with the passage that made it so; and the model you ran as.
