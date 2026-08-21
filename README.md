# The Polite Scraper

A small, well-behaved scraping pipeline built for FlyRank Internship — Backend Track, Week 5, Assignment A9.

It downloads the first three catalogue pages of [Books to Scrape](https://books.toscrape.com), visits all 60 book pages, turns the raw HTML into clean, schema-validated JSON, survives a broken page without crashing, and ends every run with a short report of what happened.

**Pipeline:** `fetch → extract → normalize → validate → store → report`

---

## Target classification

| | |
|---|---|
| **Site** | `books.toscrape.com` |
| **Why** | It is a public sandbox explicitly built for people to practise scraping on — stated on the site itself. |
| **Scope** | The first 3 catalogue pages only (60 book listings, followed via the site's own "next" link — not hardcoded). |
| **Data collected** | Title, price, availability, star rating, description, and canonical URL for each book. Nothing beyond what's needed for the assignment. |
| **`robots.txt` check** | Requested `https://books.toscrape.com/robots.txt` once → **404 Not Found**. No robots file exists. A missing file is not treated as blanket permission — it's simply the absence of a rule — so scope was still kept to the sandbox's intended practice use (3 pages, one polite pass). |

> I will not reuse this code on another site without checking its rules and terms first.

---

## Lane & installation

**Python 3.10+**, using `requests`, `BeautifulSoup4`, and `Pydantic`.

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>/scraper
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run it

```bash
python src/main.py
```

This single command fetches (or reads from cache), extracts, normalizes, validates, and stores all 60 records, then writes a run report. Re-running it produces the same 60 records — never duplicates — and reads mostly from cache.

---

## Project structure

```
scraper/
├── src/
│   └── main.py           # entry point: runs the full pipeline
├── cache/                 # saved HTML responses (gitignored)
├── output/
│   ├── books.json         # 60 validated records
│   ├── errors.json        # records that failed validation, with reasons
│   └── run-report.json    # honest numbers for the run
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Record schema

**Raw record** (as extracted from each book page):

```json
{
  "title": "A Light in the Attic",
  "product_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "price_text": "£51.77",
  "availability_text": "In stock (22 available)",
  "rating_text": "Three",
  "description": "...",
  "source_page": "https://books.toscrape.com/catalogue/page-1.html",
  "fetched_at": "2026-08-06T10:00:00Z"
}
```

**Validated record** (stored in `books.json`, checked with Pydantic):

| Field | Type | Notes |
|---|---|---|
| `title` | `str` | required |
| `product_url` | `HttpUrl` | required — canonical identity of the record |
| `price_text` | `str` | required — original text, kept alongside the clean value |
| `price_gbp` | `float` | required — numeric price parsed from `price_text` |
| `availability_text` | `str` | required |
| `rating_text` | `str` | required |
| `description` | `str \| null` | optional — `null` when the page has none, never invented |
| `source_page` | `HttpUrl` | required — provenance |
| `fetched_at` | `str` (ISO 8601) | required — provenance |

Records are deduplicated on `product_url`. Anything that fails validation is written to `errors.json` with the reason, never into `books.json`.

---

## Politeness rules

- **User-agent:** every request identifies itself, e.g. `FlyRankInternshipA9/1.0 (+https://github.com/<your-username>/<your-repo>)`.
- **Timeout:** every request gives up after a few seconds rather than hanging.
- **Delay:** at least 500 ms between real requests to the site. Cache hits add no delay.
- **Cache:** every page is saved to `cache/` on first fetch; development re-reads the saved copy instead of re-hitting the site.
- **Status check:** only `200` is treated as a successful fetch. `404` and `403` are never retried; `5xx` and timeouts get a single retry.

## Failure handling

Each page is fetched and parsed independently, so one broken page is logged and skipped without taking down the run. This was verified by adding one deliberately fake book URL to the list — the run still finished with all 60 good records, and `run-report.json` reported `"failed_pages": 1`.

## Sample run report

```json
<paste your actual output/run-report.json here>
```

## Why no browser was needed

The book data — title, price, availability, rating, description — is already present in the HTML the server sends on first request; nothing is rendered client-side with JavaScript. A headless browser would only add cost (memory, startup time, complexity) with no extra data in return.

## Ethics note

- Use an official API instead of scraping whenever one exists.
- Never bypass logins, paywalls, or explicit blocks.
- Collect only the data actually needed for the task, at a low, respectful rate.
- This project touches a single public practice sandbox built for exactly this purpose — the approach here is not assumed valid for any other site.

## Known limitation

<one honest limitation — e.g. retry logic is a single attempt with a fixed wait, not full exponential backoff; that upgrade is scoped for next week's assignment (A16).>

---

Built for FlyRank Internship, Backend Track — Week 5, Assignment A9.
