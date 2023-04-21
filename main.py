import requests
from bs4 import BeautifulSoup
import datetime
import time
import webbrowser

def search_on_nyaa(title, episode):
    # Merge the title and episode number into a single search query
    search_query = f"{title} {episode_info.replace('Episode ', '')} vostfr"
    
    
    # Open the search page on nyaa.si in a new tab
    webbrowser.open_new_tab(f"https://nyaa.si/?f=0&c=0_0&q={search_query}")
    time.sleep(1)

# Set the URL of the agenda page and make a request
url = "https://www.adkami.com/agenda"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
response = requests.get(url, headers=headers)

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
    
    print("- {} (Episode {})".format(title, episode_info))
    
    # Search on nyaa.si for the anime
    search_on_nyaa(title, episode_info)
