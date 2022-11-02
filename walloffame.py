#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib.request
import phpserialize
import os
import html
import requests

r = requests.get("https://storybooksound.com/who-we-are/")
soup = BeautifulSoup(r.text, "html5lib")
os.mkdir("images/wall_of_fame/")
with open("_data/walloffame.yml", "w") as polaroids:
  for img in soup.find_all("img", {"data-src": True}):
    orig = img['data-src'].replace("-scaled", "")
    filename = "images/wall_of_fame/" + os.path.basename(orig)
    try:
      urllib.request.urlretrieve(orig, filename)
    except urllib.error.HTTPError:
      print("Couldn't fetch ", filename)
    print("- image:", file=polaroids)
    print("  url: " + orig, file=polaroids)
