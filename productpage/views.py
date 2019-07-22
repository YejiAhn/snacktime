from django.shortcuts import render
from reviewpage.models import Product, Save, Like, Review
from django.shortcuts import redirect
from django.contrib.auth.models import User

import pandas as pd
import numpy as np
import collections

# Create your views here.

def index(request):
    products = Product.objects.all()
    for product in products:
        product.get_rating()
        product.update_emoticon()
    categories = ['전체','간편식사', '즉석조리','과자류','아이스크림', '식품','음료']
    return render(request, 'productpage/index.html', {'products': products, 'categories':categories})

def new(request):
    CU = pd.read_csv('productpage/productlist/CU.csv') 
    emart24 = pd.read_csv('productpage/productlist/emart24.csv') 
    all_product = pd.merge(CU, emart24)
    i_category = 1
    i_image = 2
    i_name = 3
    i_price = 4
    i_PB = 5
    for i in range(len(all_product)):
        store_name=all_product.iloc[i,i_PB]
        PBstore=stores(store_name)
        Product.objects.create(name=all_product.iloc[i,i_name], price=all_product.iloc[i,i_price], category=all_product.iloc[i,i_category], photo=all_product.iloc[i,i_image], PBstore=PBstore)
    return redirect('/products/')


def show(request, id):
    if request.method == 'GET':
        product= Product.objects.get(id=id)
        product.get_rating()
        product.update_emoticon()
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

def category(request, ct):
    if ct=='전체':
        return redirect('/products/')
    categories = ['전체', '간편식사', '즉석조리','과자류','아이스크림', '식품','음료']
    products= Product.objects.all().filter(category = ct)[:10]
    return render(request, 'productpage/category.html', {'products': products, 'categories':categories})

def stores(val):
    return {
        'cu': 'https://membership.bgfretail.com/membership/pc/images/family_site_02.png',
        'gs25': '',
        'emart24': 'https://www.emart24.co.kr/images/introduce/img_visual_bi.gif',
        'seveneleven': '',
        'ministop': '',
        '0': ''
    }.get(val,'')


def detail(request):
    return render(request, 'productpage/detail.html')

    
# def get_product_rating(id):
#     product = Product.objects.get(id=id)
#     review_list = product.review_set.all()
#     sum_rating = 0
#     if review_list.count()>0 :
#         for review in review_list:
#             sum_rating += review.rating
#         product_rating = sum_rating / review_list.count()
#     else : product_rating = 0

#     return product_rating