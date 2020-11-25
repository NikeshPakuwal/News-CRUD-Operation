from django.shortcuts import render, redirect
from .forms import NewsForm
from. models import newsDetails

# Create your views here.
def news_list(request):
    context = {'news_list' : newsDetails.objects.all()}
    return render(request, "newsApp/news_list.html", context)

def news_form(request, id = 0):
    if request.method == "GET":
        if id == 0:
            form = NewsForm()
        else: 
            newsDetail = newsDetails.objects.get(pk = id)
            form = NewsForm(instance = newsDetail)
        return render(request, "newsApp/news_form.html", {'form': form})
    else:
        if id == 0:
            form = NewsForm(request.POST)
        else:
            newsDetail = newsDetails.objects.get(pk = id)
            form = NewsForm(request.POST, instance = newsDetail)
        if form.is_valid():
            form.save()
        return redirect('/news/list')

def news_delete(request, id):
    newsDetail = newsDetails.objects.get(pk = id)
    newsDetail.delete()
    return redirect('/news/list')