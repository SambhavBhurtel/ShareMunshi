#! .\\venv\\Scripts\\python.exe

from Scrapper.ScrapeCode import ScripCode, AddScripCode
from Scrapper.ScrapeName import StockName
from Scrapper.ScrapeMD import marketdepth_url_resolver, scrape_market_depth
from Scrapper.ScrapeFS import fs_scraper, fs_data


def create_company_dict():
    company_detail_url = 'http://www.nepalstock.com/company/index/1?stock-name=&stock-symbol=&sector-id=&_limit=500'
    company_detail = StockName(company_detail_url)

    market_depth_url = 'http://www.nepalstock.com/marketdepth'
    scrip_code = ScripCode(market_depth_url)

    return AddScripCode(company_detail, scrip_code)
    

def md_data(scrip_symbol):
    company_dict = create_company_dict()
    scrip_code = company_dict[scrip_symbol][2]
    url = marketdepth_url_resolver(scrip_code)
    scrip_depth = scrape_market_depth(scrip_symbol, url)
    return scrip_depth


def Merge(dict1, dict2, dict3):
    return {k:v for d in [dict1,dict2,dict3] for k,v in d.items()}

def md_data_additional(scrip_symbol):
    md_data_minimal = md_data(scrip_symbol)
    additional_data_scrip = fs_data(scrip_symbol,True)
    add_data = fs_data('',True)
    additional_data_nepse = {}
    for key, value in add_data.items():
        additional_data_nepse['NEPSE ' + key] = value
    return Merge(md_data_minimal, additional_data_scrip, additional_data_nepse)

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
