from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View, ListView
from googlesearch import search
from datatables_view.views import DatatablesView
from .models import SerpDataLink, SerpContentDetail

from bs4 import BeautifulSoup
import requests
from pprint import pprint

class SemrushCallSerp(View):
    def get(self, request, keyword, pk):
        query = keyword
        search_list = []
        for serp_result in search(query, tld="co.in", num=10, stop=5, pause=2):
            search_list.append(serp_result)

        context = {
            'items': search_list,
            'id' : pk,
            'title': 'Items'
        }
        #return HttpResponse(pk)
        #return HttpResponse(search_list)
        return render(request, 'newsApp/serp/serp.html', context)

@method_decorator(login_required(login_url='login'), name="dispatch")
class SerpDataList(ListView):
    model = SerpDataLink
    template_name = 'newsApp/serp/serp_list.html'
    ordering = ['-id']
    def get_context_data(self, **kwargs):
        context = super(SerpDataList, self).get_context_data(**kwargs)
        context['title'] = 'List Links'
        return context

class AjaxDatatableSerpDataList(DatatablesView):
    model = SerpDataLink
    title = 'Serp Data Link'

    column_defs = [
        {
            'name': 'sn',
            'title': 'sn',
            'className': 'checkbox_input',
            'defaultContent': '<h1>test</h1>',
            'searchable': True,
            'orderable': False,
        },
        {
            'name': 'id',
            'autofilter': True,
        },
        {
            'name': 'Keyword',
            'foreign_field': 'keyword_id__keyword'
        },
        {
            'name': 'links',
        },
        {
            'name': 'created_at',
            'title': 'created_at',
            'className': 'date_input',
            'searchable': True,
            'orderable': True,
        }
        
    ]

    def customize_row(self, row, obj):
        row['sn'] = '<input type="checkbox" name="chk_list" class="checklist" data-cid="%s" id="chk_%s">' % (obj.id, obj.id)
        return

class GoogleLinkUpload(View):
    def post(self, request):
        links_arr = request.POST.getlist('links')
        links = list(links_arr)
        #
        instances = [
            (
                SerpDataLink(
                    links=row,
                    keyword_id_id=request.POST.get('keyword_id')
                )
            )
            for row in links
        ]
        #return HttpResponse(instances)
        SerpDataLink.objects.bulk_create(instances)

        return render(request, 'newsApp/serp/serp_list.html')


class AjaxLoadContent(View):

    def post(self, request):
        # Proxies api-endpoint
        URL = "http://api.proxiesapi.com"
        # insert your auth key here
        auth_key = "060c45d2fd4e69cc72e8f9b51e94a376_sr98766_ooPq87"
        # url = "http://httpbin.org/anything"
        session = "444"

        ids = request.POST.getlist('id[]')
        ulist = []
        insert_list = []
        for i in ids:
            link_info = SerpDataLink.objects.get(id=i)
            #pprint(link_info)
            page_url = link_info.links
            # defining a params dict for the parameters to be sent to the API
            PARAMS = {'auth_key': auth_key, 'url': page_url, 'render': 'true'}

            r = requests.get(url=URL, params=PARAMS)

            # print(r.text)

            html = BeautifulSoup(r.content, 'html.parser')
            insert_list.append(
                SerpContentDetail(
                    serp_link_id=i,
                    keyword_id=int(link_info.keyword_id_id),
                    title=self.get_title(html),
                    content=str(self.get_description(html))
                ),
            )
        SerpContentDetail.objects.bulk_create(insert_list)
        return HttpResponse(insert_list)
        

    def get_title(self, html):
        """Scrape page title."""
        title = None
        if html.title.string:
            title = html.title.string
        elif html.find("meta", property="og:title"):  
            title = html.find("meta", property="og:title").get('content')
        elif html.find("meta", property="twitter:title"):
            title = html.find("meta", property="twitter:title").get('content')
        elif html.find("h1"):
            title = html.find("h1").string
        return title
    
    def get_description(self, html):
        """Scrape page description."""
        description = None
        if html.find("article"):
            description = html.find("article")
        elif html.find("div", {
            'class': ['wrap-content-main', 'post_the_content', 'mw-parser-output', 'descContainer', 'content']}):
            description = html.find(True, {
                'class': ['wrap-content-main', 'mw-parser-output', 'post_the_content', 'descContainer', 'content']})
        elif html.find("main", id_='main'):
            description = html.find("main")
        elif html.find("p"):
            description = html.body.find_all('p')
        return description


class AjaxDatatableSerpContentDetail(DatatablesView):
    model = SerpContentDetail
    title = 'Serp Content Detail'

    column_defs = [
        {
            'name': 'id',
            'autofilter': True,
        },
        {
            'name': 'title',
        },
        {
            'name': 'content',
        },
        {
            'name': 'created_at',
            'title': 'created_at',
            'className': 'date_input',
            'searchable': True,
            'orderable': True,
        }
    ]

class SerpDataContent(ListView):
    model = SerpContentDetail
    template_name = 'newsApp/serp/serp_data_content.html'
    ordering = ['-id']
    def get_context_data(self, **kwargs):
        context = super(SerpDataContent, self).get_context_data(**kwargs)