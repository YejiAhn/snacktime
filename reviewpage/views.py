# from django.shortcuts import render
# from .models import Review
# from django.shortcuts import redirect
# from django.contrib.auth.models import User

# # Create your views here.
# def index(request):
#     if request.method == 'GET': # index
#         reviews = Review.objects.all()
#         return render(request, 'reviewpage/index.html', {'reviews': reviews})
#     elif request.method == 'POST': # create
#         content = request.POST['content']
#         photo = request.FILES.get('photo', False)
#         Review.objects.create(content=content, author = request.user, photo=photo)
#         return redirect('/reviews')

# def new(request):
#     return render(request, 'reviewpage/new.html')

# def show(request, id):
#     if request.method == 'GET': # show
#         review = Review.objects.get(id=id)
#         return render(request, 'reviewpage/show.html', {'review': review})
#     elif request.method == 'POST': # update
#         review = Review.objects.get(id=id)
#         content = request.POST['content']
#         review.content = content
#         review.save()
#         return redirect('/reviews')

# def delete(request, id):
#     review = Review.objects.get(id=id)
#     review.delete()
#     return redirect('/reviews')

# def edit(request, id):
#     review = Review.objects.get(id=id)
#     return render(request, 'reviewpage/edit.html', {'review': review})