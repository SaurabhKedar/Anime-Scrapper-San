import undetected_chromedriver as uc
import os
import json
from bs4 import BeautifulSoup
import time

# Define Brave browser's user-agent string to help avoid ads/tracking
BRAVE_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Brave/134.1.0.0"

# Define Chrome browser's user-agent string
CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36";

#Main Anime site url
BASE_URL = 'https://animepahe.ru'

# This function sets up a headless, stealth Chrome driver with custom options
def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')  # Run browser in headless mode
    options.add_argument('--disable-gpu')   # Disable GPU rendering
    options.add_argument('--no-sandbox')    # For Linux sandboxing issues
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')  # Prevent popups
    options.add_argument(f"user-agent={BRAVE_USER_AGENT}")  # Use Brave user-agent
    return uc.Chrome(version_main=138, options=options)

def save_to_json(data, filename):
    """
    Save the given data (dict or list) to a JSON file.
    
    Parameters:
    - data: The dictionary or list to save.
    - filename: The filename (with extension) to save the data into.
    
    The file will be saved in the same directory as this script.
    """
    if not filename.endswith('.json'):
        raise ValueError("Filename must end with '.json'")
    
    curr_dir_path = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(curr_dir_path, filename)

    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"\nData saved to: {json_file_path}\n")

def prompt_and_save(data):
    """
    Ask the user if they want to save the data.
    If yes, prompt for filename and save using save_to_json().
    """
    save_choice = input("\nDo you want to save the result to a JSON file? (yes/no): ").strip().lower()

    if save_choice in ['yes', 'y']:
        filename = input("Enter a filename (with .json extension): ").strip()
        if not filename.endswith('.json'):
            filename += '.json'
        save_to_json(data, filename)
    else:
        print("Okay, data will not be saved.")


# Function to visit a specific anime's detail page and extract basic info
def visit_anime_detail(driver, anime_data):
    """
    Visits the anime detail page and extracts:
    - Name
    - Poster URL
    - Original anime link

    Returns:
        dict: {
            "Name": <anime title>,
            "Link": <original anime relative URL>,
            "Poster": <poster image URL>
        }
    """
    full_url = BASE_URL + anime_data["Link"]
    driver.get(full_url)
    time.sleep(5)  # Wait for content to load

    soup = BeautifulSoup(driver.page_source, "lxml")

    # Extract anime title
    title_tag = soup.find("h1", class_="user-select-none")
    anime_name = title_tag.span.get_text(strip=True) if title_tag and title_tag.span else anime_data.get("AnimeName", "Unknown")

    # Extract poster image URL
    poster_tag = soup.select_one(".anime-poster a")
    poster_url = poster_tag["href"] if poster_tag else None

    # Return data as JSON-ready dict
    return {
        "Name": anime_name,
        "Link": anime_data["Link"],
        "Poster": poster_url
    }

def fetch_anime_episodes(driver, anime_info):
    """
    Extracts all paginated episode details including:
    - Episode Number
    - Watch Link
    - Duration
    - Snapshot Image

    Args:
        driver: Selenium driver instance
        anime_info: Dictionary containing anime details

    Returns:
        Updated anime_info dict with all episodes in an "Episodes" list
    """
    episodes = []
    page = 1

    while True:
        full_url = f"{BASE_URL}{anime_info['Link']}?page={page}"
        driver.get(full_url)
        time.sleep(3)  # Adjust wait as needed

        soup = BeautifulSoup(driver.page_source, "lxml")
        episode_divs = soup.select("div.episode-wrap")

        if not episode_divs:
            # No more episodes found — stop pagination
            break

        for div in episode_divs:
            try:
                # Episode link
                link_tag = div.select_one("a.play")
                episode_link = BASE_URL + link_tag["href"] if link_tag else None

                # Episode number
                episode_no = div.select_one(".episode-number")
                episode_no = episode_no.get_text(strip=True) if episode_no else "Unknown"

                # Duration
                duration = div.select_one(".episode-duration")
                duration = duration.get_text(strip=True) if duration else "Unknown"

                # Snapshot image
                snapshot_img = div.select_one(".episode-snapshot img")
                snapshot = snapshot_img["src"] if snapshot_img else None

                episodes.append({
                    "Episode No": episode_no,
                    "Link": episode_link,
                    "Duration": duration,
                    "Snapshot": snapshot
                })
            except Exception as e:
                print(f"[Page {page}] Error parsing episode: {e}")
                continue

        print(f"[Page {page}] Fetched {len(episode_divs)} episode(s)")
        page += 1

    anime_info["Episodes"] = episodes
    prompt_and_save(anime_info)
    return anime_info
