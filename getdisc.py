#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib.request
import phpserialize
import os
import html

with open("disc.xml") as f: soup = BeautifulSoup(f, "xml")
with open("media.xml") as f: media = BeautifulSoup(f, "xml")

def quote_str(str):
  return "'" + html.unescape(str).replace("'", "''") + "'"

class YearDict(dict):
  """
  Populate a dictionary of open files, named for call parameter.
  """
  def __missing__(self, year):
    self[year] = open("_data/discography/" + year + ".yml", "w")
    return self[year]

years = YearDict()

for item in soup.find_all("item"):
  if not (item.find('category', {"domain": "artist"})):
      continue
  metadata = {}
  for meta in item.find_all('meta_key'):
    for elem in meta.next_siblings:
      if elem.name == "meta_value":
        metadata[meta.text] = elem.text.strip()
        break
  set = item.find('category', {"domain": "set"})
  if not set: continue
  year = set.text
  disco = years[year]
  # if we have a quoted "project" _within_ the title, just use that
  titleparts = item.title.text.split('"')
  if len(titleparts) >= 3:
    title = titleparts[1]
  else:
    title = item.title.text
  print('- project: ' + quote_str(title), file=disco)
  print('  artist: ' + quote_str(item.find('category', {"domain": "artist"}).text), file=disco)
  print('  year: ' + year, file=disco)
  print('  roles:', file=disco)
  for role in item.find_all('category', {"domain": "project_role"}):
    print('    - ' + role.text, file=disco)
  if not item.find_all('category', {"domain": "project_role"}):
    print('    - ' + "What did I do here again?", file=disco)
  project_link = ""
  if project_url := metadata.get('project_url'):
    urlparts = phpserialize.loads(project_url.encode())
    if b"url" in urlparts and b"title" in urlparts:
      print('  project_url: ', file=disco)
      project_link = urlparts[b'url'].decode()
      print('    url: ' + project_link, file=disco )
      print('    title: ' + urlparts[b'title'].decode(), file=disco )
  if notes := metadata.get('additional_notes'):
    notesoup = BeautifulSoup("<body>" + notes, "html5lib")
    for r in notesoup.find_all("b", text="Mastered by Scott Anthony at Storybook Sound"):
      r.replace_with("")
    for r in notesoup.find_all("b", text="Mastered by Scott Anthony at Storybook Sound "):
      r.replace_with("")
    for r in notesoup.find_all("b", text="Mastered by Scott Anthony"):
      r.replace_with("")
    if (project_link):
      for link in notesoup.find_all("a", {"href": project_link}):
        link.replace_with("")
    notes = notesoup.body.decode_contents()
    print('  notes: >-', file=disco)
    print('    ' + notes.replace("\n", "\n    "), file=disco)
  if (set := item.find('guid', {"isPermaLink": "false"})):
    if thumb := metadata.get('_thumbnail_id'):
      os.makedirs("images/discography/" + year, exist_ok=True)
      attachment = media.find('post_id', text=thumb).parent
      filename = "images/discography/" + year + "/" + os.path.basename(attachment.attachment_url.text)
      print('  image: ', file=disco )
      print('    url: ' + filename, file=disco )
      print("    title: " + quote_str(attachment.title.text), file=disco )
      if not os.path.exists(filename):
        try:
          urllib.request.urlretrieve(attachment.attachment_url.text, filename)
        except urllib.error.HTTPError:
          print("Couldn't fetch ", filename)
