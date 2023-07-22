# product_listing
This Python project is a web scraper that collects product data from multiple pages of Amazon's search results for bags. The scraper gathers product URLs, names, prices, ratings, and the number of reviews from the search result pages. Then, for each product URL, the script visits the individual product pages to extract additional information, such as ASIN, product description, and manufacturer.

The project's main features are:

Scraping Product Listing Pages:

The function scrape_product_listing_page fetches product data from multiple pages by utilizing web scraping techniques.
It extracts product URLs, names, prices, ratings, and the number of reviews from the search results.
Scraping Individual Product Pages:

The function scrape_product_details accesses each product's unique URL to collect additional information.
It extracts the ASIN (Amazon Standard Identification Number), product description, and manufacturer of each product.
Limiting the Data and Exporting to CSV:

The main function main coordinates the entire scraping process, ensuring the collection of information from a maximum of 200 products.
The scraped data is exported to a CSV file named "amazon_product_data.csv."
The script sleeps for a short time between requests to avoid overwhelming the server.
