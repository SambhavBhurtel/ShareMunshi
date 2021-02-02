#! .\\venv\\Scripts\\python.exe
import requests
from bs4 import BeautifulSoup

'''
Code to scrape the scrip code of stock
'''
def ScripCode(url):
    # Reading the HTML data from NEPSE as text
    source = requests.get(url).text
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

    return company_data

def AddScripCode(all_data, code):
    for key, value in all_data.items():
        all_data[key].append(code[key])
    print(all_data)