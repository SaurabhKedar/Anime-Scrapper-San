from bs4 import BeautifulSoup
import time
from common import setup_driver
from common import fetch_anime_episodes
from common import prompt_and_save
from common import visit_anime_detail

# Function to search for a specific anime name (case-insensitive partial match)
def fetch_specific_anime():
    # Prompt user to enter anime name to search
    search_query = input("Enter anime name to search (case-insensitive): ").lower()

    # Determine the section ID based on the first character of the search query
    # The website categorizes anime by first letter (A-Z) or 'hash' for others
    first_char = search_query[0].lower() if search_query else ''
    searchId = first_char.upper() if 'a' <= first_char <= 'z' else 'hash'

    print(f"Searching in section: {searchId}")

    # Setup undetected Chrome driver using common.py helper function
    driver = setup_driver()
    BASE_URL = 'https://animepahe.ru'
    driver.get(BASE_URL + "/anime")

    # Wait for page to fully load dynamic JS content (adjust if needed)
    time.sleep(5)

    # Parse the page source HTML with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Find the div corresponding to the search section (A-Z or hash)
    div = soup.find('div', id=searchId)

    anime_data_list = []

    # If the div section exists, extract all anime entries inside it
    if div:
        # Find all anchor tags with href and title attributes within the div
        anchor_tags = div.find_all('a', href=True, title=True)
        for anchor in anchor_tags:
            anime_data = {
                'AnimeName': anchor.get_text(strip=True),  # Clean anime name text
                'Link': anchor['href']                     # URL link to the anime page
            }
            anime_data_list.append(anime_data)
 
    # List to hold all anime that match the user's search query
    matching_anime = []

    # Loop through extracted anime to find matches
    for anime in anime_data_list:
        anime_title_lower = anime["AnimeName"].lower()

        # CASE 1: User pressed Enter (no input), and we're in the 'hash' section
        if search_query == "" and searchId == "hash":

            # Include if title is empty OR first character is not a letter
            if anime_title_lower == "" or not anime_title_lower[0].isalpha():
                matching_anime.append(anime)

        # CASE 2: User entered some text — normal substring or full match
        elif search_query in anime_title_lower:
            matching_anime.append(anime)

    # If any matches found, display count and details, then prompt to save results
    if len(matching_anime) > 1:
        print(f"\n{len(matching_anime)} matching anime(s) found:\n")
        # Save matching anime to JSON file with the search query as key
        prompt_and_save({f"{search_query}": matching_anime})
    else:
        # No matches found, inform the user to try again with a different keyword
        print("\nNo matching anime found. Try a different keyword.")

    print(matching_anime)
    for anime in matching_anime:
        anime_details = visit_anime_detail(driver, anime) 
        anime_details = fetch_anime_episodes(driver, anime_details);

    # Close the browser session cleanly
    driver.quit()
