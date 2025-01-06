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
from pickle import dump, load
# https://dev.to/webscraping/extract-google-search-results-using-python-and-beautifulsoup-16ig


url = "https://www.google.com/search?q=%22Storybook+Sound%22+site%3Abandcamp.com"


r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

main = soup.select_one("#main")
results = main.findAll("div", {"class": "kCrYT"})
for result in results:
    link = result.find("a")
    try:
      url = link.attrs.get("href")
      print(url)
      # get the subdomain using regex
      subdomain = re.search(r"/(?:url?q=http:\/\/)?(?:([^.]+)\.)?bandcamp\.com/", url).group(1)
      # get the urlpath using regex
      urlpath = re.search(r"/(?:url?q=http:\/\/)?(?:([^.]+)\.)?bandcamp\.com/", url).group(1)
    except AttributeError:
      subdomain = None
      urlpath = None
    print(subdomain)
    print(urlpath)

    divs = result.findAll("div")
    for div in divs:
        print(div.text)
url = "https://www.google.com/search?q=%22Storybook+Sound%22+site%3Abandcamp.com"
resultspages = []
for page in range(1, 150):
    url = f"https://www.google.com/search?q=%22Storybook+Sound%22+site%3Abandcamp.com&start={page}"
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
        bandsmapping[artist][pagetype] = bandsmapping[artist].get(pagetype, [])
        bandsmapping[artist][pagetype].append(bareurl)
        print(f"pagetype: {pagetype} for {artist}")
