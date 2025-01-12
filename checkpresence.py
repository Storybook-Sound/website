import re
years = ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"]
for year in years:
  print(f"Checking for {year}...")
  try:
    with(open(f"test/{year}.yml", "r")) as f:
      lines_with_project = [line for line in f.readlines() if re.search(r"project", line)]
      print(f"Fetched {len(lines_with_project)} projects for {year}...")
      for line in lines_with_project:
        try:
          project = re.search(r"- project: '(.*)'", line).group(1)
        except AttributeError:
          continue
        print(f"Checking for {project} in {year}...")
        try:
          with(open(f"_data/discography/{year}.yml", "r")) as f:
            matched_lines = [line for line in f.readlines() if re.search(r"project", line) and re.search(project, line)]
            print(f"Matched {len(matched_lines)} lines for {project} in {year}...")
            if len(matched_lines) == 0:
              print(f"Project {project} not found in {year}...")
            else:
              for matched_line in matched_lines:
                print("Matched Line: %s" % matched_line)
        except FileNotFoundError:
          print(f"Current File not found for {year}...")
          continue
  except FileNotFoundError:
    print(f"No Read File found for {year}...")
    continue
