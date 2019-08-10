from django.shortcuts import render
from reviewpage.models import Product, Save, Like, Review
from django.shortcuts import redirect
from django.contrib.auth.models import User

import pandas as pd
import numpy as np

# Create your views here.

def index(request):
    products = Product.objects.all()
    ### 수정: Product model의 업데이트는 리뷰 작성시에 하는걸로!
    # for product in products:
    #     product.get_rating()
    #     product.update_emoticon()
    CATEGORY_CODES = {
        00: 'undefined',

        10: 'icecream',
        11: 'icecream_bar',
        12: 'icecream_cone',

        20: 'liquid',
        21: 'liquid_coffee',
        22: 'liquid_dairy',
        23: 'liquid_soda',

        30: 'snack',

        40: 'sweets',
        41: 'sweets_chocolate',
        42: 'sweets_candy',
        43: 'sweets_gum',
        44: 'sweets_jelly',

        50: 'convenient',
        51: 'convenient_gimbab',
        52: 'convenient_sandwich',
        53: 'convenient_dosirak',

        60: 'ramen',

        70: 'alcohol',
        71: 'alcohol_beer',
        72: 'alcohol_soju',

        80: 'bread/dessert',
        81: 'dessert_bread',
        82: 'dessert_cake',

        90: 'etc'
    }
    PB_STORE_CODES = {
        0: 'is_not_pb',
        1: 'cu',
        2: 'gs25',
        3: 'emart24',
        4: 'seveneleven',
        5: 'ministop',
    }
    MAIN_CATEGORY = dict()
    for (key, value) in CATEGORY_CODES.items():
        if key%10 ==0 : 
            MAIN_CATEGORY[key] = value; 
    return render(request, 'productpage/index.html', {'products': products, 'categories':MAIN_CATEGORY, 'pb_stores':PB_STORE_CODES,'ct':0, 'pb':0})

### 수정: 바뀐 모델에 맞게 수정. 새로운 데이터 베이스를 입력해야 함.
def new(request):
    # CU = pd.read_csv('productpage/productlist/CU.csv') 
    # emart24 = pd.read_csv('productpage/productlist/emart24.csv') 
    # all_product = pd.merge(CU, emart24)
    all_product = pd.read_csv('productpage/productlist/numbering_cu.csv')
    i_category = 1
    i_image = 2
    i_name = 3
    i_price = 4
    i_PB = 5
    for i in range(len(all_product)):
        Product.objects.create(name=all_product.iloc[i,i_name], price=all_product.iloc[i,i_price], category_code=all_product.iloc[i,i_category], photo=all_product.iloc[i,i_image], pb_store_code=all_product.iloc[i,i_PB])
    return redirect('/products')

def seed(request, id):
    product = Product.objects.get(id=id)
    count = int(request.POST['count'])
    taste = request.POST['taste']
    product.seed(count, taste)
    product.update_rate()
    return redirect('/products/'+str(id))


def show(request, id):
    ### 수정 : 리뷰 작성시 여기로 올듯. GET->POST
    if request.method == 'POST':
        product= Product.objects.get(id=id)
        product.update_rate()
        reviews = product.review_set.all()
        review_count = reviews.count()
        rates_num = [
            reviews.filter(review_rating = 5).count(),
            reviews.filter(review_rating = 4).count(),
            reviews.filter(review_rating = 3).count(),
            reviews.filter(review_rating = 2).count(),
            reviews.filter(review_rating = 1).count()
        ]
        return render(request, 'productpage/show.html', {'product':product, 'rates' : rates_num, 'count' : review_count})
    
    ### else 문 작성하기
    elif request.method == 'GET':
        product= Product.objects.get(id=id)
        # product.update_rate() # GET에션 업데이트 없음.
        reviews = product.review_set.all()
        review_count = reviews.count()
        rates_num = [
            reviews.filter(review_rating = 5).count(),
            reviews.filter(review_rating = 4).count(),
            reviews.filter(review_rating = 3).count(),
            reviews.filter(review_rating = 2).count(),
            reviews.filter(review_rating = 1).count()
        ]
        return render(request, 'productpage/show.html', {'product':product, 'rates' : rates_num, 'count' : review_count})
    

    return render(request, 'productpage/show.html', {'product':product})


    
def product_save(request, pk):
    product = Product.objects.get(id = pk)
    save_list = product.save_set.filter(user_id = request.user.id)
    if save_list.count() > 0:
        product.save_set.get(user_id = request.user.id).delete()
    else:
        Save.objects.create(user_id = request.user.id, product_id = product.id)
    next = request.META['HTTP_REFERER']
    return redirect(next)

def category(request, ct, pb):
    # if ct==00:
    #     return redirect('/products/category/00/0')
    CATEGORY_CODES = {
        00: 'undefined',

        10: 'icecream',
        11: 'icecream_bar',
        12: 'icecream_cone',

        20: 'liquid',
        21: 'liquid_coffee',
        22: 'liquid_dairy',
        23: 'liquid_soda',

        30: 'snack',

        40: 'sweets',
        41: 'sweets_chocolate',
        42: 'sweets_candy',
        43: 'sweets_gum',
        44: 'sweets_jelly',

        50: 'convenient',
        51: 'convenient_gimbab',
        52: 'convenient_sandwich',
        53: 'convenient_dosirak',

        60: 'ramen',

        70: 'alcohol',
        71: 'alcohol_beer',
        72: 'alcohol_soju',

        80: 'bread/dessert',
        81: 'dessert_bread',
        82: 'dessert_cake',

        90: 'etc'
    }
    PB_STORE_CODES = {
        0: 'is_not_pb',
        1: 'cu',
        2: 'gs25',
        3: 'emart24',
        4: 'seveneleven',
        5: 'ministop',
    }
    MAIN_CATEGORY = dict()
    SUB_CATEGORY = dict()

    for (key, value) in CATEGORY_CODES.items():
        if key%10 ==0 : 
            MAIN_CATEGORY[key] = value

        elif key//10 == ct//10: 
            SUB_CATEGORY[key] = value   
    if ct == 0:
        products = Product.objects.all()
    else: 
        products = Product.objects.all().filter(category_code = ct)
    
    if pb != 0: 
        products = products.filter(pb_store_code = pb)

    
    # elif pb == 0:   
    #     products= Product.objects.all().filter(category_code = ct)#[:20] # 보여줄 개수를 정하려면 추가
    # else : 
    #     products= Product.objects.all().filter(category_code = ct).filter(pb_store_code = pb)#[:20] # 보여줄 개수를 정하려면 추가
    return render(request, 'productpage/category.html', {'products': products, 'categories':MAIN_CATEGORY, 'sub_categories':SUB_CATEGORY,'pb_stores':PB_STORE_CODES,'ct':ct, 'pb':pb})

### 수정: 모델에서 코드를 정했으니 삭제해도 될듯. 단 저장된 이미지 주소를 연동하는 건 고려해봐야 함.
# def stores(val):
#     return {
#         'cu': 'https://membership.bgfretail.com/membership/pc/images/family_site_02.png',
#         'gs25': '',
#         'emart24': 'https://www.emart24.co.kr/images/introduce/img_visual_bi.gif',
#         'seveneleven': '',
#         'ministop': '',
#         '0': ''
#     }.get(val,'')


def detail(request):
    return render(request, 'productpage/detail.html')

