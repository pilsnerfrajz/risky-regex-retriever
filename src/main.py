import requests
from bs4 import BeautifulSoup

url = "https://github.com/search?q=topic:web+language:JavaScript&type=repositories&ref=advsearch"

# GitHub might block some bots, so set a User-Agent header
headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)

# Save the full HTML content to search.txt
with open("search.txt", "w", encoding="utf-8") as f:
    f.write(res.text)

print(f"Saved response to search.txt (Status: {res.status_code})")
