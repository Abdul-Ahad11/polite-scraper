# The Polite Scraper

**FlyRank Internship — Backend Track — Week 5 — Assignment A9**

## About This Assignment

The assignment is to build a small, respectful scraping pipeline against [Books to Scrape](https://books.toscrape.com/), a public sandbox site made specifically for web-scraping practice.

The goal is to download the first three catalogue pages, follow them to all 60 book pages, turn the HTML into clean, schema-checked JSON, keep the run alive even if one page fails, and finish with an honest report of what happened.

The underlying idea is that scraping is not simply "open a page and copy the text" — it is a chain of small, provable steps:

| Step | Question It Answers | Proof |
|---|---|---|
| Classify | May I automate this site? | A note in the README |
| Fetch | Did the page really arrive? | Saved HTML + status 200 |
| Extract | Which parts do I need? | Raw text fields |
| Normalize | How does `"£51.77"` become a number? | Clean values, absolute URLs |
| Validate | Is every record safe to store? | Schema check; bad records set aside |
| Store | Can another program use it? | `books.json` |
| Report | Did the run actually work? | A few honest numbers |

Three habits run through the whole assignment:

- **Check before you collect** — classify the target first.
- **Be a polite guest** — identify yourself, go slowly, and never hammer the site.
- **Trust nothing you scraped** — web pages are untrusted input until validated.

---

## Tasks

The work is divided into seven required stages, completed in order, with each stage ending in a checkpoint and a commit:

1. **Check before you collect** — confirm that Books to Scrape is a practice sandbox, check `robots.txt`, and write a target-classification note in the README.

2. **Fetch once, cache once** — download catalogue page 1 with a real user-agent, a timeout, and a status check; cache it so re-runs do not unnecessarily hit the site.

3. **Find all three pages** — parse the cached HTML, follow the site's own "next" link through all three catalogue pages, and collect and deduplicate all 60 book URLs.

4. **Extract the raw records** — visit each of the 60 book pages and pull eight raw fields per book:
   - title
   - URL
   - price text
   - availability
   - rating
   - description
   - source page
   - fetch time

5. **Clean it, check it, store it** — normalize price text into a number, validate every record against a schema, write valid records to `books.json`, and write rejected records to `errors.json`.

6. **Survive failures, report the run** — handle each page independently so one broken page does not take down the entire run; finish with a `run-report.json` containing honest run statistics.

7. **Publish the evidence** — push the project to a public repository with a README that a stranger can run in five minutes. The README includes target classification, run instructions, schema, politeness rules, a real run report, a limitation, and an ethics note.

### Optional Bonus — The AI Rematch

The optional bonus stage asks you to prompt an AI to rebuild the same pipeline from a description and then compare its output against your own implementation — what it did better, what it missed, and what the original prompt failed to specify.

---

## What I Built

| | |
|---|---|
| **Lane** | Python 3.10+ — `requests`, `BeautifulSoup4`, `Pydantic` |
| **Target** | `books.toscrape.com` — first 3 catalogue pages, 60 books |
| **`robots.txt`** | Requested once → **404 Not Found**. No robots rules were available. The scraper was still limited to the sandbox's intended scope: three catalogue pages and one polite pass. |
| **Output** | `output/books.json`, `output/errors.json`, `output/run-report.json` |

The pipeline runs with one command. It fetches each page, reads from cache on repeat runs, extracts the eight raw fields per book, normalizes prices and URLs, validates every record with Pydantic, writes the results, and finishes with a run report.

A deliberately broken URL was added to the book list to prove that one bad page does not take down the entire run. The successful records are still written to `books.json`, while the failure is recorded in `errors.json` and reflected in the run report.

> I will not reuse this code on another site without checking its rules and terms first.

---

## Quick Start

```bash
git clone https://github.com/Abdul-Ahad11/polite-scraper.git

cd polite-scraper/scraper

python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
# venv\Scripts\activate

pip install -r requirements.txt

python src/main.py
```

Re-running the command does not create duplicate records. Previously downloaded pages are read from the cache instead of being fetched again.

---

## Record Schema

| Field | Type | Notes |
|---|---|---|
| `title` | `str` | Required |
| `product_url` | `HttpUrl` | Required — canonical identity of the record |
| `price_text` | `str` | Required — original price text |
| `price_gbp` | `float` | Required — numeric price parsed from `price_text` |
| `availability_text` | `str` | Required |
| `rating_text` | `str` | Required |
| `description` | `str \| null` | Optional — `null` when the page has no description; never invented |
| `source_page` | `HttpUrl` | Required — provenance of the record |
| `fetched_at` | `str` | Required — ISO 8601 timestamp |

Records are deduplicated using `product_url`.

Records that fail validation are written to `errors.json` with the reason for rejection and are never written to `books.json`.

---

## Politeness Rules

- **User-Agent:** Every request identifies itself:

  `FlyRankInternship-A9/1.0 (+https://github.com/Abdul-Ahad11/polite-scraper)`

- **Timeout:** Every request has a timeout so the scraper does not hang indefinitely.

- **Delay:** At least 500 ms between real requests. Cache hits do not add a delay.

- **Cache:** Every successfully fetched page is saved on the first request. Development re-runs read the saved copy from the cache.

- **Retries:** `5xx` responses and timeouts receive one retry. `404` and `403` responses are not retried.

---

## Sample Run Report

The following section should contain the **actual contents of `output/run-report.json` from a real run**.

```json
PASTE THE ACTUAL CONTENT OF output/run-report.json HERE
```

---

## Why No Browser Was Needed

The book data is already present in the HTML returned by the server. Nothing required for this assignment is rendered client-side with JavaScript.

Therefore, a headless browser would add additional complexity and resource usage without providing additional data.

---

## Ethics Note

Use an official API instead of scraping whenever one exists.

Never bypass logins, paywalls, authentication, or explicit access restrictions.

Collect only the information that is necessary and use a low, respectful request rate.

This project targets a single public practice sandbox built specifically for scraping practice. Nothing in this implementation is assumed to be valid for another website.

---

## Known Limitation

The retry mechanism is limited to one fixed-wait retry rather than using full exponential backoff.

---

## Project Structure

```text
polite-scraper/
└── scraper/
    ├── cache/
    ├── output/
    │   ├── books.json
    │   ├── errors.json
    │   └── run-report.json
    ├── src/
    │   └── main.py
    ├── README.md
    ├── requirements.txt
    └── .gitignore
```

---

## Repository

[GitHub Repository](https://github.com/Abdul-Ahad11/polite-scraper)

---

Built for **FlyRank Internship — Backend Track — Week 5 — Assignment A9**.
