import requests
from bs4 import BeautifulSoup

'''
Code to scrape the stock name
'''

def StockName(url):
    # Reading the HTML data from NEPSE as text
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    company_table = soup.find('table', class_='my-table table')
    company_list = company_table.find_all('tr', class_=lambda x:x != 'unique', align=lambda x:x !='right')
    company_data = []

    for company_detail in company_list:
        all_tds = company_detail.find_all('td')
        selected_tds = all_tds[2:5]
        company_data.append(selected_tds)

    del company_data[-1]
    
    companies = {}
    for data in company_data:
        companies[data[1].text] = [data[0].text.strip(), data[2].text]

    return companies


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
    return (all_data)

    
    
    

