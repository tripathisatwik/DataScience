import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://web-scraping.dev/products"

def scrape_page(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def parse_products(soup):
    products = []
    # On /products the structure: each product listed under div.product
    for card in soup.select("div.product"):
        title = card.select_one("h3").get_text(strip=True)
        # There is no explicit description/variety/before/after price on listing page.
        # So we need to open each product’s detail page.
        link = card.select_one("h3 a")["href"]
        # full product URL
        product_url = f"https://web-scraping.dev/{link.split('/')[-1]}"
        
        # fetch detail page
        detail_soup = scrape_page(product_url)
        desc = detail_soup.select_one("div.description").get_text(strip=True)
        
        # The price line may contain either a single price or a "from $X" style
        price_text = detail_soup.select_one("div.product-pricing").get_text(strip=True)
        before = ""
        after = ""
        # Example price_text: "$9.99 from $12.99" or "$4.99"
        parts = price_text.split("from")
        if len(parts) == 2:
            after = parts[0].strip()
            before = parts[1].strip()
        else:
            after = parts[0].strip()
        
        # Variety/variants — optional
        variety_elem = detail_soup.select_one("div.variants")
        variety = variety_elem.get_text(strip=True) if variety_elem else ""
        
        products.append({
            "title": title,
            "description": desc,
            "variety_name": variety,
            "before_price": before,
            "after_price": after
        })
        # polite delay
        time.sleep(1)
    return products

def main():
    all_products = []
    # First page
    soup = scrape_page(BASE_URL)
    all_products += parse_products(soup)

    # Pagination: find links to other pages
    page_links = soup.select("ul.paging li a")
    for a in page_links:
        href = a.get("href")
        full = f"https://web-scraping.dev{href}"
        soup2 = scrape_page(full)
        all_products += parse_products(soup2)

    # Write to CSV
    with open("bs_products.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["title", "description", "variety_name", "before_price", "after_price"])
        writer.writeheader()
        writer.writerows(all_products)

    print(f"Saved {len(all_products)} products to bs_products.csv")

if __name__ == "__main__":
    main()
