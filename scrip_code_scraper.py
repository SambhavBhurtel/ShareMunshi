#! .\\venv\\Scripts\\python.exe

from bs4 import BeautifulSoup
import requests

# Reading the HTML data from NEPSE as text
source = requests.get('http://www.nepalstock.com/marketdepth').text
soup = BeautifulSoup(source, 'lxml')

# Parsing the all the options tags for Scrip Symbol and Code.
options = soup.find('select', class_='form-control', id='StockSymbol_Select1')
scrips = options.find_all('option')

# Storing the parsed data in a dictionary.
company_data = {}
for scrip in scrips:
    company_symbol = scrip.text
    company_code = scrip['value']
    company_data[company_symbol] = company_code

del company_data['Choose Symbol']

print(company_data)