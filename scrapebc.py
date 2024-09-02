import re
import requests
from bs4 import BeautifulSoup

from urllib.parse import urljoin

print("Enter your URL:")
url = input()

r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")

album_links = []
for album in soup.find_all('a', href=re.compile(r"\/album/.+")):
    album_url = album.get('href')
    album_links.append(urljoin(url, album_url))

print(len(album_links), album_links)
