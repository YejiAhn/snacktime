from django.shortcuts import render
from .models import Review, Like, Save
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
        Review.objects.create(review_rating=1, content=content, author = request.user, photo=photo)
        return redirect('/reviews')

#def index(request):
#    if request.method == 'GET':
#        sort = request.GET.get('sort','')
#        if sort == 'likes':
#            reviews = Review.objects.annotate(like_count=Count('likes')).order_by('like_count','updated_at')
#            return render(request, 'reviewpage/index.html', {'reviews': reviews})
#        else:
#            reviews = Review.objects.order_by('updated_at')
#            return render(request, 'reviewpage/index.html', {'reviews': reviews})
#    elif request.method == 'POST': # create
#        content = request.POST['content']
#        photo = request.FILES.get('photo', False)
#        Review.objects.create(review_rating=1, content=content, author = request.user, photo=photo)
#        return redirect('/reviews')

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
    return redirect('/reviews')

def review_save(request, pk):
    review = Review.objects.get(id = pk)
    save_list = review.save_set.filter(user_id = request.user.id)
    if save_list.count() > 0:
        review.save_set.get(user_id = request.user.id).delete()
    else:
        Save.objects.create(user_id = request.user.id, reiew_id = review.id)
    return redirect('/reviews')
