import os
import time
import json
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from pydantic import BaseModel

def clean_price(price_text):
    return float(price_text.replace("£", "").strip())

class BookRecord(BaseModel):
    title: str
    product_url: str
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    description: str | None = None
    source_page: str
    fetched_at: str

URL="https://books.toscrape.com/catalogue/page-1.html"
headers = {
    "User-Agent": "FlyRankInternship-A9/1.0 (+https://github.com/Abdul-Ahad11/polite-scraper)"
}
CACHE_DIR="/Users/abdulahad/Downloads/polite-scraper/scraper/cache"
current_url=URL
page_num=1
book_urls = []
book_sources = {}
records=[]
errors=[]
while True:
    cache_file=os.path.join(
        CACHE_DIR,
        f"catalogue-page-{page_num}.html"
    )
    print("processing :" , current_url)
    if os.path.exists(cache_file):
        print("Cache HIT")
        with open(cache_file, "r", encoding="utf-8") as file:
            html = file.read()
        size = os.path.getsize(cache_file)
        print(f"Response size: {size} bytes")

    else:
        response = requests.get(current_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"fetch failed , {response.status_code}")
            break
        else:
            with open(cache_file, "w", encoding=("utf-8")) as file:
                file.write(response.text)
                html = response.text
                print(f"fetch success , {response.status_code}")
                print(f"response size , {len(response.content)} bytes")
                time.sleep(0.5)
    print("cache file" , cache_file)
    soup = BeautifulSoup(html, "html.parser")

    books = soup.find_all("article", class_="product_pod")
    print(f"Total books : {len(books)}")


    for book in books:
        link = book.find("a")
        href = link["href"]
        full_url = urljoin(current_url, href)
        book_urls.append(full_url)
        book_sources[full_url] = current_url
    print(f"Discovered , {len(book_urls)}")
    for url in book_urls:
        print(url)

    next_page = soup.find("li", class_="next")

    if page_num == 3:
        print("Reached page 3. Stopping.")
        break

    if next_page:
        next_link = next_page.find("a")
        next_href = next_link["href"]

        print("current url:", current_url)
        print("next href:", next_href)

        next_url = urljoin(current_url, next_href)
        print("next url:", next_url)
        print("next page", next_url)

        current_url=next_url
        page_num+=1
    else:
        print("no next page....")
        break


unique_urls = list(dict.fromkeys(book_urls))
DETAIL_CACHE_DIR = os.path.join(CACHE_DIR, "details")
os.makedirs(DETAIL_CACHE_DIR, exist_ok=True)

print(f"discovered={len(book_urls)}")
print(f"unique_urls={len(unique_urls)}")


for product_url in unique_urls:

    print("\n-----------------------------")
    print("Processing:", product_url)

    book_id = product_url.split("_")[-1].split("/")[0]
    print("Book ID:", book_id)

    detail_cache_file = os.path.join(
        DETAIL_CACHE_DIR,
        f"{book_id}.html"
    )
    metadata_file = os.path.join(
        DETAIL_CACHE_DIR,
        f"{book_id}.json"
    )
    print("Cache file:", detail_cache_file)
    if os.path.exists(detail_cache_file):

        print("CACHE HIT")

        with open(detail_cache_file, "r", encoding="utf-8") as file:
            html = file.read()

        if os.path.exists(metadata_file):
            with open(metadata_file, "r", encoding="utf-8") as file:
                metadata = json.load(file)

            fetched_at = metadata["fetched_at"]
        else:
            fetched_at = None
        print(f"Response size: {len(html.encode('utf-8'))} bytes")
    else:
        print("FETCH")
        response = requests.get(
            product_url,
            headers=headers,
            timeout=10
        )
        print("Status:", response.status_code)
        if response.status_code != 200:
            print("Fetch failed. Skipping this book.")
            continue
        html = response.content.decode("utf-8")

        with open(detail_cache_file, "w", encoding="utf-8") as file:
            file.write(html)
        fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        metadata = {
            "fetched_at": fetched_at
        }
        with open(metadata_file, "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=2)
        print(f"Response size: {len(response.content)} bytes")
        time.sleep(0.5)
    soup = BeautifulSoup(html, "html.parser")
    title_element = soup.find("h1")
    title_text = title_element.get_text(strip=True)
    print("Title:", title_text)
    # extrect price
    price_element = soup.find("p", class_="price_color")
    price_text = price_element.get_text(strip=True)
    print("Price:", price_text)
    # availability
    availability_element = soup.find(
        "p",
        class_="instock availability"
    )
    availability_text = availability_element.get_text(
        " ",
        strip=True
    )
    print("Availability:", availability_text)
    #rating
    rating_element = soup.find(
        "p", class_="star-rating"
    )
    rating_text = rating_element.get("class")[1]
    print("Rating:", rating_text)
    #discription
    product_description = soup.find("div", id="product_description")

    if product_description:
        description_tag = product_description.find_next_sibling("p")

        if description_tag:
            description = description_tag.get_text(" ", strip=True)
        else:
            description = None
    else:
        description = None
#retrive source page
    source_page = book_sources[product_url]
    print("Source page:", source_page)
    price_gbp=clean_price(price_text)
    record = {
        "title": title_text,
        "product_url": product_url,
        "price_text": price_text,
        "price_gbp":price_gbp,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at
    }
    try:
        validated_record = BookRecord(**record)
        records.append(validated_record.model_dump())
        print("Record valid.")
    except Exception as error:
        print("Record invalid:", error)
        errors.append({
            "product_url": product_url,
            "error": str(error)
        })

print("\n=============================")
print(f"detail_pages={len(records)}")
print("=============================")

#books.json
OUTPUT_DIR = os.path.join(os.path.dirname(CACHE_DIR),"output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
BOOKS_FILE = os.path.join(OUTPUT_DIR,"books.json")
with open(BOOKS_FILE, "w", encoding="utf-8") as file:
    json.dump(records,file,indent=2,ensure_ascii=False
    )
print(f"Saved {len(records)} records to {BOOKS_FILE}")

#error.json
ERRORS_FILE = os.path.join(
    OUTPUT_DIR,
    "errors.json"
)
with open(ERRORS_FILE, "w", encoding="utf-8") as file:
    json.dump(
        errors,
        file,
        indent=2,
        ensure_ascii=False
    )
print(f"Saved {len(records)} records to {BOOKS_FILE}")
print(f"Saved {len(errors)} errors to {ERRORS_FILE}")

if records:
    print(json.dumps(records[0], indent=2, ensure_ascii=False))
