from bs4 import BeautifulSoup
import urllib.request
import phpserialize

with open("disc.xml") as f: soup = BeautifulSoup(f, "xml")
with open("media.xml") as f: media = BeautifulSoup(f, "xml")

def quote_str(str):
  return "'" + str.replace("'", "''") + "'"

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
  print('- project: ' + quote_str(item.title.text), file=disco)
  print('  artist: ' + item.find('category', {"domain": "artist"}).text, file=disco)
  print('  year: ' + year, file=disco)
  print('  roles:', file=disco)
  for role in item.find_all('category', {"domain": "project_role"}):
    print('    - ' + role.text, file=disco)
  if not item.find_all('category', {"domain": "project_role"}):
    print('    - ' + "What did I do here again?", file=disco)
  if project_url := metadata.get('project_url'):
    print('  project_url: ', file=disco)
    urlparts = phpserialize.loads(project_url.encode())
    for k,v in urlparts.items():
      print('    ' + k.decode() + ': ' + v.decode(), file=disco )
  if notes := metadata.get('additional_notes'):
    print('  notes: >-', file=disco)
    print('    ' + notes.replace("\n", "\n    "), file=disco)
  if (set := item.find('guid', {"isPermaLink": "false"})):
    try:

      if thumb := metadata.get('_thumbnail_id'):
        attachment = media.find('post_id', text=thumb).parent
        print('  image: ', file=disco )
        print('    url: ' + attachment.attachment_url.text, file=disco )
        print("    title: " + quote_str(attachment.title.text), file=disco )
      # print('  image_filename: ' + image_url.split('/')[-1], file=disco)
      # urllib.request.urlretrieve(image_url, "disco_images/" + item.find('guid', {"isPermaLink": "false"}).text.split('/')[-1])
    except urllib.error.HTTPError:
      pass
