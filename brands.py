import json

import requests
from bs4 import BeautifulSoup


def fetch_brands(page):
    url = f'https://www.car.info/en-se/ajax-get-brands-list?page={page}&search_text=&country=show_all&order=owner_count&view=list_cards'
    print(f'Fetch Page: {page} \nFetch URL:{url}')
    response = requests.get(url)

    if response.status_code == 200:
        response_data = json.loads(response.text)

        brand_recs_html = response_data.get("brand_recs_html", "")

        soup = BeautifulSoup(brand_recs_html, 'html.parser')

        brand_items = soup.select('.brand_item')
        brands = []

        # Iterate over each brand item
        for item in brand_items:
            # Extract brand information
            brand = dict()
            brand['Name'] = item.select_one('.brand_name').text.strip()
            brand['URL'] = item.select_one('.brand_name')['href']
            brand['Country'] = item.select_one('.tooltip_topleft img')['alt']
            brand['CountryCode'] = item.select_one('.tooltip_topleft')['data-country']
            brand['CountryLogoURL'] = item.select_one('.tooltip_topleft img')['src']

            # Check if brand logo image exists before accessing its attributes
            brand_logo_image = item.select_one('.brand_logo_image')
            if brand_logo_image:
                brand['BrandLogoURL'] = brand_logo_image['style'].replace("background-image: url('", "").replace("');",
                                                                                                                 "")
            else:
                brand['BrandLogoURL'] = None

            brand['Year'] = item.select_one('.brand_year').text.strip()  # Extract brand year

            # Append the brand data to the list
            brands.append(brand)

        return brands
    else:
        print("Failed to retrieve data for page", page)
        return []


def main():
    all_brands = []
    for page in range(0, 37):  # Fetch data from pages 0 to 36
        brands_on_page = fetch_brands(page)
        all_brands.extend(brands_on_page)

    # Convert the list of brands to JSON format
    json_data = json.dumps(all_brands, indent=4)

    # Write the JSON data to a file
    with open('brands.json', 'w') as file:
        file.write(json_data)

    print("Data saved to brands.json")


if __name__ == '__main__':
    main()
