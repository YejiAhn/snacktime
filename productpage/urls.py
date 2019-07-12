from django.urls import path
from productpage import views

urlpatterns = [
    path('', views.index, name='index'),
]