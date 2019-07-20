from django.urls import path
from productpage import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.show, name='show'),
    path('new/', views.new, name='new'),
    path('<int:pk>/save/', views.product_save, name='save'),
    path('category/<str:ct>/', views.category, name='category'),
    path('detail', views.detail, name='detail'),
]