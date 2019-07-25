from django.shortcuts import render
from .models import Review
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    if request.method == 'GET': # index
        reviews = Review.objects.all()
        return render(request, 'reviewpage/index.html', {'reviews': reviews})
    elif request.method == 'POST': # create
        content = request.POST['content']
        photo = request.FILES.get('photo', False)
        ### 수정: 리뷰레이팅 추가
        review_rating = request.POST['review_rating']
        ###
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
        content = request.POST['content']
        review.content = content
        review.save()
        ### 수정: 리뷰 점수도 수정받기
        if review.review_rating != request.POST['review_rating']:
            review.review_rating = request.POST['review_rating']
            review.save()
            product = review.product 
            product.get_rating()  
            product.calc_rank_point()

        return redirect('/reviews')

def delete(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect('/reviews')

def edit(request, id):
    review = Review.objects.get(id=id)
    return render(request, 'reviewpage/edit.html', {'review': review})