from bs4 import BeautifulSoup
import urllib.request
import phpserialize

with open("disc.xml") as f: soup = BeautifulSoup(f, "xml")

with open("_data/discography.yml", "w") as disco:
  for item in soup.find_all("item"):
    metadata = {}
    for meta in item.find_all('meta_key'):
      for elem in meta.next_siblings:
        if elem.name == "meta_value":
          metadata[meta.text] = elem.text.strip()
          break
    print('- project: ' + item.title.text.replace(":", "&#58;"), file=disco)
    if (set := item.find('category', {"domain": "artist"})):
      print('  artist: ' + item.find('category', {"domain": "artist"}).text, file=disco)
    if (set := item.find('category', {"domain": "set"})):
      print('  year: ' + set.text, file=disco)
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
      print('  notes: ' + notes, file=disco)
    if (set := item.find('guid', {"isPermaLink": "false"})):
      try:
        image_url = item.find('guid', {"isPermaLink": "false"}).text
        print('  image: ' + image_url.replace("wp/wp-content", "app"), file=disco)
        # print('  image_filename: ' + image_url.split('/')[-1], file=disco)
        # urllib.request.urlretrieve(image_url, "disco_images/" + item.find('guid', {"isPermaLink": "false"}).text.split('/')[-1])
      except urllib.error.HTTPError:
        pass
