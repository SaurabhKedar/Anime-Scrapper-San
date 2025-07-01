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
    if len(matching_anime) > 0:
        print(f"\n{len(matching_anime)} matching anime(s) found:\n")

        while True:
            # Print numbered list of matched anime titles
            for idx, anime in enumerate(matching_anime, start=1):
                print(f"{idx}. AnimeName: {anime['AnimeName']}")

            # Ask user to select one by number
            try:
                choice = int(input("\nEnter the number of the anime you want to proceed with: "))
                if 1 <= choice <= len(matching_anime):
                    selected_anime = matching_anime[choice - 1]
                    print(f"\nYou selected: {selected_anime['AnimeName']}")
                    
                    #Fetch selected anime and their episodes
                    anime_details = visit_anime_detail(driver, selected_anime)
                    anime_details = fetch_anime_episodes(driver, anime_details)
                    print(anime_details)

                    # Ask if they want to select another
                    again = input("\nDo you want to choose another anime from the list? (yes/no): ").strip().lower()
                    if again != "yes":
                        print("Exiting selection.")
                        break
            except ValueError:
                print("Please enter a valid number.\n")
    else:
        # No matches found, inform the user to try again with a different keyword
        print("\nNo matching anime found. Try a different keyword.")

    # Close the browser session cleanly
    driver.quit()
