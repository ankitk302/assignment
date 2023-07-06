import requests
from bs4 import BeautifulSoup
import csv

# Specify the URL and number of pages to scrape
base_url = "https://www.amazon.in/s"
search_query = "bags"
num_pages = 20

# Create a list to store the scraped data
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

    # Loop through each listing and extract the required information
    for listing in listings:
        # Extract the product URL
        product_url = listing.find("a", {"class": "a-link-normal s-no-outline"})["href"]
        product_url = "https://www.amazon.in" + product_url

        # Extract the product name
        product_name = listing.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).text.strip()

        # Extract the product price
        product_price = listing.find("span", {"class": "a-price-whole"}).text.strip()

        # Extract the rating
        rating = listing.find("span", {"class": "a-icon-alt"}).text.strip()

        # Extract the number of reviews
        num_reviews = listing.find("span", {"class": "a-size-base"}).text.strip()

        # Append the scraped data to the list
        products.append({
            "Product URL": product_url,
            "Product Name": product_name,
            "Product Price": product_price,
            "Rating": rating,
            "Number of Reviews": num_reviews
        })

# Export the scraped data to a CSV file
output_file = "part1product_data.csv"

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"])
    writer.writeheader()
    writer.writerows(products)

print("Scraping complete. Data exported to part1product_data.csv")
