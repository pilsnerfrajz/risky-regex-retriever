import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import json
from urllib.parse import quote
import time
import re
import subprocess

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

content_headers = {
		"Accept": "application/vnd.github.raw+json",
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
	search_filter = ' in:file language:JavaScript'
	repo_list = []
	with open("search_results.txt", "r") as f:
		repo_list = [line.strip() for line in f if line.strip()]
		
	filter_code = [".match", ".exec", "RegExp", ".test"]
	with open("regex_results.txt", "w", encoding="utf-8") as f:
		for re_function in filter_code:
			print("\n" + re_function)
			for repo in repo_list:
				print("\nScanning " + repo)
				seen = set()
				url = base + re_function + quote(search_filter) + ' repo:' + repo
				r = requests.get(url, headers=headers)

				start = time.time()
				try:
					data = json.loads(r.text)

					paths = [item["path"] for item in data["items"]]
					if len(paths) == 0:
						print("\tFound nothing...")

					for path in paths:
						print("\tFile: " + path)
						if path in seen:
							break
						seen.add(path)
						get_req = "https://api.github.com/repos/" + repo + "/contents/" + path
						content_req = requests.get(get_req, headers=content_headers)
						# TODO FIX FUTUREWARNINGS FROM REGEX ENGINE
						#regex = r'( /(?!\*\*|\/).*?/)'#|(?:\"/(?!\*\*|\/).*?/\")|(?:\'/(?!\*\*|\/).*?/\')'
						regex = r'/(?!\*\*|\/).*?/'
						regex_list = re.findall(regex, content_req.text)
						unique_regexes = set(regex_list)
						valid_regexes = [reg for reg in unique_regexes if is_valid_regex(reg)]

						if len(valid_regexes) != 0:
							print("\tFound unique and valid regexes")
							f.write("Repo " + re_function + " " + repo + path + "\n")
							f.write("\n".join(valid_regexes) + "\n" + "\n")
					
				except KeyError:
					print("\tFound nothing...")

				end = time.time()
				# Avoid rate limiting
				if end - start < 6:
					print("\tSleeping for " + str(6 - (end - start)))
					time.sleep(6 - (end - start))

def is_valid_regex(regex):
	try:
		re.compile(regex)
		return True
	except re.error:
		return False

def validate_regexes():
	repo = ""
	with open("unsafe-regexes.txt", "w") as unsafe_file:
		with open("regex_results.txt", "r") as f:
			for line in f:
				line = line.strip()
				#TODO ADJUST THIS IF-STATEMENT
				if line.startswith("Repo"):
					split = line.split(" ")
					repo = split[2]
					continue
				if line == "":
					continue
				
				#line = "/(a+)+$/"

				# Escape \ to \\ for patterns like /^([^<>]|<[^<>]*>)*>\s*\(/
				escaped_pattern = line.encode('unicode_escape').decode()  # Escapes \ to \\ for JSON
				json_data = {
					"pattern": escaped_pattern,
					"timeLimit": 10,
					"memoryLimit": 1024
				}
				with open("temp.json", "w") as f:
					json.dump(json_data, f)

				# Run vuln-regex-detector
				detector_output = subprocess.run(["vuln-regex-detector/src/detect/detect-vuln.pl", "temp.json"], capture_output=True, text=True)
				if detector_output.returncode != 0:
					continue
				
				data = json.loads(detector_output.stdout)
				opinions = data.get("detectorOpinions", [])

				unsafe_count = sum(1 for o in opinions if o.get("opinion", {}).get("isSafe") == 0)
				safe_count = sum(1 for o in opinions if o.get("opinion", {}).get("isSafe") == 1)

				if unsafe_count > safe_count:
					print(f"❌ Regex pattern {line} is unsafe!")
					unsafe_file.write(line + " " + repo)
				else:
					print(f"✅ Regex pattern {line} is probably safe.")

	subprocess.run(["rm", "temp.json"])

if __name__ == "__main__":
	#get_repos()
	#get_regexes()
	validate_regexes()