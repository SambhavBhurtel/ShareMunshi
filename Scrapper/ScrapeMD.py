#! .\\venv\\Scripts\\python.exe

import requests
from bs4 import BeautifulSoup
from Scrapper.ScrapeFS import fs_data
from Scrapper.ScrapeName import create_company_dict

def marketdepth_url_resolver(scrip_code):
    url = 'http://www.nepalstock.com/marketdepthofcompany/' + str(scrip_code)
    return url

def scrape_market_depth(scrip_symbol, url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    depth_details = soup.find('table', width='100%', class_='depthIndex')
    depth_details_2 = depth_details.find_all('td')
    
    scrip_depth = {}
    scrip_depth['Scrip Name'] = scrip_symbol
    scrip_depth['Last Traded Price(LTP)'] = depth_details_2[0].find('label').text.strip().replace(',','')
    
    ltp = float(depth_details_2[0].find('label').text.strip().replace(',',''))

    for depth_detail in depth_details_2:
        depth_detail.label.decompose()
    
    scrip_depth['Previous Closing Price'] = depth_details_2[1].text.strip().replace(',','')
    scrip_depth['Opening Price'] = depth_details_2[2].text.strip().replace(',','')
    scrip_depth['Highest Price'] = depth_details_2[3].text.strip().replace(',','')
    scrip_depth['Lowest Price'] = depth_details_2[4].text.strip().replace(',','')
    scrip_depth['Closing Price'] = depth_details_2[5].text.strip().replace(',','')

    pre_close = float(depth_details_2[1].text.strip().replace(',',''))

    if ltp >= pre_close:
        inc_price = ltp - pre_close
        inc_percent = (inc_price / pre_close) * 100
        scrip_depth['Increase in Price'] = inc_price
        scrip_depth['Increase in Percentage'] = round(inc_percent,2)
    else:
        inc_price = pre_close - ltp
        inc_percent = (inc_price / pre_close) * 100
        scrip_depth['Decrease in Price'] = inc_price
        scrip_depth['Decrease in Percentage'] = round(inc_percent,2)

    return scrip_depth

def md_data(scrip_symbol):
    company_dict = create_company_dict()
    scrip_code = company_dict[scrip_symbol][2]
    url = marketdepth_url_resolver(scrip_code)
    scrip_depth = scrape_market_depth(scrip_symbol, url)
    return scrip_depth


def Merge(dict_list):
    return {k:v for d in dict_list for k,v in d.items()}

def md_data_additional(scrip_symbol):
    md_data_minimal = md_data(scrip_symbol)
    additional_data_scrip = fs_data(scrip_symbol,True)
    add_data = fs_data('',True)
    additional_data_nepse = {}
    for key, value in add_data.items():
        additional_data_nepse['NEPSE ' + key] = value

    percentage_of_nepse = {}
    
    nepse_turnover = additional_data_nepse['NEPSE Total Turnover Amount'] 
    scrip_turnover = additional_data_scrip['Total Turnover Amount']
    percent_turnover = (scrip_turnover / nepse_turnover) * 100
    percentage_of_nepse['Percentage of Total Turnover'] = round(percent_turnover,2)
    
    nepse_quantity = additional_data_nepse['NEPSE Total Quantity']
    scrip_quantity = additional_data_scrip['Total Quantity']
    percent_quantity = (scrip_quantity / nepse_quantity) * 100
    percentage_of_nepse['Percentage of Total Quantity'] = round(percent_quantity,2)

    return Merge([md_data_minimal, additional_data_scrip, additional_data_nepse, percentage_of_nepse])

def md_printer(additional=True):
    scrip_symbol = input("MARKET DEPTH VIEWER\nEnter Scrip Code: ").upper()
    print('\n')
    if additional:
        md_data1 = md_data_additional(scrip_symbol)
    else:
        md_data1 = md_data(scrip_symbol)
    for key, value in md_data1.items():
        print(str(key) + ': ' + str(value))
