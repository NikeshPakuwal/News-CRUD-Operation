from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View, ListView
from googlesearch import search
from datatables_view.views import DatatablesView
from .models import SerpDataLink


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