# Journal

## Snapshot

- 2026-11-09: spec 0001 approved; census done; list (40 versions, 15 current) and codebook v1.1 FROZEN. Main passes on the current set next.
- Next: freeze documents.csv after the census, then the codebook pilot on 3 documents.

## Evidence log (append only)

- 2026-11-09T11:20Z: inputs read. METR list metr.org/fsp (html sha256 28575229…), gov.uk Seoul commitments page (sha256 8323f289…, 20 signatories), EU Code of Practice Safety and Security chapter PDF (sha256 d879f9b54c6068aae57ebaead9d90ddaa46f2503312b9185367a724fa8da2f4a, 43 pages). Probe: 28 of 38 METR-linked URLs return PDFs; RSP v2.0, Meta AASF v2.0 (HTTP 400), Amazon FMSF 2025 (landing page) need archive copies; Anthropic FCF is a Vanta trust-portal page.
- 2026-11-09: Wisdom approved spec 0001 with: level 4 = all three accountability parts; two Claude passes on all cells, no hand coding; latest versions then all earlier versions; local commits on owizdom/rung-v1.
- 2026-11-09T13:31:22Z: census merged. 40 versions from 13 developers (Samsung included as its Seoul framework; IBM blog post, Inflection 2023 summit page and Zhipu co-authored framework excluded, reasons in universe.yaml). Anthropic FCF v1.2 has no obtainable bytes (replaced on the trust portal, never archived). Every distinct PDF text in the Wayback history of each URL maps to a listed version or is a layout/one-word variant (Meta 2.1 page headers, GDM 2.0 link fix, RSP 2.0 changelog link, xAI Aug 2025 one word) or an empty capture. Magic page: published text 2024-07-04 coded as 1.0; "This policy is outdated" note added between 2026-09-02 and 2026-09-08, coded as 1.0r (current).
- FREEZE 2026-11-09T13:31:22Z: documents.csv sha256 644c74279ea3f912da480836ccf26cba35b12d31d66fcaa90f992e2ba4315b85, codebook.md sha256 e6eae305adf934a4c9e128bf7d1135062ee3d8df1efdea41900a4bb4caf9b3ab
