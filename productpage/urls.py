from django.urls import path
from productpage import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.show, name='show'),
    path('<int:id>/seed', views.seed, name='seed'),
    path('new/', views.new, name='new'),
    path('<int:pk>/save/', views.product_save, name='save'),
    path('category/<int:ct>/<int:pb>/', views.category, name='category'),
    path('category/00/0/', views.category, name='index'),
    
]