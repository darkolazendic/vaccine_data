#!/usr/bin/env python3

import requests
import json
import csv
import os
from bs4 import BeautifulSoup
from datetime import date
from tabulate import tabulate


URL = "https://www.bloomberg.com/graphics/covid-vaccine-tracker-global-distribution"

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
  + " (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

soup = BeautifulSoup(requests.get(URL,headers=headers).content,"html.parser")
try:
  script_contents = soup.select("script#dvz-data-cave")[0].string
  data = json.loads(script_contents)["vaccination"]["global"]
except:
  exit("Could not find or parse the data script tag.")

percentages = []

file_name = date.today().strftime("%Y_%m_%d")
with open(f"./data/{file_name}.csv",mode="w") as csv_file:
  columns = data[0].keys()
  writer = csv.DictWriter(csv_file,fieldnames=columns,extrasaction="ignore")

  writer.writeheader()
  for d in data:
    writer.writerow(d)
    try:
      percentages.append([d["name"],round(d["noDosesTotalPerCapita"]*100,2)])
    except:
      pass

sorted_percentages = sorted(percentages,key=lambda a: a[1],reverse=True)

with open(f"./data/{file_name}_percentages.csv",mode="w") as rankings_csv:
  columns = ["country", "percent inoculated"]
  writer = csv.DictWriter(rankings_csv,fieldnames=columns,extrasaction="ignore")

  writer.writeheader()
  for p in sorted_percentages:
    writer.writerow({"country": p[0], "percent inoculated": p[1]})

print(f"\nAll data pulled successfully.")
print("\nCountries ranked by inoculation percentage:")
print(tabulate(sorted_percentages,headers=["country","percent inoculated"]))

os.system("notify-send 'vaccine data pulled'")