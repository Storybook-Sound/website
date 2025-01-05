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


p2 = url + "&dpr=2"
page2 = requests.get(p2)
moresoup = BeautifulSoup(page2.content, "html.parser")
results2 = moresoup.findAll("div", {"class": "kCrYT"})
len(results2)

link = results[2].find("a")
link.attrs.get("href")

def extract_href(href):
    url = urlparse(href)
    query = parse_qs(url.query)
    if not ('q' in query and query['q'] and len(query['q']) > 0):
        return None
    return query['q'][0]

def extract_section(gdiv):
    # Getting our elements
    title = gdiv.select_one('h3')
    link = gdiv.select_one('a')
    description = gdiv.find('.BNeawe')
    return {
        # Extract title's text only if text is found
        'title': title.text if title else None,

        'link': link['href'] if link else None,
        'description': description.text if description else None
    }

def extract_results(soup):
    main = soup.select_one("#main")

    res = []
    for gdiv in main.select('.g, .fP1Qef'):
        res.append(extract_section(gdiv))
    return res

results = extract_results(soup)
print(results)
