import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "http://quotes.toscrape.com/"

def scrape_quotes(pages=1):
    quotes_data = []

    for page in range(1, pages + 1):
        url = f"{BASE_URL}page/{page}/"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]

            quotes_data.append({
                "Quote": text,
                "Author": author,
                "Tags": ", ".join(tags)
            })

    return quotes_data

def save_to_csv(data, filename="quotes.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f" Data saved to {filename}")

if __name__ == "__main__":
    scraped_data = scrape_quotes(pages=3)  # scrape first 3 pages
    save_to_csv(scraped_data)
