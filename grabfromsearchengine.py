import re
import sys
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
# from rich import print
from urllib.parse import urlparse
from urllib.parse import parse_qs
# https://dev.to/webscraping/extract-google-search-results-using-python-and-beautifulsoup-16ig

""" query = "Python programming"
url = f"https://www.google.com/search?q={query}" """

urls = [
    "https://www.google.com/search?q=%22Storybook+Sound%22+site%3Abandcamp.com",
    "https://www.google.com/search?q=%22Storybook+Sound%22+site:bandcamp.com&sca_esv=8eafa2c7f6cb903b&ei=K79wZ730ErbjwN4P0ufayQU&start=10&sa=N&sstk=ATObxK5trltjAFMFeoSYPVUSYKa8URRt7t6cbkWrWXQtE5YWZxZVGcj4glwZDFcsA1dNZdnDwmRp_Mn6gTwn9JIv5mNoh658f6Fy-g&ved=2ahUKEwj9tYqIgsyKAxW2MdAFHdKzNlkQ8tMDegQICRAE&biw=1476&bih=973&dpr=2",
    "https://www.google.com/search?q=%22Storybook+Sound%22+site:bandcamp.com&sca_esv=8eafa2c7f6cb903b&ei=Qr9wZ4PuKdb-p84Po8T_wAs&start=20&sa=N&sstk=ATObxK5L0rktb1cOTNu8UTJhdYH_q66lG-hyaFWeI6g3pRcayMQVJXiuM3SsMgwUbttt80q7wTYPvqFIB_WmOPHOGAVT2LXiJz0gaS2mAAgloTXWTSlp-m5KcgnGgtJ9xbwN&ved=2ahUKEwiDl52TgsyKAxVW_8kDHSPiH7g4ChDy0wN6BAgJEAc&biw=1476&bih=973&dpr=2"
]


r = requests.get(urls[2])
soup = BeautifulSoup(r.content, "html.parser")

results = soup.findAll("div", {"class": "kCrYT"})
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
