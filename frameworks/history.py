"""Version history of every framework URL: one row per distinct capture digest, from the
Wayback CDX index plus the live file. Distinct texts at one URL are candidate versions.

Usage: python3 -m frameworks.history URLS.txt  ->  frameworks/url_history.csv
URLS.txt lines: <label> <url>
"""
from __future__ import annotations

import csv
import datetime as dt
import sys
from pathlib import Path

from frameworks.wayback import (CACHE, cdx_all, get, kind, printed_dates, raw_url, sha256, text_key, text_of,
                                ts_date, version_label)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "frameworks" / "url_history.csv"
FIELDS = ["label", "url", "source", "capture_ts", "capture_date", "cdx_digest", "sha256", "bytes", "kind",
          "pages", "words", "text_key", "version_label", "printed_dates", "cache_path", "error"]


def store(data: bytes) -> tuple[str, Path]:
    h = sha256(data)
    k = kind(data)
    p = CACHE / "docs" / f"{h}.{ 'pdf' if k == 'pdf' else 'html' if k == 'html' else 'bin'}"
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_bytes(data)
    return h, p


def row_for(label: str, url: str, source: str, ts: str, digest: str, data: bytes) -> dict:
    h, p = store(data)
    plain, layout, pages = text_of(data, p)
    tdir = CACHE / "text"
    tdir.mkdir(parents=True, exist_ok=True)
    (tdir / f"{h}.txt").write_text(plain, encoding="utf-8")
    (tdir / f"{h}.layout.txt").write_text(layout, encoding="utf-8")
    return {"label": label, "url": url, "source": source, "capture_ts": ts, "capture_date": ts_date(ts) if ts else "",
            "cdx_digest": digest, "sha256": h, "bytes": len(data), "kind": kind(data), "pages": pages,
            "words": len(plain.split()), "text_key": text_key(plain), "version_label": version_label(plain),
            "printed_dates": " | ".join(printed_dates(plain)), "cache_path": str(p), "error": ""}


def history(label: str, url: str) -> list[dict]:
    rows = []
    try:
        caps = [c for c in cdx_all(url) if c.get("statuscode") == "200"]
    except Exception as e:
        caps = []
        rows.append({"label": label, "url": url, "source": "wayback", "error": f"cdx: {e}"})
    seen = set()
    for c in sorted(caps, key=lambda c: c["timestamp"]):
        if c["digest"] in seen:
            continue
        seen.add(c["digest"])
        try:
            data = get(raw_url(c["timestamp"], url))
            rows.append(row_for(label, url, "wayback", c["timestamp"], c["digest"], data))
        except Exception as e:
            rows.append({"label": label, "url": url, "source": "wayback", "capture_ts": c["timestamp"],
                         "cdx_digest": c["digest"], "error": str(e)[:200]})
    try:
        data = get(url)
        now = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d%H%M%S")
        rows.append(row_for(label, url, "live", now, "", data))
    except Exception as e:
        rows.append({"label": label, "url": url, "source": "live", "error": str(e)[:200]})
    return rows


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    pairs = [l.split(None, 1) for l in Path(argv[0]).read_text().splitlines() if l.strip() and not l.startswith("#")]
    done = set()
    if OUT.exists():
        done = {(r["label"], r["url"]) for r in csv.DictReader(OUT.open(encoding="utf-8"))}
    new = not OUT.exists()
    with OUT.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        for label, url in pairs:
            url = url.strip()
            if (label, url) in done:
                continue
            rows = history(label, url)
            for r in rows:
                w.writerow({k: r.get(k, "") for k in FIELDS})
            f.flush()
            ok = [r for r in rows if not r.get("error")]
            print(f"{label}: {len(ok)} captures, {len({r['text_key'] for r in ok})} distinct texts", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
