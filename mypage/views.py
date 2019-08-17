from django.shortcuts import render
from reviewpage.models import Review, Like
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    user = request.user
    user_id = request.user.id
    reviewed = Review.objects.filter(author_id=user_id)
    liked = Like.objects.filter(user_id=user_id)
    return render(request, 'mypage/index.html', {
        'user': user,
        'review_count': len(reviewed),
        'like_count': len(liked)
    })