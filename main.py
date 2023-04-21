import requests
from bs4 import BeautifulSoup
import datetime
import time
import webbrowser
import os

# Constants
AGENDA_URL = "https://www.adkami.com/agenda"
NYAA_SEARCH_URL = "https://nyaa.si/?f=0&c=0_0&q={}"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
BLACKLIST_FILE = "blacklist.txt"

# Functions
def create_blacklist_file():
    if not os.path.exists(BLACKLIST_FILE):
        open(BLACKLIST_FILE, "w").close()
        print(f"{BLACKLIST_FILE} file created.")

def is_in_blacklist(anime_title):
    with open(BLACKLIST_FILE, "r") as f:
        blacklist = f.read().splitlines()
        return anime_title in blacklist

def search_on_nyaa(title, episode):
    # Merge the title and episode number into a single search query
    search_query = f"{title} vostfr"

    # Open the search page on nyaa.si in a new tab
    webbrowser.open_new_tab(NYAA_SEARCH_URL.format(search_query))
    time.sleep(1)

# Check if the blacklist file exists and create it if it doesn't
create_blacklist_file()

# Set the headers for the requests
headers = {
    "User-Agent": USER_AGENT
}

# Make a request to the agenda page
response = requests.get(AGENDA_URL, headers=headers)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the anime listings that were released today
anime_listings = soup.find_all("div", {"class": "col-12 episode"})
today = datetime.date.today()

# Get the title and episode number of each anime that was released today
anime_info = []
for listing in anime_listings:
    date_hour_span = listing.find("span", {"class": "date_hour"})
    if date_hour_span is not None:
        # Convert the data-time attribute to a Unix timestamp
        unix_timestamp = int(date_hour_span["data-time"])
        release_date = datetime.datetime.utcfromtimestamp(unix_timestamp).date()
        if release_date == today:
            title = listing.find("p", {"class": "title"}).text
            episode_info = listing.find("p", {"class": "epis"}).text
            anime_info.append((title, episode_info))

# Print out the list of anime that were released today along with their episode numbers
print("Anime that came out today:")
for title, episode_info in anime_info:
    # Remove the "Episode" string from the episode info
    episode_info = episode_info.replace("Episode ", "")
    
    # Check if the anime is in the blacklist
    if not is_in_blacklist(title):
        print("O - {} (Episode {})".format(title, episode_info))
        # Search on nyaa.si for the anime
        search_on_nyaa(title, episode_info)
    else:
        print(f"X - {title} (Episode {episode_info})")
