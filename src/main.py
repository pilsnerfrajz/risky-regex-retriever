import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import json
from urllib.parse import quote
import time

parser = 'html.parser'

filter_url = "https://api.github.com/search/repositories?q=topic:web+language:JavaScript"
repo_filter = "%20(%22.match(%22%20OR%20%22.test(%22%20OR%20%22regex(%22%20OR%20%22RegExp(%22%20OR%20%22.exec(%22)%20language%3AJavaScript&type=code"

load_dotenv("token.env")  # Load from .env

token = os.getenv("GITHUB_TOKEN")

headers = {
	"Accept": "application/vnd.github+json",
	"Authorization": f"token {token}",
	"User-Agent": "RegexCrawler/1.0",
	"X-GitHub-Api-Version": "2022-11-28"
}

def get_repos():
	r = requests.get(filter_url, headers=headers)
	
	if r.status_code == 404:
		print("404 not found")	
		return
	
	data = json.loads(r.text)
	urls = [item["full_name"] for item in data["items"]]
	with open("search_results.txt", "w") as f:
		for url in urls:
			f.write(url + "\n")

def get_files():
	base = 'https://api.github.com/search/code?q='
	#repo = ' repo:webpack/webpack'
	filter = '.test OR .match OR RegExp OR .exec in:file language:JavaScript'
	repo_list = []
	with open("search_results.txt", "r") as f:
		repo_list = [line.strip() for line in f if line.strip()]
	
	for repo in repo_list:
		url = base + quote(filter) + ' repo:' + repo
		print(url)
		name = repo.replace("/", "") + ".json"
		with open("outputs/" + name, "w") as f:
			r = requests.get(url, headers=headers)
			time.sleep(6.5)
			f.write(r.text)

"""with open("search_results.txt", "r") as f:
        repo_list = [line.strip() for line in f if line.strip()]

    # Pattern to search in each repo
    search_terms = '"match(" OR "test(" OR "regex(" OR "RegExp(" OR "exec("'

    for repo in repo_list:
        query = f'{search_terms} language:JavaScript repo:{repo}'

        params = {
            'q': query,
            'per_page': 10
        }

        print(f"Searching in {repo}...")

        r = requests.get("https://api.github.com/search/code", headers=headers, params=params)
        print(r.url)
        if r.status_code == 200:
            results = json.loads(r.text)
            print(results)
"""

"""def get_files():
	with open("search_results.txt", "r") as f:
		for link in f:
			r = requests.get("https://github.com/search?q=repo%3A" + link + repo_filter, headers=headers)
			with open("repo_text_test.txt", "w") as f:
				f.write(r.text)
			break"""

if __name__ == "__main__":
	#get_repos()
	get_files()