############################
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import time


driver = webdriver.Firefox(executable_path='/Users/Sangwoo/Desktop/멋쟁이 사자처럼/snack time/geckodriver')
base_url =  'https://www.ministop.co.kr/MiniStopHomePage/page/guide/list'
group= ['도시락', '주먹밥', '김밥', '샌드위치', '인기상품', '신상품', '햄버거','', 'PB']
PB = '0'
img_base_url = 'https://www.ministop.co.kr/MiniStopHomePage/page'
category_range = list(range(len(group)))
# sub_group_coord=[[('1',2),('3',3),('2',4)],[('4',2),('5',3),('6',4)],[('71',2),('7',3),('8',4)],[('9',2)],[('12',2),('10',3),('11',4)],[('13',2),('14',3),('15',4)]]
prod_id=1
# sub_group_page=[[1, 2, 1],[1, 1, 0],[8, 5, 8],[6],[14, 6, 9],[21, 1, 5]]
sub_group_page = [1, 1, 0, 2, 8, 9, 2, 0, 3]
all_prod_list=[['id','category','image','name','price','PB']]
for c in category_range:   
    if c==0:
        category_url = base_url + '.do'
    else:
        category_url = base_url + '_' + str(c+1) + '.do'
        if c==8:
            PB = '5'
    driver.get(category_url)
    time.sleep(5)
    category=group[c]
    click_n=sub_group_page[c]
    for i in range(click_n):
        driver.find_element_by_xpath("//a[@class='pr_more']").click()
        time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    prod_list= soup.find("div", {"class": "section_tab_content"})
    name_list = prod_list.select('ul > li')
    price_list = prod_list.select('ul > li > a > p > strong')
    img_list = prod_list.select('ul > li')    
    if len(name_list)==len(price_list) and len(price_list)==len(img_list):
        for j in range(len(name_list)):
            temp_list=[prod_id, category, img_base_url+img_list[j].img['src'][2:], name_list[j].img['alt'], price_list[j].text+'원', PB]
            prod_id=prod_id+1
            all_prod_list.append(temp_list)
    else:
        print("not same number error")
        

f = open('ministop''.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
for info in range(prod_id):
    wr.writerow(all_prod_list[info])
f.close()