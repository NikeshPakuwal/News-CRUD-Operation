from django.urls import path, include
from .import views
from django.contrib.auth.views import LoginView
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.news_form, name = 'news_insert'),
    path('login/',auth_views.LoginView.as_view(template_name='newsApp/login.html'), name='login'),
    path('register/', RegistrationView.as_view(template_name='newsApp/register.html'), name = 'register'),
    path('<int:id>/', views.news_form, name = 'news_update'),
    path('delete/<int:id>/', views.news_delete, name = 'news_delete'),
    path('list/', views.news_list, name = 'news_list'),
]