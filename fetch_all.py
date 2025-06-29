from bs4 import BeautifulSoup
import time
from common import setup_driver  # Import shared function to set up undetected Chrome driver
from common import prompt_and_save  # Import shared function to prompt user and save data to JSON
from common import  visit_anime_detail #Fetch Anime Details
from common import fetch_anime_episodes #fetch anime episodes

# Function to scrape all anime from the site and optionally save the data to a JSON file
def fetch_all_anime():
    # Initialize undetected Chrome driver
    driver = setup_driver()

    BASE_URL = 'https://animepahe.ru'

    # Navigate to the main anime listing page
    driver.get(BASE_URL + "/anime")

    # Wait for dynamic JavaScript content to load fully (adjust time as needed)
    time.sleep(5)

    # Parse the rendered HTML content with BeautifulSoup for easy scraping
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Find all 'div' elements with class 'tab-content' 
    # Each 'tab-content' div contains sections categorized by letter or symbol
    animeList = soup.find_all('div', class_='tab-content')

    # This list will store all inner div IDs like 'A', 'B', 'C', ... or 'hash' 
    all_inner_ids = []

    # Loop through each 'tab-content' section to extract inner divs that have IDs
    for section in animeList:
        inner_divs = section.find_all('div', id=True)  # Find only divs with an 'id' attribute
        ids = [div['id'] for div in inner_divs]  # Extract the value of each id attribute
        all_inner_ids.extend(ids)  # Add them to the cumulative list

    # Dictionary to hold anime data categorized by section ID (e.g. 'A', 'B', 'hash')
    id_div_dict = {}

    # Iterate over each section ID found on the page
    for id_value in all_inner_ids:
        div = soup.find('div', id=id_value)  # Find the div corresponding to this ID

        # If div is not found (unlikely but possible), skip to next
        if div is None:
            continue

        anime_data_list = []

        # Extract all anchor tags with href and title attributes within this section
        anchor_tags = div.find_all('a', href=True, title=True)

        # Loop through each anchor tag to extract anime name and its link
        for anchor in anchor_tags:
            anime_data = {
                'AnimeName': anchor.get_text(strip=True),  # Clean text of anime name
                'Link': anchor['href']                      # Link to anime page
            }
            anime_data_list.append(anime_data)  # Add to the list for this section

        # Store the list of anime for this section ID in the dictionary
        id_div_dict[id_value] = anime_data_list

    # Print a summary of how many anime entries were found in each section
    for id_key, anime_list in id_div_dict.items():
        print(f"ID: {id_key} -> {len(anime_list)} anime(s)")

    # Prompt the user if they want to save the collected data and save if requested
    prompt_and_save(id_div_dict)

    for section_id, anime_list in id_div_dict.items():
        print(f"\nSection ID: {section_id} -> {len(anime_list)} anime(s)")

        for anime in anime_list:
            anime_details = visit_anime_detail(driver, anime) 
            anime_details = fetch_anime_episodes(driver, anime);
            print(anime_details)

    # Close the browser session cleanly
    driver.quit()
