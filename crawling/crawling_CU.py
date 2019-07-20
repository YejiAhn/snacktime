'''
import requests
from bs4 import BeautifulSoup

r = requests.get('http://cu.bgfretail.com/product/pb.do?category=product&depth2=1')
html = r.text
f = open('cu_prod_datapy.txt', 'w')

# print(html)

# print(r.status_code)
# print(r.headers['Content-Type'])
# print(r.encoding)
# print(r.ok)

soup = BeautifulSoup(html, 'html.parser')
titles = soup.select('.prodName')
for title in titles:
    print(title.text)
'''
############################
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import time


driver = webdriver.Firefox(executable_path='/Users/Sangwoo/Desktop/멋쟁이 사자처럼/snack time/geckodriver')
base_url =  'http://cu.bgfretail.com/product/product.do?category=product&depth2=4&depth3='
group= ['간편식사', '즉석조리','과자류','아이스크림', '식품','음료']
PB = 'cu'

# sub_group=[]
# sub_group.append(['도시락','샌드위치햄버거','주먹밥김밥'])
# sub_group.append(['튀김', '베이커리', '즉석커피'])
# sub_group.append(["스낵비스켓", "빵디저트", "껌초콜릿캔디"])
# sub_group.append(['아이스크림'])
# sub_group.append(['가공식사', '안주류', '식재료'])
# sub_group.append(['음료', '아이스드링크', '유제품'])
category_range = list(range(len(group)))
end=False
sub_group_coord=[[('1',2),('3',3),('2',4)],[('4',2),('5',3),('6',4)],[('71',2),('7',3),('8',4)],[('9',2)],[('12',2),('10',3),('11',4)],[('13',2),('14',3),('15',4)]]
prod_id=1
sub_group_page=[[1, 2, 1],[1, 1, 0],[8, 5, 8],[6],[14, 6, 9],[21, 1, 5]]
all_prod_list=[['id','category','image','name','price','PB']]
for c in category_range:   
    category_url = base_url + str(c+1)
    driver.get(category_url)
    category=group[c]
    sub_category_range=list(range(len(sub_group_coord[c])))
    for s in sub_category_range:
		# sub_category=sub_group[c][s]
        go_sub = 'gosub'+str(sub_group_coord[c][s])+';'
        driver.execute_script(go_sub)
        time.sleep(5)
        for i in range(sub_group_page[c][s]):
            driver.execute_script("nextPage(1);")
            time.sleep(5)
            location=[ c+1 , s+1 , i+1 ]
            print(location)	
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        prod_list= soup.find("div", {"class": "prodListWrap"})
        name_list = prod_list.select('.prodName')
        price_list = prod_list.select('.prodPrice')
        img_list = prod_list.select('.photo')
        if len(name_list)==len(price_list) and len(price_list)==len(img_list):
            for j in range(len(name_list)):
                temp_list=[prod_id, category, img_list[j].img['src'], name_list[j].text, price_list[j].text, PB]
                prod_id=prod_id+1
                all_prod_list.append(temp_list)
        else:
            print("not same number error")
        

f = open('cu''.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
for info in range(prod_id):
    wr.writerow(all_prod_list[info])
f.close()