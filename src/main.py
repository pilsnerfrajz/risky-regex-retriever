import requests
from bs4 import BeautifulSoup
parser = 'html.parser'

res = requests.get("https://github.com/search?q=topic:web language:JavaScript&type=repositories&ref=advsearch", data = {})
print(res)

#if __name__ == "__main__":
    #TODO add function