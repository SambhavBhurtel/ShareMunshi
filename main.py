#! .\\venv\\Scripts\\python.exe

from Scrapper.ScrapeCode import ScripCode, AddScripCode
from Scrapper.ScrapeName import StockName
from Scrapper.ScrapeMD import marketdepth_url_resolver, scrape_market_depth


def create_company_dict():
    company_detail_url = 'http://www.nepalstock.com/company/index/1?stock-name=&stock-symbol=&sector-id=&_limit=500'
    company_detail = StockName(company_detail_url)

    market_depth_url = 'http://www.nepalstock.com/marketdepth'
    scrip_code = ScripCode(market_depth_url)

    return AddScripCode(company_detail, scrip_code)
    

def show_market_depth(scrip_symbol):
    company_dict = create_company_dict()
    scrip_code = company_dict[scrip_symbol][2]
    url = marketdepth_url_resolver(scrip_code)
    scrip_depth = scrape_market_depth(scrip_symbol, url)
    return scrip_depth


scrip_symbol = input("Enter Scrip Code: ")
print(show_market_depth(scrip_symbol))