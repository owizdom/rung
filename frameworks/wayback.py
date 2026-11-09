"""Wayback Machine and download helpers (adapted from owizdom/tide cards/fetch.py)."""
from __future__ import annotations

import gzip
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path
from urllib.parse import quote

CACHE = Path.home() / ".rung-cache"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36 rung-research"


def raw_url(ts: str, url: str) -> str:
    return f"https://web.archive.org/web/{ts}id_/{url}"


def ts_date(ts: str) -> str:
    return f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}"


def decompress(data: bytes) -> bytes:
    if data[:4] == b"\x28\xb5\x2f\xfd":
        return subprocess.run(["zstd", "-dc", "-q"], input=data, capture_output=True, check=True).stdout
    if data[:2] == b"\x1f\x8b":
        return gzip.decompress(data)
    return data


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def get(url: str, tries: int = 4) -> bytes:
    import requests

    last = None
    for i in range(tries):
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=120)
            if r.status_code == 200:
                return decompress(r.content)
            last = f"HTTP {r.status_code}"
            if r.status_code in (400, 403, 404, 410):
                break
        except Exception as e:  # retried, then raised
            last = repr(e)
        time.sleep(10 * (2 ** i))
    raise RuntimeError(f"{url}: {last}")


def cdx_query(url: str) -> str:
    bare = quote(re.sub(r"^https?://", "", url), safe=":/%~@!$'()*+,;=")
    return (f"https://web.archive.org/cdx/search/cdx?url={bare}&output=json"
            f"&fl=timestamp,statuscode,digest,mimetype,length&limit=5000")


def cdx_all(url: str) -> list[dict]:
    time.sleep(1)
    body = get(cdx_query(url))
    rows = json.loads(body or b"[]")
    if not rows:
        return []
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:]]


def kind(data: bytes) -> str:
    if data[:5] == b"%PDF-":
        return "pdf"
    head = data[:2000].lower()
    if b"<html" in head or b"<!doctype html" in head:
        return "html"
    return "other"


def pdf_text(path: Path, layout: bool = False) -> str:
    args = ["pdftotext"] + (["-layout"] if layout else []) + [str(path), "-"]
    return subprocess.run(args, capture_output=True, check=False).stdout.decode("utf-8", "replace")


def pdf_pages(path: Path) -> int:
    out = subprocess.run(["pdfinfo", str(path)], capture_output=True).stdout.decode("utf-8", "replace")
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else 0


def html_text(data: bytes) -> str:
    import html as H

    s = data.decode("utf-8", "replace")
    s = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<(br|/p|/div|/li|/h[1-6]|/tr|/section|/article)[^>]*>", "\n", s)
    s = re.sub(r"(?i)<li[^>]*>", "\n- ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = H.unescape(s)
    s = re.sub(r"[ \t ]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s.strip()


def text_of(data: bytes, path: Path) -> tuple[str, str, int]:
    """(plain text, layout text, pages) for cached bytes at path."""
    k = kind(data)
    if k == "pdf":
        return pdf_text(path), pdf_text(path, layout=True), pdf_pages(path)
    if k == "html":
        t = html_text(data)
        return t, t, 0
    return data.decode("utf-8", "replace"), "", 0


def text_key(text: str) -> str:
    """Hash of the words only, so re-uploads that differ in bytes but not in text group together."""
    return sha256(re.sub(r"\W+", " ", text.lower()).strip().encode())[:16]


VERSION_RE = re.compile(r"\b(?:version|v)\s?(\d+(?:\.\d+)*)\b", re.I)
DATE_RE = re.compile(
    r"\b(?:(?:effective|published|last updated|updated|applicable from|initial publication date|effective date)[:\s]+)?"
    r"((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+20\d\d"
    r"|\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December),?\s+20\d\d"
    r"|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+20\d\d)", re.I)


def version_label(text: str) -> str:
    m = VERSION_RE.search(text[:4000])
    return m.group(1) if m else ""


def printed_dates(text: str) -> list[str]:
    return [m.group(0).strip() for m in DATE_RE.finditer(text[:4000])][:4]
