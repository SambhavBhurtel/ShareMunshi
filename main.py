from Scrapper.ScrapeCode import ScripCode, AddScripCode
from Scrapper.ScrapeName import StockName

company_detail_url = 'http://www.nepalstock.com/company/index/1?stock-name=&stock-symbol=&sector-id=&_limit=500'
company_detail = StockName(company_detail_url)

market_depth_url = 'http://www.nepalstock.com/marketdepth'
scrip_code = ScripCode(market_depth_url)

finaldata = AddScripCode(company_detail, scrip_code)
