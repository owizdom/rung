"""Write frameworks/documents.csv from universe.yaml: verify each document's bytes against its
recorded sha256, store them content-addressed in the cache and extract plain and layout text.

Usage: python3 -m frameworks.build_documents
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

from frameworks.census import ROOT, current_set, load_universe
from frameworks.history import row_for
from frameworks.wayback import CACHE, sha256

OUT = ROOT / "frameworks" / "documents.csv"
FIELDS = ["doc_id", "developer", "line", "title", "version", "published", "published_source", "url", "archive_url",
          "sha256", "bytes", "kind", "pages", "words", "cache_path", "text_path", "layout_path", "current", "note"]


def main() -> int:
    u = load_universe()
    cur = {d["doc_id"] for d in current_set(u)}
    out = []
    for d in u:
        data = Path(d["local"]).expanduser().read_bytes()
        if sha256(data) != d["sha256"]:
            print(f"{d['doc_id']}: sha256 mismatch", file=sys.stderr)
            return 1
        r = row_for(d["doc_id"], d["url"], "census", "", "", data)
        out.append({**{k: d.get(k, "") for k in FIELDS}, "bytes": r["bytes"], "kind": r["kind"], "pages": r["pages"],
                    "words": r["words"], "cache_path": r["cache_path"].replace(str(Path.home()), "~"),
                    "text_path": str(CACHE / "text" / f"{d['sha256']}.txt").replace(str(Path.home()), "~"),
                    "layout_path": str(CACHE / "text" / f"{d['sha256']}.layout.txt").replace(str(Path.home()), "~"),
                    "current": int(d["doc_id"] in cur)})
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} documents, {sum(r['current'] for r in out)} current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
