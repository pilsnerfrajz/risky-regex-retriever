import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

url = "https://github.com/search?q=topic:web+language:JavaScript&type=repositories&ref=advsearch"

load_dotenv()  # Load from .env

token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {token}",
    "User-Agent": "MyCrawler/1.0"
}

res = requests.get(url, headers=headers)

# Save the full HTML content to search.txt
with open("search.txt", "w", encoding="utf-8") as f:
    f.write(res.text)

print(f"Saved response to search.txt (Status: {res.status_code})")
