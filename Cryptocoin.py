import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

headers= {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}
base_url = "https://www.coingecko.com/en"

tables = []

for i in range(1, 4):
    print('Processing page {0}'.format(i))
    params = {
        'page': i
    }
    response = requests.get(base_url, headers=headers, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    html_stringio = StringIO(str(soup))
    tables.append(pd.read_html(html_stringio)[0])

master_table = pd.concat(tables)
master_table = master_table.loc[:, master_table.columns[1:-1]]
master_table.to_csv('TradingRobot/Crypto Data Table.csv', index=False)

crypto_id = input('Enter the crypto id: ')

url_crypto = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days=1'

# Make a GET request to fetch the data
response = requests.get(url_crypto)

# Parse the JSON data  

data = response.json()
price_history = data['prices']
print(data['prices'][0][0])
from datetime import datetime

# # Example integer timestamp
timestamp = data['prices'][0][0]  # Replace this with your integer timestamp
print('timestamp: ',timestamp)
# # Convert the integer timestamp to a date
date = datetime.fromtimestamp(timestamp / 1000)

# Print the date
print('date: ',date)
print("price: ", data['prices'][0][1])
df = pd.DataFrame(price_history)
df.to_csv('TradingRobot/Crypto Price History.csv', index=False)