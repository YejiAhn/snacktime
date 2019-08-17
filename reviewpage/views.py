from django.shortcuts import render
from .models import Review, Like, Save
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from productpage.views import product_save

# Create your views here.

# def index(request):
#    if request.method == 'GET': # index
#        reviews = Review.objects.all()
#        return render(request, 'reviewpage/index.html', {'reviews': reviews})

#    elif request.method == 'POST': # create
#        content = request.POST['content']        
#        photo = request.FILES.get('photo', False)
        
#         ## 수정: 리뷰레이팅 추가
#        review_rating = request.POST['review_rating']
#        Review.objects.create(review_rating=review_rating, content=content, author = request.user, photo=photo)
#        return redirect('/reviews')

def index(request):
    if request.method == 'GET':
        sort = request.GET.get('sort','')
        if sort == 'likes':
            reviews = Review.objects.all()
            
            reviews.order_by('-like_count','-updated_at')
            return render(request, 'reviewpage/index.html', {'reviews': reviews})
        elif sort == 'mypost':
            user = request.user
            reviews = Review.objects.filter(name_id = user).ordered_by('-updated_at')
            return render(request, 'reviewpage/index.html', {'reviews': reviews})
        else:
            reviews = Review.objects.order_by('-updated_at')
            return render(request, 'reviewpage/index.html', {'reviews': reviews})
    elif request.method == 'POST': # create
        content = request.POST['content']
        photo = request.FILES.get('photo', False)
        review_rating = request.POST['review_rating']
        Review.objects.create(review_rating=review_rating, content=content, author = request.user, photo=photo)
        return redirect('/reviews')

def new(request):
    return render(request, 'reviewpage/new.html')

def show(request, id):
    if request.method == 'GET': # show
        review = Review.objects.get(id=id)

        return render(request, 'reviewpage/show.html', {'review': review})

    elif request.method == 'POST': # update
        review = Review.objects.get(id=id)
        # Need to implement these data.
        # product, author, liked_users

        content = request.POST['content']
        review_rating = request.POST['review_rating']
        # photo = request.FILES['photo']:

        review.content = content
        review.review_rating = review_rating

        review.save()
        ### 수정: 리뷰 점수도 수정받기

        # if review.review_rating != request.POST['review_rating']:
        #     review.review_rating = request.POST['review_rating']
        #     review.save()
        #     product = review.product 
        #     product.get_rating()  
        #     product.calc_rank_point()

        return redirect('/reviews')

def delete(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect('/reviews')

def edit(request, id):
    review = Review.objects.get(id=id)
    return render(request, 'reviewpage/edit.html', {'review': review})

def review_like(request, pk):
    review = Review.objects.get(id = pk)
    like_list = review.like_set.filter(user_id = request.user.id)
    if like_list.count() > 0:
        review.like_set.get(user_id = request.user.id).delete()
    else:
        Like.objects.create(user_id = request.user.id, review_id = review.id)
    review.update_date()
    print('log')
    print(review.like_count)
    return redirect('/reviews')

def review_save(request, pk):
    review = Review.objects.get(id = pk)
    save_list = review.save_set.filter(user_id = request.user.id)
    if save_list.count() > 0:
        review.save_set.get(user_id = request.user.id).delete()
    else:
        Save.objects.create(user_id = request.user.id, reiew_id = review.id)
    return redirect('/reviews')

def review_category(request, ct, pb):

    CATEGORY_CODES = {
        00: '전체',

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
        reviews = Review.objects.all()
    else: 
        reviews = Review.objects.all().filter(category_code = ct)
    
    if pb != 0: 
        reviews = reviews.filter(pb_store_code = pb)

    return render(request, 'reviewpage/index.html', {'products': products, 'categories':MAIN_CATEGORY, 'sub_categories':SUB_CATEGORY,'pb_stores':PB_STORE_CODES,'ct':ct, 'pb':pb})