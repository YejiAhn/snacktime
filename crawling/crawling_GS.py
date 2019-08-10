# error not fixed

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time



driver = webdriver.Chrome(executable_path="C:\Workspace\chromedriver")
driver.implicitly_wait(3)
base_url= 'http://gs25.gsretail.com/gscvs/ko/products/youus-freshfood'

group = ['음료/커피', '유제품', '과자/간식', '라면/가공제품', '생활용품', '도시락', '김밥/주먹밥', '햄버거/샌드위치', '간편식']
PB = 'GS'
#category_range = list(range(len(group)))
all_prod_list=[['id','category','image','name','price','PB']]
prod_id=1

driver.get(base_url)
<<<<<<< HEAD
time.sleep(3)
element = driver.find_element_by_id('productSnack')
element.click()

time.sleep(3)
for n in range(4):
    category = '간편식'
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #divs = driver.find_elements_by_class_name('prod_box')
        
    #products = soup.select
    prod_list= soup.find("div", {"class": "tab_cont on"})
    name_list = prod_list.select('.tit')
    price_list = prod_list.select('.cost')
    img_list = prod_list.select('.img')
    if len(name_list)==len(price_list) and len(price_list)==len(img_list):
        
        for j in range(len(name_list)):
            if str(img_list[j]).find('src') != -1:
                img = img_list[j].img['src']
            else:
                print(str(img_list[j]))
                img = ''
                
            temp_list=[prod_id, category, img, name_list[j].text, price_list[j].text, PB]
            prod_id=prod_id+1
            all_prod_list.append(temp_list)
    element2 = driver.find_element_by_class_name('next')
    element2.click()
    time.sleep(3)


f = open('gs_meal''.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
for info in range(prod_id):
    wr.writerow(all_prod_list[info])
f.close()
