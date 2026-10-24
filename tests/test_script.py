import urllib.request
from bs4 import BeautifulSoup

req = urllib.request.Request('https://geometrygeeks.bike/bike/ribble-endurance-sl-disc-2021/', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

for script in soup.find_all('script'):
    if script.string and 'skeleton' in script.string.lower():
        print(script.string)
