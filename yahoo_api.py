from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

url = 'https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'} #sets correct headers to emulate a browers (avoids 404)

webpage = requests.get(url, headers=headers, timeout=10)

print("Yahoo finance HTTP response: {http_val}".format(http_val=webpage.status_code)) #Checks the https status code

soup = BeautifulSoup(webpage.content, features = "html.parser")


############# Scraping for table #############
table = soup.find('table', attrs={'class':'W(100%) M(0)'})
table_body = table.find('tbody')
table_header = table.find('thead')

############# PULLNG IN ROW DATA #############
historical_data = []
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    historical_data.append([ele for ele in cols if ele]) # Get rid of empty values

############# Pulling in column names #############
tmp_names = table_header.find('tr')
col_names = tmp_names.find_all('th')
col_names = [ele.text.strip() for ele in col_names]

 ############# Creating the pandas dataframe ############# 
df = pd.DataFrame(historical_data, columns = col_names)

historical_high = df['High'].str.replace(",", "").astype(float).to_numpy()

############# Setting up plot #############
historical_dates = df['Date'].to_numpy()
historical_dates = np.flip(historical_dates)
date_ticks = [historical_dates[0],historical_dates[int((len(historical_dates)/4))],historical_dates[int(len(historical_dates)/2)],historical_dates[-1]]
plt.plot(historical_dates, historical_high)
plt.xticks(date_ticks)
plt.show()