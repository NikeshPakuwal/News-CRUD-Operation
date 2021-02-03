from django.shortcuts import render, redirect
from .forms import NewsCat, NewsForm, ScrapperForm
from. models import newsDetails, Category, todoList, webScraping
from django.contrib import auth
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from urllib.request import Request, urlopen as uReq
from bs4 import BeautifulSoup  

# Create your views here.
def home(request):
    return render(request, 'newsApp/view.html')

@login_required(login_url='login')
def news_index(request):
    return render(request, 'newsApp/base.html')

@login_required(login_url='login')
def news_list(request):
    context = {'news_list' : newsDetails.objects.all()}
    return render(request, "newsApp/admin/news_list.html", context)

@login_required(login_url='login')
def news_form(request, id = 0):
    if request.method == "GET":
        if id == 0:
            form = NewsForm()
        else: 
            newsDetail = newsDetails.objects.get(pk = id)
            form = NewsForm(instance = newsDetail)
        return render(request, "newsApp/admin/news_form.html", {'form': form})
    else:
        if id == 0:
            form = NewsForm(request.POST)
        else:
            newsDetail = newsDetails.objects.get(pk = id)
            form = NewsForm(request.POST, instance = newsDetail)
        if form.is_valid():
            form.save()
            messages.success(request, 'Process Suceessful!')
        return redirect('/news/list')

def news_delete(request):
    id = request.POST.get('id')
    news = newsDetails.objects.get(pk = id)
    news.delete()
    return JsonResponse({'success' : 'true'});
           
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('/display')
    
    return render(request, 'newsApp/authenticate/login.html')

@login_required(login_url='login')
def news_category(request, id = 0):
    if request.method == "GET":
        if id == 0:
            cat = NewsCat()
        else: 
            category = Category.objects.get(pk = id)
            cat = NewsCat(instance = category)
        return render(request, "newsApp/admin/category.html", {'cat': cat})
    else:
        
        if id == 0:
            cat = NewsCat(request.POST)
        else:
            category = Category.objects.get(pk = id)
            cat = NewsCat(request.POST, instance = category)
        if cat.is_valid():
            cat.save()
            messages.success(request, 'Process Successful!')
        return redirect('/news/category')

@login_required(login_url='login')
def news_category_list(request):
    content = {'news_category_list' : Category.objects.all()}
    return render(request, "newsApp/admin/category_list.html", content)

def news_category_delete(request):
    id = request.POST.get('id')
    category = Category.objects.get(pk = id)
    category.delete()
    return JsonResponse({'success' : 'true'})

@login_required(login_url='login')
def todo(request):
    content = {'todo' : todoList.objects.all()}
    return render(request, "newsApp/ToDo/toDO.html", content)

def submitTodo(request):
    if request.method == 'POST':
        title = request.POST['title']
        data = todoList.objects.create(
            title = title
        )
    return JsonResponse({'succes':'true','title':title,'created_at':data.created_at.strftime
    ('%b. %d, %Y, %H:%M %p.').replace('AM', 'a.m').replace('PM', 'p.m')})

def todoCheck(request):
    id = request.POST.get('id')
    todo = todoList.objects.get(pk = id)
    if(todo.status == True):
        todo.status = False
    else:
        todo.status = True
    todo.save()
    return JsonResponse({'success' : 'true','id':id})

def TodoSumbit(request):
    id = request.POST.get('id')
    title = request.POST.get('title')
    todo = todoList.objects.get(pk=id)
    todo.title = title
    todo.save()
    return JsonResponse({'success' : 'true','id':id,'title':title})

@login_required(login_url='login')
def scraping(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        array = url.split(',')
        for i in array:
            page = uReq(url)
            page_html = page.read()
            page.close()

            soup = BeautifulSoup(page_html, 'html.parser')

            if soup.h1 and soup.p:
                title = soup.h1.string
                content = soup.p.string
                messages.success(request, 'Process Suceessful!')

            data = webScraping.objects.create(
                title = title,
                content = content,
                url = url
            )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        context = {}
        form = ScrapperForm(request.POST or None)
        context['form'] = form
        context = {'list' : webScraping.objects.all()}
        return render(request, 'newsApp/Scraping/scraping.html',context)

def deleteScraping(request):
    id = request.POST.get('id')
    scrap = webScraping.objects.get(pk = id)
    scrap.delete()
    return JsonResponse({'success' : 'true'})