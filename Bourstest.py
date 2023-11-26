import streamlit
import requests_html
from tsetmc_api.symbol import Symbol
session = requests_html.HTMLSession()
h =session.get('http://cdn.tsetmc.com/api/ClosingPrice/GetMarketMap?market=0&size=1360&sector=0&typeSelected=1')
j = h.json()
# print(j)
# for i in j:
#     if i["percent"] > float(2) :
#         print(f'{i["lVal18AFC"]} - {i["color"]}')
#     else:
#         print('mosbat')

for i in j:
    if i["lVal18AFC"] == "وبملت":
        print(i)

    # if i['priceMin'] < '1200':
    #     print(i["lVal30"])

    # if i["lVal30"] == 'سايپا':
    #     print(f'{i["lVal18AFC"]} ______ {i["lVal30"]} ______ {i["percent"]}')
    # else:
    #     print('هیچی پیدا نشد') 