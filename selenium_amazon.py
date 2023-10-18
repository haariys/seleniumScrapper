from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_experimental_option("detach", True)
#options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#driver = webdriver.Chrome(service=Service('D:/chromedriver'))
driver.maximize_window()
driver.get("https://www.amazon.com")
driver.find_element(By.NAME, 'field-keywords').send_keys('dog cooling mat')
driver.find_element(By.NAME, 'field-keywords').send_keys(Keys.ENTER)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
quotes=[]
product_selector = soup.find_all('div', class_='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20')
print(len(product_selector))
#print(product_selector)
for i in product_selector:
    quote={}
    price=i.find('span',attrs={'class':'a-offscreen'})
    name=i.find('span', attrs={'class':'a-size-base-plus a-color-base a-text-normal'})
    if hasattr(price,'text'):
        quote['name']=name.text
        if '$' in price.text:
            quote['price']=price.text
        else:
            continue
        quotes.append(quote)
    else:
        continue
filename = 'D:/quotes.csv'
with open(filename, 'w', newline='',encoding="utf-8") as f:
    w = csv.DictWriter(f,['name','price'])
    w.writeheader()
    for quote in quotes:
        w.writerow(quote)
print('DONE')