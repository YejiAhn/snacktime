############################
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import time


driver = webdriver.Firefox(executable_path='/Users/Sangwoo/Desktop/멋쟁이 사자처럼/snack time/geckodriver')
base_url =  'https://www.emart24.co.kr/product/'
img_url = 'https://www.emart24.co.kr'
# group= ['간편식사', '즉석조리','과자류','아이스크림', '식품','음료']
PB = 'emart24'
group = ['간편식사','즉석조리','과자류','아이스크림', '식품']


category_range = list(range(len(group)))
end=False

sub_group_coord=[3,2,5,4,1]
prod_id=1
sub_group_page=[[1, 2, 1],[1, 1, 0],[8, 5, 8],[6],[14, 6, 9],[21, 1, 5]]
all_prod_list=[['id','category','image','name','price','PB']]
detail_url = ['emart24.asp', 'emart.asp','peacock.asp','freshFood.asp','sourcing.asp']
for c in category_range:   
    category_url = base_url + detail_url[c]
    driver.get(category_url)
    category=group[c]
    sub_category_range=list(range(sub_group_coord[c]))
    for s in sub_category_range:
        if s !=0:
            go_page = 'goPage'+'('+str(s+1)+');'
            driver.execute_script(go_page)
            time.sleep(1)
        location=[ c+1 , s+1]
        print(location)	
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        prod_list= soup.find("div", {"class": "tabContArea"})
        name_list = prod_list.select('.productDiv')
        price_list = prod_list.select('.price')
        img_list = prod_list.select('.productImg')
        if len(name_list)==len(price_list) and len(price_list)==len(img_list):
            for i in range(len(name_list)):
                temp_list=[prod_id, category, img_url+img_list[i].img['src'], name_list[i].text, price_list[i].text[2:], PB]
                prod_id=prod_id+1
                all_prod_list.append(temp_list)
        else:
            print("not same number error")
        

f = open('emart24''.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
for info in range(prod_id):
    wr.writerow(all_prod_list[info])
f.close()