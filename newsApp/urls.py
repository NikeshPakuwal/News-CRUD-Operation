from django.urls import path, include
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('', views.news_form, name = 'news_insert'),
    path('login/',views.loginPage, name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='newsApp/authenticate/logout.html'), name='logout'),
    path('news/<int:id>/', views.news_form, name = 'news_update'),
    path('list/', views.news_list, name = 'news_list'),
    path('news/', views.news_form, name = 'news_form'),
    path('category/', views.news_category, name = 'news_category'),
    path('category/list', views.news_category_list, name = 'news_category_list'),
    path('delete/', views.news_delete, name = 'news_delete'),
    path('display/', views.news_index, name = 'news_index'),
    path('category/<int:id>/', views.news_category, name = 'news_category_update'),
    path('deleteCategory/', views.news_category_delete, name = 'news_category_delete')
]