from googleapiclient.discovery import build
from pprint import pprint
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

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

for start in range(1, 100, 10):
  r = google_search('"Storybook Sound"', configs.googleapikey, configs.custom_search_engine_id, num=10, start=start)
  for i in r:
      links.add(i['link'])

rolesmapping = {}

todaysdateandtime = datetime.now().strftime("%Y-%m-%d-%H-%M")

for link in links:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    albumCredits = soup.findAll('div', {'class': 'tralbumData tralbum-credits'})[0].get_text()
    roles = []
    if re.search(r"Scott Anthony|Storybook Sound", albumCredits, re.IGNORECASE):
      roles = [r.strip() for r in albumCredits.split('\n')]
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
        pprint(f"\033[33;1m{albumCredits}\033[0m\n")
        rolesmapping[link] = albumCredits
    else:
        print(f"\033[46;1m(found Scott Anthony in {link})\033[0m\n")
        rolesmapping[link] = roles
with open(f'discimports/{todaysdateandtime}.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['url', 'year', 'roles', 'notes'])
    writer.writeheader()
    for link, roles in rolesmapping.items():
        writer.writerow({'url': link, 'year': year, 'roles': ', '.join(roles), 'notes': ''})

print(f"Wrote import file for {len(links)} links.")
