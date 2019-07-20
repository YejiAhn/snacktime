from django.urls import path
from productpage import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.show, name='show'),
    path('new/', views.new, name='new'),
    path('<int:pk>/like/', views.product_like, name='like'),
    path('category/<str:ct>/', views.category, name='category'),
]