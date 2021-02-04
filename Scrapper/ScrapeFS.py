#! .\\venv\\Scripts\\python.exe

import requests
from bs4 import BeautifulSoup

def fs_scraper(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    floor_sheet_table = soup.find('table', class_='table my-table')
    floor_sheet_rows = floor_sheet_table.find_all('tr')

    fs_trs = floor_sheet_rows[2:-3]

    fs_dict = {}

    for fs_tr in fs_trs:
        all_tds = fs_tr.find_all('td')
        fs_dict[all_tds[0].text] = {
            'Contract No.':int(all_tds[1].text),
            'Scrip Symbol':all_tds[2].text,
            'Buyer Broker No.':int(all_tds[3].text),
            'Seller Broker No.':int(all_tds[4].text),
            'Quantity':int(all_tds[5].text),
            'Rate':round(float(all_tds[6].text),2),
            'Amount':all_tds[7].text,
        }

    total_details = {
        'Total Turnover Amount':floor_sheet_rows[-2].find_all('td')[1].text,
        'Total Quantity':floor_sheet_rows[-1].find_all('td')[1].text,
    }

    return fs_dict, total_details

def fs_data(scrip_symbol='', turnover= False):
    if not turnover:
        url = 'http://www.nepalstock.com/main/floorsheet/index/1/?&stock-symbol='+scrip_symbol+'&_limit=30000'
        fs_data_records = fs_scraper(url)[0]
        return fs_data_records
    else:
        url = 'http://www.nepalstock.com/main/floorsheet/index/1/?&stock-symbol='+scrip_symbol+'&_limit='
        fs_data_turnover = fs_scraper(url)[1]
        for k,v in fs_data_turnover.items():
            fs_data_turnover[k] = int(v.replace(',',''))
        return fs_data_turnover

# scrip_name = 'PCBL'
# url = 'http://www.nepalstock.com/main/floorsheet/index/1/?contract-no=&stock-symbol='+scrip_name+'&buyer=&seller=&_limit=30000'
# with open('floorsheet_data.txt', 'w') as f:
#     print(fs_scraper(url)[0], file=f)

# print(fs_data('',True))