# your app code here

import pandas as pd
import requests
import sqlite3
from bs4 import BeautifulSoup

url = " https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text
# print(html_data)

requests.get(url).text

soup = BeautifulSoup(html_data,"html.parser")
# print(soup)

tables = soup.find_all('table')

for index, table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        table_index = index

#create a dataframe        
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        tesla_revenue = tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)

"""
tesla_revenue=pd.read_html(url, match="Tesla Quarterly Revenue", flavor='bs4')[0]
tesla_revenue = tesla_revenue.rename(columns={"Tesla Quarterly Revenue(Millions of US $)":"Date","Tesla Quarterly Revenue(Millions of US $).1":"Revenue"}) #Rename df columns to 'Date' and 'Revenue'
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"") # remove the comma and dollar sign from the 'Revenue' column
tesla_revenue.head()
"""

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
# print(tesla_revenue)

records = tesla_revenue.to_records(index=False)
# print(records)

print(f"hay estos records : {len(records)}")


# transformo array a lista
list_of_tuples = list(records)
# print(list_of_tuples)

# Crea la base
connection = sqlite3.connect('Tesla.db')

c = connection.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS revenue (Date, Revenue)''')

# Insert data
c.executemany('INSERT INTO revenue VALUES (?,?)', list_of_tuples)
# Save (commit) the changes
connection.commit()

"""
for row in c.execute('SELECT * FROM revenue'):
    print(row)
"""
