import json
from scraper import scrape_geometrygeeks
from FrameStack import FrameStack

print("--- Scraped Data ---")
res = scrape_geometrygeeks("https://geometrygeeks.bike/bike/ribble-endurance-sl-disc-2021/")
scraped = res['geometry'].get('L', {})
print(json.dumps(scraped, indent=2))

print("--- FrameStack Parsing Scraped Data ---")
with open('temp_scraped.txt', 'w') as f:
    for k, v in scraped.items():
        f.write(f"{k}\t{v}\n")
try:
    fs1 = FrameStack('temp_scraped.txt')
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")

print("--- FrameStack Parsing Original TXT ---")
try:
    fs2 = FrameStack('Geometry_files/Ribble_endurance_L.txt')
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
