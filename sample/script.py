import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_stock_value(stock):
    url = f'https://finance.yahoo.com/quote/{stock}'
    output = requests.get(url)
    soup = BeautifulSoup(output.text, 'html.parser')
    price = soup.find(class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)').text
    price = float(price.replace(',',''))
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return {'stock':stock,'price':price,'time':time}

def auth_with_gsheet():
    scope = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', scope)
    return gspread.authorize(credentials)

def update_sheet():
    client = auth_with_gsheet()
    sheet = client.open('Copy of Investments_2.0').worksheet('Overview')
    data = sheet.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    for i in range(df.shape[0]):
        if df.at[i,"Status"] == 'Active':
            stock = df.at[i,"Stock"]
            stock_info = get_stock_value(stock=stock)
            print(stock_info)
            sheet.update_cell(i+2, 6, stock_info.get('price'))

if __name__ == '__main__':
    update_sheet()
