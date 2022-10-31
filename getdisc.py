from bs4 import BeautifulSoup

with open("disc.xml") as f: soup = BeautifulSoup(f, "xml")

with open("_data/discography.yml", "w") as disco:
  for item in soup.find_all("item"):
    print('- project: ' + item.title.text, file=disco)
    if (set := item.find('category', {"domain": "artist"})):
      print('  artist: ' + item.find('category', {"domain": "artist"}).text, file=disco)
    if (set := item.find('category', {"domain": "set"})):
      print('  year: ' + set.text, file=disco)
    print('  roles:', file=disco)
    for role in item.find_all('category', {"domain": "project_role"}):
      print('    - ' + role.text, file=disco)
    if not item.find_all('category', {"domain": "project_role"}):
      print('    - ' + "What did I do here again?", file=disco)
    if (set := item.find('guid', {"isPermaLink": "false"})):
      print('  image: ' + item.find('guid', {"isPermaLink": "false"}).text.replace("wp/wp-content", "app"), file=disco)
