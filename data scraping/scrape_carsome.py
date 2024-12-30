import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def scrape_all_pages(base_url): 
    with open('carsome_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(['Model', 'Brand', 'Year', 'Price', 'Mileage', 'Transmission'])
            
            page = 1
            while True: 
                print(f"Scraping page {page}...")
                url = f"{base_url}?pageNo={page}"

                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'lxml')
                    cars = soup.find_all('div', class_="mod-b-card__footer")  # Adjust class name as per actual HTML
                    
                    if not cars:  # Break if there is nothing scraped (end of page)
                        print("No more pages to scrape.")
                        break

                    for car in cars:
                        name = car.find_all('p')
                        name = " ".join([tag.get_text(strip=True) for tag in name])
                        parts = name.split()
                        year = parts[0]
                        brand = parts[1]
                        model = brand + " " + parts[2]

                        price = car.find('strong').text
                        settings = car.find('div', class_="mod-b-card__car-other")
                        spans = settings.find_all('span', recursive=False)  # Find only top-level spans within the div

                        if len(spans) >= 2:  # Ensure there are at least two spans
                            mileage = spans[0].get_text(strip=True)
                            transmission = spans[1].get_text(strip=True)    
                        else: 
                            mileage, transmission = "NA", "NA"
                            
                        # save to csv file
                        writer.writerow([model, brand, year, price, mileage, transmission])
                    page += 1

                else:
                    print(f"Failed to fetch page: {response.status_code}")

base_url = "https://www.carsome.my/buy-car"
scrape_all_pages(base_url)


