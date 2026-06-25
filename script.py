import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

URL = "https://meteo.hr/podaci.php?section=podaci_vrijeme&param=dnevext"

def scrape():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table")

    if not tables:
        print("No tables found")
        return

    table = tables[0]
    rows = table.find_all("tr")

    data = []
    today = datetime.today().strftime("%Y-%m-%d")

    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) == 2:
            try:
                temp_value = float(cols[1].text.strip())
            except:
                continue

            data.append([
                today,
                cols[0].text.strip(),
                temp_value
            ])

    if len(data) == 0:
        print("No data extracted")
        return

    df_new = pd.DataFrame(data, columns=["Datum", "Postaja", "Temperatura"])

    file = "data.xlsx"

    if os.path.exists(file):
        df_old = pd.read_excel(file)

        # spriječi duplikat
        if today in df_old["Datum"].astype(str).values:
            print("Data already exists for today")
            return

        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_excel(file, index=False)

    print("✅ Data saved to Excel")

scrape()
