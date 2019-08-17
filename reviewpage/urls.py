from django.urls import path
from reviewpage import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sort=likes', views.index, name="index_sort=like"),
    path('sort=mypost', views.index, name="index_sort=mypost"),
    path('new/', views.new, name='new'),
    path('<int:id>/', views.show, name='show'),
    path('<int:id>/delete', views.delete, name='delete'),
    path('<int:id>/edit', views.edit, name='edit'),
    path('<int:pk>/like/', views.review_like, name='like'),
    path('<int:pk>/save/', views.review_save, name='save'),
]
