import urllib.request
from bs4 import BeautifulSoup
import json
import re

req = urllib.request.Request('https://geometrygeeks.bike/bike/canyon-endurace-cf-slx-2023/', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table') # geometrygeeks often has class="table" or just the first table

headers = []
for th in table.find('thead').find_all('th'):
    headers.append(th.text.strip())

sizes = [h for h in headers[1:] if "To view geometry" not in h and "Add to Compare" not in h]

data = {size: {} for size in sizes}

for row in table.find('tbody').find_all('tr'):
    cols = row.find_all(['th', 'td'])
    if not cols or len(cols) <= 1: continue
    
    measure_name = cols[0].text.strip()
    if measure_name.lower() in ('data source', 'add to compare', ''):
        continue

    # Sometimes there are extra columns, mapping one-to-one
    for i, size in enumerate(sizes):
        if i + 1 < len(cols):
            val = cols[i+1].text.strip()
            # Remove any non-numeric except dots or minuses
            val = re.sub(r'[^\d.-]', '', val)
            if val:
                data[size][measure_name] = val

print(json.dumps(data, indent=2))
