from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.news_form, name = 'news_insert'),
    path('<int:id>/', views.news_form, name = 'news_update'),
    path('delete/<int:id>/', views.news_delete, name = 'news_delete'),
    path('list/', views.news_list, name = 'news_list'),
]