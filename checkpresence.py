import re
import os

def findfiles(path, regex):
    regObj = re.compile(regex)
    res = []
    for root, dirs, fnames in os.walk(path):
        for fname in fnames:
            if regObj.match(fname):
                res.append(os.path.join(root, fname))
    return res


years = ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"]
for year in years:
  print(f"Checking for {year}...")
  try:
    with(open(f"test/{year}.yml", "r")) as f:
      lines_with_project = [line for line in f.readlines() if re.search(r"project", line)]
      #print(f"Fetched {len(lines_with_project)} projects for {year}...")
      for line in lines_with_project:
        try:
          project = re.search(r"- project: '(.*)'", line).group(1)
        except AttributeError:
          continue
        #print(f"Checking for {project} in {year}...")
        currentfiles = next(os.walk("_data/discography/"), (None, None, []))[2]  # [] if no file
        found = False
        for fname in currentfiles:
          if os.path.isfile(f"_data/discography/{fname}"):
              # Full path
              f = open(f"_data/discography/{fname}", 'r')

              if project.lower().replace("'", "&#39;") in f.read().lower():
                  print('\t \033[46;1m(found %s in file %s)\033[0m' % (project, fname))
                  found = True
                  break
              else:
                  pass
                  #print('Project %s not found in file %s' % (project, fname))
              f.close()
        if not found:
          print(f"\033[31;1m!!!DID NOT FIND: Project {project} \033[0m \n")
  except FileNotFoundError:
    print(f"No Read File found for {year}...")
    continue
