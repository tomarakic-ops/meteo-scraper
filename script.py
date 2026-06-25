
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

URL = "https://meteo.hr/podaci.php?section=podaci_vrijeme&param=dnevext"

def scrape():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")

    data = []
    today = datetime.today().strftime("%Y-%m-%d")

    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) == 2:
            data.append([today, cols[0].text.strip(), cols[1].text.strip()])

    df_new = pd.DataFrame(data, columns=["Datum", "Postaja", "Temperatura"])

    file = "data.csv"

    if os.path.exists(file):
        df_old = pd.read_csv(file)

        # NE DUPLIRAJ DATUM
        if today in df_old["Datum"].values:
            print("Data already exists for today")
            return

        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(file, index=False)

scrape()
``
