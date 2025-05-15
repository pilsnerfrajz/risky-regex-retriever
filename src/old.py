import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

parser = 'html.parser'

filter_url = "https://api.github.com/search?q=topic:web+language:JavaScript&type=repositories&ref=advsearch&p="
repo_filter = "%20(%22.match(%22%20OR%20%22.test(%22%20OR%20%22regex(%22%20OR%20%22RegExp(%22%20OR%20%22.exec(%22)%20language%3AJavaScript&type=code"

load_dotenv()  # Load from .env

token = os.getenv("GITHUB_TOKEN")

headers = {
	"Authorization": f"token {token}",
	"User-Agent": "MyCrawler/1.0"
}

def get_repos():
	repo_links = set()
	
	for i in range(1,2):
		r = requests.get(filter_url + str(i), headers=headers)
		
		if r.status_code == 404:	
			break

		matches = []
		
		for line in r.text.splitlines():
			if line.startswith('</style><h1 class="sr-only">repositories Search Results'):
				matches.append(line)
				soup = BeautifulSoup(line, parser)
				
				# Now extract links
				for a in soup.find_all("a", href=True):
					href = a["href"]
					if href.startswith("/") and href.count("/") == 2 and not href.startswith("/search") and not href.startswith("/topics"):
						full_url = href[1:] # remove first slash
						repo_links.add(full_url)

	with open("search_results.txt", "w") as f:
		for link in sorted(repo_links):
			f.write(link + "\n")
	print(repo_links)
	print(f"Found {len(repo_links)} unique repository links.")

def get_files():
	with open("search_results.txt", "r") as f:
		for link in f:
			r = requests.get("https://api.github.com/search?q=repo%3A" + link + repo_filter, headers=headers)
			with open("repo_text_test.txt", "w") as f:
				f.write(r.text)
			break

if __name__ == "__main__":
	get_repos()
	get_files()