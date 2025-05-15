import requests
from bs4 import BeautifulSoup
parser = 'html.parser'

requests.post("http://Github.com/", data = { 
    'username': '123456', 
    'plate': '123456', 
    'password': 'olk2', 
    'password2': 'olk2' })


if __name__ == "__main__":
    #TODO add function