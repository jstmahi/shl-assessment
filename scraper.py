import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"

def get_product_details(product_url):
    try:
        response = requests.get(product_url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Unknown"
        
        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag['content'] if description_tag else ""
        
        if not description:
            p_tag = soup.find('p')
            if p_tag:
                description = p_tag.get_text(strip=True)

        return {
            "name": title,
            "url": product_url,
            "description": description,
            "adaptive_support": "No",
            "remote_support": "Yes",
            "duration": 30,
            "test_type": ["Knowledge & Skills"] 
        }
    except Exception as e:
        print(f"Error scraping {product_url}: {e}")
        return None

def scrape_catalog():
    print("Starting scraper... this may take a few minutes.")
    products = []
    
    response = requests.get(BASE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/view/' in href:
            full_url = href if href.startswith('http') else f"https://www.shl.com{href}"
            links.add(full_url)
    
    print(f"Found {len(links)} potential products. scraping details...")
    
    count = 0
    for link in links:
        data = get_product_details(link)
        if data:
            products.append(data)
            count += 1
            print(f"Scraped {count}: {data['name']}")
    
    df = pd.DataFrame(products)
    df.to_csv("shl_products.csv", index=False)
    print("Scraping complete. Saved to shl_products.csv")

if __name__ == "__main__":
    scrape_catalog()
