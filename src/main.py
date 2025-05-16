import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import json
from urllib.parse import quote
import time
import re

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

def get_regexes():
	base = 'https://api.github.com/search/code?q='
	# TODO Iterate through filters to get more results
	search_filter = '.match in:file language:JavaScript'
	repo_list = []
	with open("search_results.txt", "r") as f:
		repo_list = [line.strip() for line in f if line.strip()]
	
	content_headers = {
		"Accept": "application/vnd.github.raw+json",
		"Authorization": f"token {token}",
		"User-Agent": "RegexCrawler/1.0",
		"X-GitHub-Api-Version": "2022-11-28"
	}	

	for repo in repo_list:
		url = base + quote(search_filter) + ' repo:' + repo
		r = requests.get(url, headers=headers)
		time.sleep(6.5)
		data = json.loads(r.text)
		paths = [item["path"] for item in data["items"]]
		for path in paths:
			get_req = "https://api.github.com/repos/" + repo + "/contents/" + path
			content_req = requests.get(get_req, headers=content_headers)
			regex = r'(?: /(?!\*\*|\/).*?/)|(?:\"/(?!\*\*|\/).*?/\" )|(?:\'/(?!\*\*|\/).*?/\')'
			regex_list = re.findall(regex, content_req.text)
			if len(regex_list) != 0: #TODO Log instead of print
				print(path)
				print(regex_list)
		return # TODO Remove

if __name__ == "__main__":
	#get_repos()
	get_regexes()