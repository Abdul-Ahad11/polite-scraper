import os
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests


URL="https://books.toscrape.com/catalogue/page-1.html"
headers = {
    "User-Agent": "FlyRankInternship-A9/1.0 (+https://github.com/Abdul-Ahad11/polite-scraper)"
}
CACHE_DIR="/Users/abdulahad/Downloads/polite-scraper/scraper/cache"
current_url=URL
page_num=1
book_urls = []
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


unique_urls = set(book_urls)

print(f"discovered={len(book_urls)}")
print(f"unique_urls={len(unique_urls)}")