#!/usr/bin/env python3
"""
Download open-access PDFs for an OpenAlex search.

Usage
-----
1. Find the API URL for your search. On the OpenAlex results page, click the
   API icon (or just convert the UI URL by hand). For your current search it
   would be something like:

       https://api.openalex.org/works?search=mining%20gold%20biodiversity

   Paste that into BASE_URL below, *without* a cursor parameter — the script
   adds one.

2. Set EMAIL to your real address. OpenAlex's "polite pool" gives faster,
   more reliable responses; some publisher hosts also throttle anonymous
   User-Agents hard.

3. Run:  python openalex_pdf_download.py

Outputs
-------
    ./pdfs/W<openalex_id>.pdf      one file per successfully fetched work
    ./openalex_works.jsonl         one JSON object per work (full metadata)
    ./download_log.csv             per-work outcome (status, url, reason)

Re-running is safe: works whose PDF already exists on disk are skipped.
"""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path
from urllib.parse import urlencode

import httpx

# ---------------------------------------------------------------------------
# Config — edit these
# ---------------------------------------------------------------------------

BASE_URL = "https://api.openalex.org/works"
SEARCH_PARAMS = {
    "search": "mining gold biodiversity",
    # Add filters here if you want to mirror UI facets, e.g.:
    # "filter": "is_oa:true,from_publication_date:2015-01-01",
}
EMAIL = "your.email@example.com"     # <- replace
OUT_DIR = Path("pdfs")
META_PATH = Path("openalex_works.jsonl")
LOG_PATH = Path("download_log.csv")

PER_PAGE = 200          # OpenAlex max
PAGE_SLEEP = 1.0        # between API pages
PDF_SLEEP = 1.5         # between PDF fetches (be polite to publishers)
PDF_TIMEOUT = 60        # seconds
MAX_PDF_BYTES = 50 * 1024 * 1024   # skip anything claiming >50 MB

# ---------------------------------------------------------------------------


def iter_works() -> list[dict]:
    """Page through the OpenAlex search using cursor pagination."""
    params = dict(SEARCH_PARAMS)
    params["per-page"] = PER_PAGE
    params["mailto"] = EMAIL
    cursor = "*"
    works: list[dict] = []

    with httpx.Client(timeout=30.0) as client:
        while cursor:
            params["cursor"] = cursor
            url = f"{BASE_URL}?{urlencode(params)}"
            r = client.get(url, headers={"User-Agent": f"pdf-downloader ({EMAIL})"})
            r.raise_for_status()
            payload = r.json()

            batch = payload.get("results", [])
            works.extend(batch)
            print(f"  fetched {len(works)} / {payload['meta']['count']}")

            cursor = payload["meta"].get("next_cursor")
            time.sleep(PAGE_SLEEP)

    return works


def pick_pdf_url(work: dict) -> str | None:
    """
    Return the best PDF URL for a work, or None if none is advertised.

    Order of preference:
      1. best_oa_location.pdf_url    (OpenAlex's own choice)
      2. primary_location.pdf_url    (publisher copy, often paywalled but worth trying)
      3. any locations[].pdf_url     (repositories, preprint servers)
    """
    boa = work.get("best_oa_location") or {}
    if boa.get("pdf_url"):
        return boa["pdf_url"]

    prim = work.get("primary_location") or {}
    if prim.get("pdf_url"):
        return prim["pdf_url"]

    for loc in work.get("locations") or []:
        if loc and loc.get("pdf_url"):
            return loc["pdf_url"]

    return None


def short_id(openalex_id: str) -> str:
    """'https://openalex.org/W123' -> 'W123'."""
    return openalex_id.rsplit("/", 1)[-1]


def looks_like_pdf(resp: httpx.Response) -> bool:
    """Sanity-check the response before saving."""
    ctype = resp.headers.get("content-type", "").lower()
    if "pdf" in ctype:
        return True
    # Some servers send octet-stream; check magic bytes
    return resp.content[:5] == b"%PDF-"


def download_pdf(client: httpx.Client, url: str, dest: Path) -> tuple[bool, str]:
    """Try to fetch one PDF. Returns (ok, reason)."""
    try:
        r = client.get(url, follow_redirects=True, timeout=PDF_TIMEOUT)
    except httpx.HTTPError as e:
        return False, f"network_error: {type(e).__name__}"

    if r.status_code != 200:
        return False, f"http_{r.status_code}"

    clen = r.headers.get("content-length")
    if clen and int(clen) > MAX_PDF_BYTES:
        return False, f"too_large_{clen}"

    if not looks_like_pdf(r):
        ctype = r.headers.get("content-type", "?")
        return False, f"not_pdf (content-type={ctype})"

    dest.write_bytes(r.content)
    return True, "ok"


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    print("Fetching metadata from OpenAlex...")
    works = iter_works()
    print(f"Got {len(works)} works.\n")

    # Persist full metadata so you can re-derive PDF URLs without re-hitting the API
    with META_PATH.open("w") as f:
        for w in works:
            f.write(json.dumps(w) + "\n")

    log_rows = []
    headers = {"User-Agent": f"pdf-downloader ({EMAIL})"}

    with httpx.Client(headers=headers) as client:
        for i, w in enumerate(works, 1):
            wid = short_id(w["id"])
            dest = OUT_DIR / f"{wid}.pdf"

            if dest.exists():
                log_rows.append({"id": wid, "status": "skipped_exists",
                                 "url": "", "reason": ""})
                continue

            url = pick_pdf_url(w)
            if not url:
                log_rows.append({"id": wid, "status": "no_pdf_url",
                                 "url": "", "reason": "no OA pdf advertised"})
                print(f"[{i:>4}/{len(works)}] {wid}  no PDF URL")
                continue

            ok, reason = download_pdf(client, url, dest)
            status = "ok" if ok else "failed"
            log_rows.append({"id": wid, "status": status,
                             "url": url, "reason": reason})
            tag = "✓" if ok else "✗"
            print(f"[{i:>4}/{len(works)}] {tag} {wid}  {reason}")
            time.sleep(PDF_SLEEP)

    with LOG_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "status", "url", "reason"])
        writer.writeheader()
        writer.writerows(log_rows)

    # Summary
    n_ok      = sum(1 for r in log_rows if r["status"] == "ok")
    n_skipped = sum(1 for r in log_rows if r["status"] == "skipped_exists")
    n_no_url  = sum(1 for r in log_rows if r["status"] == "no_pdf_url")
    n_failed  = sum(1 for r in log_rows if r["status"] == "failed")
    print()
    print(f"Done. ok={n_ok}  skipped={n_skipped}  no_url={n_no_url}  failed={n_failed}")
    print(f"PDFs in:   {OUT_DIR.resolve()}")
    print(f"Metadata:  {META_PATH.resolve()}")
    print(f"Log:       {LOG_PATH.resolve()}")


if __name__ == "__main__":
    main()
