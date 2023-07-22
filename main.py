import csv
import requests
from bs4 import BeautifulSoup
from time import sleep


def scrape_product_listing_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'data-asin': True, 'data-component-type': 's-search-result'})

    data = []
    for product in products:
        product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
        product_name = product.find('span', {'class': 'a-size-medium'}).text.strip()
        product_price = product.find('span', {'class': 'a-offscreen'}).text.strip()
        rating_element = product.find('span', {'class': 'a-icon-alt'})
        rating = rating_element.text.split()[0] if rating_element else 'Not available'
        num_reviews = product.find('span', {'class': 'a-size-base'}).text.split()[0]

        data.append([product_url, product_name, product_price, rating, num_reviews])

    return data


def scrape_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting product details
    asin_element = soup.find('th', string='ASIN')
    asin = asin_element.find_next_sibling('td').text.strip() if asin_element else 'Not available'

    product_description_element = soup.find('div', {'id': 'productDescription'})
    product_description = product_description_element.text.strip() if product_description_element else 'Not available'

    manufacturer_element = soup.find('a', {'id': 'bylineInfo'})
    manufacturer = manufacturer_element.text.strip() if manufacturer_element else 'Not available'

    return [asin, product_description, manufacturer]


def main():
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
    output_filename = 'amazon_product_data.csv'
    num_pages = 20
    max_products = 200
    products_scraped = 0

    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description',
                         'ASIN', 'Product Description', 'Manufacturer'])

        for page in range(1, num_pages + 1):
            if products_scraped >= max_products:
                break

            url = base_url + str(page)
            product_data = scrape_product_listing_page(url)
            print(f"Scraped page {page}/{num_pages}")

            for product in product_data:
                if products_scraped >= max_products:
                    break

                product_url = product[0]
                description, *details = scrape_product_details(product_url)
                product.extend([description, *details])
                writer.writerow(product)
                products_scraped += 1
                sleep(1)  # Sleep for a short period to avoid overwhelming the server


if __name__ == "__main__":
    main()
