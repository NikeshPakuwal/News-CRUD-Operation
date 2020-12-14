from django.urls import path, include
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.news_form, name = 'news_insert'),
    path('login/',views.loginPage, name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='newsApp/logout.html'), name='logout'),
    path('<int:id>/', views.news_form, name = 'news_update'),
    path('list/', views.news_list, name = 'news_list'),
    path('', views.news_form, name = 'news_form'),
    path('category/', views.news_category, name = 'news_category'),
    path('category/', views.news_category_display, name = 'news_category_display'),
    path('delete/<str:pk>', views.news_delete, name = 'news_delete'),
]