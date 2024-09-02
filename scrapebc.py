import re
import requests
from bs4 import BeautifulSoup

from urllib.parse import urljoin


urls = [
    "https://meganreilly.bandcamp.com/album/megan-reilly",
    "https://chrisharford.bandcamp.com/album/looking-out-for-number-6?label=2914117867&tab=music"
]

for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    namesection = soup.findAll('div', {'id':'name-section'})[0]
    print(namesection)

    albumart = soup.findAll('div', {'id':'tralbumArt'})[0].find('img').get('src')
    print(albumart)

    artist_with_by = soup.findAll('h3')[0].get_text()
    print("Artist with 'by': ", artist_with_by)

    artist = soup.findAll('h3')[0].findAll('span')[0].findAll('a')[0].get_text()
    print("Artist: ", artist)

    trackTitle = soup.findAll('h2', {'class': 'trackTitle'})[0].get_text()

    """ album_links = []
    for album in soup.find_all('a', href=re.compile(r"\/album/.+")):
        album_url = album.get('href')
        album_links.append(urljoin(url, album_url))

    print(len(album_links), album_links) """
