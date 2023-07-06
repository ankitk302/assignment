import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape additional information from a product URL
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the description
    description = soup.find("div", {"id": "productDescription"})
    description = description.get_text(strip=True) if description else ""

    # Extract the ASIN
    asin = soup.find("th", string="ASIN").find_next_sibling("td").get_text(strip=True) if soup.find("th", string="ASIN") else ""

    # Extract the product description
    product_desc = soup.find("h2", string="Product Description").find_next_sibling("div").get_text(strip=True) if soup.find("h2", string="Product Description") else ""

    # Extract the manufacturer
    manufacturer = soup.find("a", {"id": "bylineInfo"}).get_text(strip=True) if soup.find("a", {"id": "bylineInfo"}) else ""

    return description, asin, product_desc, manufacturer

# Specify the base URL and number of product URLs to scrape
base_url = "https://www.amazon.in/s"
search_query = "bags"
num_pages = 20
products_per_page = 10

# Create a list to store the scraped data
product_urls = []
products = []

# Loop through each page
for page in range(1, num_pages + 1):
    # Prepare the parameters for the URL
    params = {
        "k": search_query,
        "crid": "2M096C61O4MLT",
        "qid": "1653308124",
        "sprefix": "ba%2Caps%2C283",
        "ref": f"sr_pg_{page}"
    }

    # Send a GET request to the URL
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the product listings on the page
    listings = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Loop through each listing and extract the product URLs
    for listing in listings:
        # Extract the product URL
        product_url = listing.find("a", {"class": "a-link-normal s-no-outline"})["href"]
        product_url = "https://www.amazon.in" + product_url

        # Add the product URL to the list
        product_urls.append(product_url)

# Loop through each product URL and scrape the details
for url in product_urls[:200]:  # Limiting to 200 URLs for demonstration purposes
    description, asin, product_desc, manufacturer = scrape_product_details(url)

    # Append the scraped data to the list
    products.append({
        "Product URL": url,
        "Description": description,
        "ASIN": asin,
        "Product Description": product_desc,
        "Manufacturer": manufacturer
    })

# Export the scraped data to a CSV file
output_file = "product_data.csv"
fieldnames = ["Product URL", "Description", "ASIN", "Product Description", "Manufacturer"]

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products)

print ("ScrapingThe code above scrapes the additional information"  "product_data.csv")



