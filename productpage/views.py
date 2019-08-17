#-*- coding:utf-8 -*-


from django.shortcuts import render
from reviewpage.models import Product, Save, Like, Review
from django.shortcuts import redirect
from django.contrib.auth.models import User

import pandas as pd
import numpy as np
import time
from collections import OrderedDict



# Create your views here.

def index(request):

    if request.user.is_authenticated:

        products = Product.objects.all()
        ### 수정: Product model의 업데이트는 리뷰 작성시에 하는걸로!
        # for product in products:
        #     product.get_rating()
        #     product.update_emoticon()
        CATEGORY_CODES = {
            00: '전체',

            10: '아이스크림',
            11: '바',
            12: '콘',

            20: '음료',
            21: '커피',
            22: '유제품',
            23: '탄산',

            30: '과자',

            40: '달다구리',
            41: '초콜렛',
            42: '캔디',
            43: '껌',
            44: '젤리',

            50: '간편식사',
            51: '김밥',
            52: '샌드위치',
            53: '도시락',

            60: '라면',

            70: '주류',
            71: '맥주',
            72: '소주',

            80: '빵/디저트',
            81: '빵',
            82: '케이크',

            90: '기타'
        }
        PB_STORE_CODES = {
            0: 'is_not_pb',
            1: 'CU',
            2: 'GS25',
            3: 'emart24',
            4: '세븐일레븐',
            5: '미니스톱',
        }
        MAIN_CATEGORY = dict()
        for (key, value) in CATEGORY_CODES.items():
            if key%10 ==0 : 
                MAIN_CATEGORY[key] = value; 
        return render(request, 'productpage/category.html', {'products': products, 'categories':MAIN_CATEGORY, 'pb_stores':PB_STORE_CODES,'ct':0, 'pb':0})
    
    else:
        return render(request, 'accounts/home.html')

### 수정: 바뀐 모델에 맞게 수정. 새로운 데이터 베이스를 입력해야 함.
def new(request):
    # CU = pd.read_csv('productpage/productlist/CU.csv') 
    # emart24 = pd.read_csv('productpage/productlist/emart24.csv') 
    # all_product = pd.merge(CU, emart24)
    all_product = pd.read_csv('productpage/productlist/CU.csv')
    i_category = 1
    i_image = 2
    i_name = 3
    i_price = 4
    i_PB = 5
    for i in range(len(all_product)):
        Product.objects.create(name=all_product.iloc[i,i_name], price=all_product.iloc[i,i_price], category_code=all_product.iloc[i,i_category], photo=all_product.iloc[i,i_image], pb_store_code=str(all_product.iloc[i,i_PB]))
        time.sleep(0.1)
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
    
        content = request.POST['content']
        photo = request.FILES.get('photo', False)
        review_rating = request.POST['review_rating']
    
        product = Product.objects.get(id=id)
     
        review = Review.objects.create(product=product, review_rating=review_rating, content=content, author=request.user, photo=photo)
        review.save()
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
        00: '전체',

        1: '아이스크림',
        10: '기타',
        11: '바',
        12: '콘',

        2: '음료',
        20: '기타',
        21: '커피',
        22: '유제품',
        23: '탄산',

        3: '과자',
        30: '기타',

        4: '달다구리',
        40: '기타',
        41: '초콜렛',
        42: '캔디',
        43: '껌',
        44: '젤리',

        5: '간편식사',
        50: '기타',
        51: '김밥',
        52: '샌드위치',
        53: '도시락',

        6: '라면',
        60: '기타',

        7: '주류',
        70: '기타',
        71: '맥주',
        72: '소주',

        8: '빵/디저트',
        80: '기타',
        81: '빵',
        82: '케이크',

        9: '기타'
    }
    PB_STORE_CODES = {
        0: 'is_not_pb',
        1: 'CU',
        2: 'GS25',
        3: 'emart24',
        4: '세븐일레븐',
        5: '미니스톱',
    }
    

    MAIN_CATEGORY = dict()
    # SUB_CATEGORY = OrderedDict()
    SUB_CATEGORY = dict()

    search = request.GET.get('search', '')

    for (key, value) in CATEGORY_CODES.items():
        if key < 10 : 
            MAIN_CATEGORY[key] = value

        elif key//10 == ct or key//10 == ct//10: 
            SUB_CATEGORY[key] = value
    

    sorted_sub = sorted(SUB_CATEGORY.items(), key=lambda kv: kv[0], reverse=True)
   
    key_ct = ct
    if ct == 0:
        products = Product.objects.all()
    elif ct < 10 :
        products = []
        total = Product.objects.all()
        for product in total:
            if( int(product.category_code)//10 == int(ct)):
                products.append(product)
    else: 
        key_ct = int(ct / 10)
        products = Product.objects.all().filter(category_code = ct)
    
    if pb != 0: 
        products = products.filter(pb_store_code = pb)
    print(search)
    if search: 
        products = products.filter(name__icontains=search)


    # elif pb == 0:   
    #     products= Product.objects.all().filter(category_code = ct)#[:20] # 보여줄 개수를 정하려면 추가
    # else : 
    #     products= Product.objects.all().filter(category_code = ct).filter(pb_store_code = pb)#[:20] # 보여줄 개수를 정하려면 추가
    return render(request, 'productpage/category.html', {'search' : search, 'products': products, 'categories':MAIN_CATEGORY, 'sub_categories': dict(sorted_sub), 'pb_stores':PB_STORE_CODES,'ct':ct, 'pb':pb, 'key_ct': key_ct})




def detail(request):
    return render(request, 'productpage/detail.html')