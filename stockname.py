import requests
from lxml import etree
from bs4 import BeautifulSoup

mainurl = "http://www.nepalstock.com/company/"


index = 1
data = []
# To check the end of the page
check = []
flag = True
while flag:
    url = mainurl + "index/" + str(index)
    website = requests.get(url).content
    soup = BeautifulSoup(website, "html.parser")
    pageData = soup.find(id = "company-list").find_all("tr")
    for i in range(20):
        try:
            stockData = pageData[i+2].find_all("td")
            stockName = stockData[2].text
            stockSymbol = stockData[3].text
            stockCategory = stockData[4].text
            stockDataList = [stockName, stockSymbol, stockCategory]
            if stockDataList[1] in check:
                flag = False
            else:
                data.append(stockDataList)
            check.append(stockSymbol)
        except:
            print("End of data")
    index = index + 1

print(len(data))
    

    
    
    

