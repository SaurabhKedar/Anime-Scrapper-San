from fetch_all import fetch_all_anime
from fetch_specific import fetch_specific_anime

# Menu-based controller for anime scraper
def main():
    print("Choose an option:")
    print("1. Fetch all anime links")
    print("2. Fetch only specific anime by name")
    
    # Ask user to choose an option
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        fetch_all_anime()  # Call full scraper
    elif choice == "2":
        fetch_specific_anime()  # Call specific anime scraper
    else:
        print("Invalid choice. Please enter 1 or 2.")

# Entry point
if __name__ == "__main__":
    main()
