##################
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import time


driver = webdriver.Firefox(executable_path='/Users/Sangwoo/Desktop/멋쟁이 사자처럼/snack time/geckodriver')
base_url =  'http://cu.bgfretail.com/product/pb.do?category=product&depth2=1&sf=N'
group= ['PB']
PB = '1'
prod_id=1
category_url = base_url
driver.get(category_url)
for i in range(5):
    driver.execute_script("nextPage(1);")
    time.sleep(5)
all_prod_list= [['id','name','PB']]
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
prod_list= soup.find("div", {"class": "prodListWrap"})
name_list = prod_list.select('.prodName')
for j in range(len(name_list)):
    temp_list=[prod_id, name_list[j].text, PB]
    prod_id=prod_id+1
    all_prod_list.append(temp_list)
    
f = open('cu_PB''.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
for info in range(prod_id):
    wr.writerow(all_prod_list[info])
f.close()