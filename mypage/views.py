from django.shortcuts import render
from reviewpage.models import Review, Like, Product
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    user = request.user
    user_id = request.user.id
    reviews = Review.objects.filter(author_id = user_id)
    saved = Product.objects.filter(saved_users = request.user)
    return render(request, 'mypage/index.html', {
        'user': user,
        'eaten': reviews,
        'wish' : saved
    })