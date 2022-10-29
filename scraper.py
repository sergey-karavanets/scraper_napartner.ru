import requests
from bs4 import BeautifulSoup
import lxml

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    req = requests.get(url, headers)

    with open('project.html', 'w', encoding='utf-8') as file:
        file.write(req.text)

    with open('project.html', encoding='utf-8') as file:
        src = file.read()

get_data('https://www.napartner.ru/')