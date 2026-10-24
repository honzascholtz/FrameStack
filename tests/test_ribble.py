import urllib.request
from bs4 import BeautifulSoup
import json
import re

req = urllib.request.Request('https://geometrygeeks.bike/bike/ribble-endurance-sl-disc-2021/', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table') 

headers = []
for th in table.find('thead').find_all('th'):
    headers.append(th.text.strip())

print("HEADERS:", headers)

for row in table.find('tbody').find_all('tr'):
    cols = row.find_all(['th', 'td'])
    if not cols: continue
    
    measure_name = cols[0].text.strip()
    if measure_name == 'Reach':
        print(measure_name, [c.text.strip() for c in cols[1:]])
