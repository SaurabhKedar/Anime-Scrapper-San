import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import json
import os
import requests

# Ask user for anime name
search_query = input("Enter anime name to search: ").lower()

# Extract first character and determine searchId
first_char = search_query[0].lower() if search_query else ''
print(first_char)

if 'a' <= first_char <= 'z':
    searchId = first_char.upper()
else:
    searchId = 'hash'
print(searchId)

# Launch undetected Chrome
options = uc.ChromeOptions()
options.add_argument('--headless=new')  
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36")

baseUrl = 'https://animepahe.ru'

driver = uc.Chrome(version_main=135, options=options)
driver.get(baseUrl + "/anime")

# Wait for the page to fully load JS content
time.sleep(5)  # adjust based on your network speed

# Parse content
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

# Extract anime list containers with class
#animeList = soup.find_all('div', class_ = 'tab-content')

# # Store all inner div IDs
# all_inner_ids = []

# for section in animeList:
#     inner_divs = section.find_all('div', id=True)  # only divs with 'id' attribute
#     ids = [div['id'] for div in inner_divs]
#     all_inner_ids.extend(ids)

# print(all_inner_ids)

id_div_dict = {}

div = soup.find('div', id=searchId)

anime_data_list = []
anchor_tags = div.find_all('a', href=True, title=True)

for anchor in anchor_tags:
        anime_data = {
            'AnimeName': anchor.get_text(strip=True),
            'Link': anchor['href']
        }
        anime_data_list.append(anime_data)
        id_div_dict[searchId] = anime_data_list
        
#print(id_div_dict)

#Optional 
# Get current folder path
# curr_dir_path = os.path.dirname(os.path.abspath(__file__))

# # Define file path
# json_file_path = os.path.join(curr_dir_path, "anime_data.json")

# # Write dictionary to JSON file
# with open(json_file_path, "w", encoding="utf-8") as f:
#     json.dump(id_div_dict, f, ensure_ascii=False, indent=4)

# print(f"Anime data saved to: {json_file_path}")


requiredAnime = { }
# Search through the dictionary
for key, anime_list in id_div_dict.items():
    for anime in anime_list:
        if anime["AnimeName"].lower() == search_query:
            requiredAnime = anime
            break  # Breaks out of inner loop
    if requiredAnime:
        break  # Breaks out of outer loop if found

print(requiredAnime)

driver.quit()

