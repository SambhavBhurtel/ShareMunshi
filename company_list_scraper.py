#! .\\venv\\Scripts\\python.exe

from bs4 import BeautifulSoup
import requests

# Reading the HTML data from NEPSE as text
source = requests.get("""http://www.nepalstock.com/company/index/1?stock-name=&stock-symbol=&sector-id=&_limit=500
""").text
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
    data
    companies[data[1].text] = [data[0].text[9:-4], data[2].text]

print(companies)
