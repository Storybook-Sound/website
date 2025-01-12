import re
import sys
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
# from rich import print
from urllib.parse import urlparse
from urllib.parse import parse_qs
from pprint import pprint

resultspages = []
for page in range(1, 150):
    url = f"https://www.google.com/search?q=%22Storybook+Sound%22+2024+site%3Abandcamp.com&start={page}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    main = soup.select_one("#main")
    results = main.findAll("div", {"class": "kCrYT"})
    resultspages.append(results[:])

bandsmapping = {}

for page in resultspages:
    for result in page:
        link = result.find("a")
        try:
            url = link.attrs.get("href")
            artist = re.search(r"/(?:url\?q=http[s]?:\/\/)?(?:([^.]+)\.)?bandcamp\.com\/", url).group(1)
            print(f"artist: {artist}")
            bareurl = re.search(r"/url\?q=(http[s]?:\/\/[^.]+\.bandcamp\.com\/[track|album]?.*)\&sa", url).group(1)
            pagetype = re.search(r"/(?:url\?q=http[s]?:\/\/)?(?:[^.]+\.)?bandcamp\.com\/(track|album)?", url).group(1)
        except AttributeError:
            artist = None
            pagetype = None
        # @TODO add the pagetype and page to collection for this subdomain
        bandsmapping[artist] = bandsmapping.get(artist, {})
        if (pagetype == None): continue
        bandsmapping[artist][pagetype] = bandsmapping[artist].get(pagetype, set())
        bandsmapping[artist][pagetype].add(bareurl)
        print(f"pagetype: {pagetype} for {artist}")

for band in bandsmapping.keys():
  print(f"Fetching details info for {band}...")
  for pagetype in bandsmapping[band].keys():
    for url in bandsmapping[band][pagetype]:
      print(f"Fetching {url}...")
      r = requests.get(url)
      soup = BeautifulSoup(r.content, "html.parser")
      namesection = soup.findAll('div', {'id':'name-section'})[0]
      albumart = soup.findAll('div', {'id':'tralbumArt'})[0].find('img').get('src')
      artist_with_by = soup.findAll('h3')[0].get_text()
      artist = soup.findAll('h3')[0].findAll('span')[0].findAll('a')[0].get_text()
      trackTitle = soup.findAll('h2', {'class': 'trackTitle'})[0].get_text().strip()
      albumCredits = soup.findAll('div', {'class': 'tralbumData tralbum-credits'})[0].get_text()
      year = re.search(r"(\d{4})", albumCredits).group(1) if re.search(r"(\d{4})", albumCredits) else "UNKNOWN"
      # Anything related to Scott Anthony
      roles = [r.strip() for r in albumCredits.split('\n') if re.search(r"Scott Anthony", r)] if re.search(r"Scott Anthony", albumCredits) else ["mastering probably"]
      with open('test/%s.yml' % year, 'a+') as f:
        f.write("\n- project: '%s'\n" % trackTitle.strip())
        f.write("  artist: '%s'\n" % artist.strip())
        f.write("  year: %s\n" % year)
        f.write("  roles:\n")
        for role in roles:
          f.write("    - %s\n" % role)
        f.write("  project_url:\n")
        f.write("    url: '%s'\n" % url)
        f.write("    title: '%s'\n" % "Artist Site")
        f.write("  notes: >-\n")
        f.write("    <b>%s</b>\n\n" % ', '.join([role.strip() for role in roles]))
        f.write("  image:\n")
        f.write("    url: '%s'\n" % albumart)
        f.write("    title: '%s %s'\n\n" % (artist.strip(), '"'+trackTitle.strip()+'"'))
        print(f"Done fetching {url}...")
