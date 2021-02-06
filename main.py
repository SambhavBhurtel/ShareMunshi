#! .\\venv\\Scripts\\python.exe

from Scrapper.ScrapeName import StockName, ScripCode, AddScripCode
from Scrapper.ScrapeMD import marketdepth_url_resolver, scrape_market_depth
from Scrapper.ScrapeFS import fs_data


def create_company_dict():
    company_detail_url = 'http://www.nepalstock.com/company/index/1?stock-name=&stock-symbol=&sector-id=&_limit=500'
    company_detail = StockName(company_detail_url)

    market_depth_url = 'http://www.nepalstock.com/marketdepth'
    scrip_code = ScripCode(market_depth_url)

    return AddScripCode(company_detail, scrip_code)
    

def scrip_info(scrip_symbol):
    company_dict = create_company_dict()
    return company_dict[scrip_symbol]

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

md_printer()
print(scrip_info('MEN'))