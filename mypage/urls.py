from django.urls import path
from mypage import views

urlpatterns = [
    path('', views.index, name='index'),
]