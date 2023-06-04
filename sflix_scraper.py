import requests
import csv
from bs4 import BeautifulSoup
import random
import time

base_url = "https://sflix.to/genre/action?page="


num_pages = 6

delay_min = 15
delay_max = 20

movie_details = []

for page in range(1, num_pages + 1):
    url = base_url + str(page)
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        film_name_elements = soup.find_all(class_='film-name')
        movie_names = [element.a.get_text(strip=True) for element in film_name_elements]
        film_information = soup.find_all("div", class_="fd-infor")

        for element in film_information:
            rating_element = element.find(class_='fdi-item')
            rating = rating_element.get_text(strip=True)

            quality_element = element.find('strong')
            quality = quality_element.get_text(strip=True)

            release_year_element = element.find_all(class_='fdi-item')[-1]
            release_year = release_year_element.get_text(strip=True)

            movie_details.append({'rating': rating, 'quality': quality, 'release_year': release_year})


        csv_file = f"movie_details_page_{page}.csv"

        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Movie Name', 'Rating', 'Quality', 'Release Year'])
            writer.writeheader()
            for movie_name, details in zip(movie_names, movie_details):
                writer.writerow({'Movie Name': movie_name, 'Rating': details['rating'], 'Quality': details['quality'], 'Release Year': details['release_year']})

        print("Movie details for page", page, "saved to", csv_file)


        delay = random.randint(delay_min, delay_max)
        time.sleep(delay)
