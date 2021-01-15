from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View
from googlesearch import search 

class SemrushCallSerp(View):
    def get(self, request, keyword, pk):
        query = keyword
        search_list = []
        for serp_result in search(query, tld="co.in", num=10, stop=20, pause=2):

            search_list.append(serp_result)

        context = {
            'items': search_list,
            'id' : pk,
            'title': 'Items'
        }

        #return HttpResponse(pk)
        #return HttpResponse(search_list)
        return render(request, 'newsApp/serp/serp.html', context)