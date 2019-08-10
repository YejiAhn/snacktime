##################
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import time


driver = webdriver.Firefox(executable_path='/Users/Sangwoo/Desktop/멋쟁이 사자처럼/snack time/geckodriver')
base_url =  'http://www.7-eleven.co.kr/product/bestdosirakList.asp'
group= ['PB']
PB = '3'

url='http://www.7-eleven.co.kr'

end=False
prod_id=1
all_prod_list=[['id','category','image','name','price','PB']]
  
category_url = base_url
driver.get(category_url)
category=''

for i in range(33):
    driver.execute_script('fncMore('')')
    time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
prod_list= soup.find("div", {"class": "dosirak_list dosirak_list_01 dosirak_list_01_02"})
name_list = prod_list.select('.name')
price_list = prod_list.select('.price > span')
img_list = prod_list.select('.pic_product')
if len(name_list)==len(price_list) and len(price_list)==len(img_list):
    for j in range(len(name_list)):
        temp_list=[prod_id, category, url+img_list[j].img['src'], name_list[j].text, price_list[j].text+'원', PB]
        prod_id=prod_id+1
        all_prod_list.append(temp_list)
else:
    print("not same number error")
        

f = open('7''.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
for info in range(prod_id):
    wr.writerow(all_prod_list[info])
f.close()