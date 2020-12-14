from django.shortcuts import render, redirect
from .forms import NewsForm
from .forms import NewsCat
from. models import newsDetails
from .models import Category
from django.contrib import auth
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def news_list(request):
    context = {'news_list' : newsDetails.objects.all()}
    return render(request, "admin/news_list.html", context)

@login_required(login_url='login')
def news_form(request, id = 0):
    if request.method == "GET":
        if id == 0:
            form = NewsForm()
        else: 
            newsDetail = newsDetails.objects.get(pk = id)
            form = NewsForm(instance = newsDetail)
        return render(request, "admin/news_form.html", {'form': form})
    else:
        if id == 0:
            form = NewsForm(request.POST)
        else:
            newsDetail = newsDetails.objects.get(pk = id)
            form = NewsForm(request.POST, instance = newsDetail)
        if form.is_valid():
            form.save()
        return redirect('/news/list')

def news_delete(request, pk):
    newsDelete = newsDetails.objects.get(id = pk)
    if request.method == "POST":
        newsDelete.delete()
        return redirect('/news/list')
    return render(request,'admin/delete.html') 
    
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('/news')

    return render(request, 'authenticate/login.html')

@login_required(login_url='login')
def news_category(request, id = 0):
    if request.method == "GET":
        if id == 0:
            cat = NewsCat()
        else: 
            Category = Category.objects.get(pk = id)
            cat = NewsCat(instance = Category)
        return render(request, "admin/category.html", {'cat': cat})
    else:
        if id == 0:
            cat = NewsCat(request.POST)
        else:
            Category = Category.objects.get(pk = id)
            cat = NewsCat(request.POST, instance = Category)
        if cat.is_valid():
            cat.save()
        return redirect('/news/category')

def news_category_display(request):
    context = {'news_category_display' : Category.objects.all()}
    return render(request, "admin/category.html", context)
    