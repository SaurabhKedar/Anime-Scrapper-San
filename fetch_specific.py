from bs4 import BeautifulSoup
import time
from common import setup_driver
from common import prompt_and_save

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
    baseUrl = 'https://animepahe.ru'
    driver.get(baseUrl + "/anime")

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

        # Check if user query exactly matches or is contained within the anime name (partial match)
        if search_query == anime_title_lower or search_query in anime_title_lower:
            matching_anime.append(anime)

    # If any matches found, display count and details, then prompt to save results
    if matching_anime:
        print(f"\n{len(matching_anime)} matching anime(s) found:\n")
        # Save matching anime to JSON file with the search query as key
        prompt_and_save({f"{search_query}": matching_anime})

        # Print each matched anime's details on console
        for anime in matching_anime:
            print(anime)
    else:
        # No matches found, inform the user to try again with a different keyword
        print("\nNo matching anime found. Try a different keyword.")

    # Close the browser session cleanly
    driver.quit()
