import requests
from bs4 import BeautifulSoup
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

def scrape_all_pages(base_url): 
    with open('carlist_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(['Model', 'Brand', 'Year', 'Price', 'Mileage', 'Transmission'])
            
            page = 1
            for i in range(0, 100): 
                print(f"Scraping page {page}...")
                url = f"{base_url}?page_number={page}"

                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'lxml')
                    cars = soup.find_all('div', class_="grid grid--full cf")  # Adjust class name as per actual HTML
                    
                    if not cars:  # Break if there is nothing scraped (end of page)
                        print("No more pages to scrape.")
                        break

                    for car in cars:                        
                        name = car.find('a', class_ = "ellipsize js-ellipsize-text").text
                        parts = name.split()
                        year = parts[0]
                        brand = parts[1]

                        price = car.find('div', class_="listing__price delta weight--bold")
                        if not price: # if price can't be found, car is on sale due to carlist's promotion - data will not be collected 
                            continue
                        
                        price = price.text.split()
                        price = price[1]

                        transmission = car.find('div', class_ = "item push-quarter--ends").text.strip()
                        mileage = car.find('div', class_ ="item push-quarter--ends soft--right push-quarter--right").text.strip()
                        model = car.find('div', class_="listing__rating-model text--truncate soft-quartter--right")
                        if model is not None:
                            model = model.text
                        else:
                            continue

                        # save to csv file
                        writer.writerow([model, brand, year, price, mileage, transmission])
                    page += 1

                else:
                    print(f"Failed to fetch page: {response.status_code}")

base_url = "https://www.carlist.my/used-cars-for-sale/malaysia"
scrape_all_pages(base_url)


