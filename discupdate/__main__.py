from googleapiclient.discovery import build
from pprint import pprint
import os
import re
import sys
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin, quote_plus
from . import configs
from datetime import datetime
# https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
# https://console.cloud.google.com/apis/api/customsearch.googleapis.com/metrics?inv=1&invt=AbnGmw&project=search-api-story-1737131699378
# https://stackoverflow.com/a/37084643/2223106

links = set()

def checkpresence(url):
  for f in os.listdir('_data/discography'):
    if f.endswith('.yml'):
      with open(f"_data/discography/{f}", "r") as f:
        if url in f.read():
          return f.name
  return None

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

for start in range(1, 100, 10):
  print(f"Fetching results from {start}...")
  r = google_search('"Storybook Sound"', configs.googleapikey, configs.custom_search_engine_id, num=10, start=start)
  for i in r:
      links.add(i['link'])

fixtheseroles = {}

todaysdateandtime = datetime.now().strftime("%Y-%m-%d-%H-%M")

for link in links:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    albumCredits = soup.findAll('div', {'class': 'tralbumData tralbum-credits'})[0].get_text()
    roles = []
    if re.search(r"Scott Anthony|Storybook Sound", albumCredits, re.IGNORECASE):
      roles = [r.strip() for r in albumCredits.split('\n') if re.search(r"Scott Anthony|Storybook Sound", r)]
    else: roles = ["Undefined"]
    year = re.search(r"(\d{4})", albumCredits).group(1) if re.search(r"(\d{4})", albumCredits) else "UNKNOWN"
    # Check for presence in discography
    try:
      with(open(f"_data/discography/{year}.yml", "r")) as f:
        lines_with_project = [line for line in f.readlines() if re.search(r"project", line)]
        for line in lines_with_project:
          try:
            project = re.search(r"- project: '(.*)'", line).group(1)
          except AttributeError:
            continue
          if project.lower().replace("'", "&#39;") in albumCredits.lower():
            print(f"\033[46;1m(found {project} in {link})\033[0m\n")
            break
    except FileNotFoundError:
      print(f"No Read File found for {year}...")
      continue
    if roles == ["Undefined"]:
        print(f"\033[31;1m!!!DID NOT FIND: Scott Anthony or Storybook Sound in {link} \033[0m \n")
        # make this one yellow
        # pprint(f"\033[33;1m{albumCredits}\033[0m\n")
        fixtheseroles[link] = albumCredits
    else:
        print(f"\033[46;1m(found Scott Anthony in {link})\033[0m\n")
    if (checkpresence(link)):
      print(f"Found {link} in {checkpresence(link)}")
    else:
      print(f"Did not find {link} in any discography directory. Adding to {year}.yml")
      namesection = soup.findAll('div', {'id':'name-section'})[0]
      albumarturl = soup.findAll('div', {'id':'tralbumArt'})[0].find('img').get('src')
      artist_with_by = soup.findAll('h3')[0].get_text()
      artist = soup.findAll('h3')[0].findAll('span')[0].findAll('a')[0].get_text().strip()
      trackTitle = soup.findAll('h2', {'class': 'trackTitle'})[0].get_text().strip()
      image_extension = albumarturl.split('.')[-1]
      image_basename = f"{trackTitle.replace(' ', '_').replace('/', '_')}"
      imagepath = f"images/discography/{year}/"
      with open(f"{imagepath}{image_basename}.{image_extension}", 'wb') as f:
        f.write(requests.get(albumarturl).content)
      with open('_data/discography/%s.yml' % year, 'a+') as f:
        f.write("\n- project: '%s'\n" % trackTitle.replace("'", '&#39;'))
        f.write("  artist: '%s'\n" % artist.strip())
        f.write("  year: %s\n" % year)
        f.write("  roles:\n")
        for role in roles:
          f.write("    - %s\n" % role)
        f.write("  project_url:\n")
        f.write("    url: '%s'\n" % link)
        f.write("    title: '%s'\n" % "Artist Site")
        f.write("  notes: >-\n")
        f.write("    <b></b>\n\n")
        f.write("  image:\n")
        f.write(f"    url: images/discography/{year}/{quote_plus(image_basename)}.{image_extension}\n")
        f.write("    title: '%s %s' \n\n" % (artist.replace("'", '&#39;'), '"'+trackTitle.replace("'", '&#39;')+'"'))

with open(f"discupdate/fixtheseroles-{todaysdateandtime}.yml", "w") as f:
  for link, roles in fixtheseroles.items():
    f.write(f"\n- url: {link}\n")
    f.write(f"  roles: >-\n")
    f.write(f"    {roles}\n")

print(f"Wrote import file for {len(links)} links. Fix roles for {len(fixtheseroles)} links.")
