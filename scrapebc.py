import re
import sys
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin, quote_plus


urls = [
    "https://meganreilly.bandcamp.com/album/megan-reilly",
    "https://chrisharford.bandcamp.com/album/looking-out-for-number-6?label=2914117867&tab=music"
]

for arg in sys.argv:
  print(arg)

if (len(sys.argv) < 2):
  print("Usage: python scrapebc.py discimports/filename.csv")
  sys.exit(1)

with open(sys.argv[1], newline='') as l:
  reader = csv.DictReader(l, delimiter='	')
  for row in reader:
    print(row["url"], row["year"], row["roles"], row["notes"])

    r = requests.get(row["url"])
    soup = BeautifulSoup(r.content, "html.parser")

    namesection = soup.findAll('div', {'id':'name-section'})[0]
    #print(namesection)

    albumarturl = soup.findAll('div', {'id':'tralbumArt'})[0].find('img').get('src')
    #print(albumart)

    artist_with_by = soup.findAll('h3')[0].get_text()
    #print("Artist with 'by': ", artist_with_by)

    artist = soup.findAll('h3')[0].findAll('span')[0].findAll('a')[0].get_text()
    #print("Artist: ", artist)

    trackTitle = soup.findAll('h2', {'class': 'trackTitle'})[0].get_text().strip()
    print("Track Title: ", trackTitle)
    year = row["year"].strip()
    # save the album art locally
    albumart = f"images/discography/{year}/{trackTitle.strip().replace(' ', '_').replace('/', '_')}.jpg"
    with open(albumart, 'wb') as f:
      f.write(requests.get(albumarturl).content)

    notes = row["notes"] if row["notes"] else ""
    roles = [r.strip() for r in re.split(r',|, ', row["roles"])]
    with open('_data/discography/%s.yml' % year, 'a+') as f:
      f.write("\n- project: '%s'\n" % trackTitle.strip().replace("'", "&#39;"))
      f.write("  artist: '%s'\n" % artist.strip())
      f.write("  year: %s\n" % year)
      f.write("  roles:\n")
      for role in roles:
        f.write("    - %s\n" % role)
      f.write("  project_url:\n")
      f.write("    url: '%s'\n" % row["url"].strip())
      f.write("    title: '%s'\n" % "Artist Site")
      f.write("  notes: >-\n")
      f.write("    <b>%s</b>\n\n" % notes.strip())
      f.write("  image:\n")
      f.write(f"    url: images/discography/{year}/{quote_plus(trackTitle.strip())}\n")
      f.write("    title: '%s %s'\n\n" % (artist.strip().replace("'", "&#39;"), '"'+trackTitle.strip().replace("'", "&#39;")+'"'))
