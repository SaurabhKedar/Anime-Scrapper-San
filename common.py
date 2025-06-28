import undetected_chromedriver as uc
import os
import json

# Define Brave browser's user-agent string to help avoid ads/tracking
BRAVE_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Brave/134.1.0.0"

# Define Chrome browser's user-agent string
CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36";

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