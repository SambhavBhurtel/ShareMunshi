#! .\\venv\\Scripts\\python.exe

import requests
from bs4 import BeautifulSoup

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

