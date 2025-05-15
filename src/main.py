import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
parser = 'html.parser'

filter_url = "https://github.com/search?q=topic:web+language:JavaScript&type=repositories&ref=advsearch"

load_dotenv()  # Load from .env

token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {token}",
    "User-Agent": "MyCrawler/1.0"
}

r = requests.get(filter_url, headers=headers)

soup = BeautifulSoup(r.text, parser)
repo_links = set()

for a in soup.find_all("a", href=True):
    href = a["href"]
    # Filter: repo links follow the format /owner/repo
    if href.startswith("/") and href.count("/") == 2 and not href.startswith("/search"):
        full_url = "https://github.com" + href
        repo_links.add(full_url)

# Save the full HTML content to search.txt
with open("search_results.txt", "w") as f:
    for link in sorted(repo_links):
        f.write(link + "\n")
print(repo_links)
print(f"Found {len(repo_links)} unique repository links.")