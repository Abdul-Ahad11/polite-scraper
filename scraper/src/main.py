import os
import requests

URL="https://books.toscrape.com/catalogue/page-1.html"
CACHE_FILE = "/Users/abdulahad/Downloads/polite-scraper/scraper/cache/catalogue-page-1.html"

headers = {
    "User-Agent": "FlyRankInternship-A9/1.0 (+https://github.com/Abdul-Ahad11/polite-scraper)"
}
if os.path.exists(CACHE_FILE):
    size = os.path.getsize(CACHE_FILE)
    print("Cache HIT")
    print(f"Response size: {size} bytes")

else:
    response=requests.get(URL , headers=headers , timeout=10)
    if response.status_code != 200:
        print(f"fetch failed , {response.status_code}")
    else:
        with open(CACHE_FILE , "w" , encoding=("utf-8")) as file:
            file.write(response.text)

            print(f"fetch success , {response.status_code}")
            print(f"response size , {len(response.content)} bytes")