import matplotlib.pyplot as plt
import pandas as pd
import os
import re
from datetime import datetime


DATA_PATH = "./data/"

files = [f for f in os.listdir(DATA_PATH) if re.match(r".*_percentages.csv", f)]
sorted_files = sorted(files, 
  key=lambda f: datetime(*map(int,f[:10].split("_"))).timestamp())


# pull top 5 countries from the latest data:
countries = pd.read_csv(DATA_PATH+files[-1]).head()["country"]

data = {}
dates = [f[:10].replace("_","-") for f in sorted_files]
for c in countries:
  data[c] = []
  for f in sorted_files:
    df = pd.read_csv(DATA_PATH+f)
    value = df.loc[df["country"] == c]["percent inoculated"].values[0]
    data[c].append(value)

for c in countries:
  plt.plot(dates,data[c])

plt.legend(countries)
plt.ylabel("Percentage vaccinated")
plt.xlabel("Date")
plt.title("Vaccination percentage vs time")
plt.show()