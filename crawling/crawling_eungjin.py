from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv


def fetch_each_page_until_has_no_item(category_url, start_page_number):
	res = []
	page_number = start_page_number

	end = False
	last_id = 0
	while not end:
		parsed_item_list = parse_page(category_url, page_number, last_id)
		if not has_item(parsed_item_list):
			end = True
		else:
			page_number += 1
			last_id = parsed_item_list[-1]['id']
			res += parsed_item_list
	return res


def has_item(li):
	return True if li else False


def parse_page(category_url, page_number, last_id):
	page_number_query = '&page=+' + str(page_number)
	html = urlopen(category_url + page_number_query)
	soup = BeautifulSoup(html.read(), "lxml")
	category = trim(soup.body.h2.get_text())
	items_html = soup.body.find("div", class_="pr_desc wli4")
	item_html_list = items_html.find_all('li')

	res = []
	res = parse_item_list(item_html_list, category, last_id)
	return res


def parse_item_list(item_html_list, category, last_id):
	res = []
	for index, item in enumerate(item_html_list, int(last_id)+1):
		res.append(parse_item(index, category, item))
	return res


def parse_item(index, category, item_html):
	parsed_item = {}

	parsed_item['id'] = str(index)
	parsed_item['category'] = category
	parsed_item['link'] = item_html.a['href']
	parsed_item['img'] = item_html.img['src']
	parsed_item['title'] = item_html.find("dd", class_='pname').get_text()
	parsed_item['price'] = item_html.find("dd", class_='price').p.get_text()

	res = {}
	res = trim_each_attributes(parsed_item)

	return res


def trim_each_attributes(input_dict):
	res = {}
	for key, value in input_dict.items():
		trimed_value = trim(value)
		res[key] = trimed_value
	return res


def trim(text):
	text = re.sub('\s+', '', text)
	if text == '':
		text = 'default'
	return text


def printer(li):
	for i in li:
		print(i)


def writer(li):
	f = open('output''.csv', 'w', encoding='utf-8', newline='')
	wr = csv.writer(f)
	wr.writerow(list(li[0].keys()))
	for item in li:
		wr.writerow(list(item.values()))
	f.close()

if __name__ == "__main__":
	category_range = list(range(6001, 6008))
	base_url =  'http://branch1.nowpick.co.kr/shop/list.php?cate=00'

	res = []
	for num in category_range:
		category_url = base_url + str(num)
		start_page_number = 1
		res += fetch_each_page_until_has_no_item(category_url, start_page_number)

	writer(res)