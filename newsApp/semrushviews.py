from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
import io, csv
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Employee, Semrush
from django.urls import reverse

from ajax_datatable.views import AjaxDatatableView
# from django.contrib.auth.models import Permission


@method_decorator(login_required(login_url='login'), name="dispatch")
class semrush(View):
    def get(self, request):
        return render(request, 'newsApp/semrush/semrush_add.html')
        
    def post(self, request):
        user = request.user
        paramFile = io.TextIOWrapper(request.FILES['semrushData'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        objs = [
            Semrush(
                country=row['country'],
                keyword=row['keyword'],
                seed_keyword =row['seed_keyword'],
                tags=row['tags'],
                volume =row['volume'],
                keyword_difficulty=row['keyword_difficulty'],
                ccp  =row['ccp'],
                competitive_density  =row['competitive_density'],
                number_of_results  =row['number_of_results'],
                serp_Features =row['serp_Features'],
                trend  =row['trend'],
                click_potential  =row['click_potential'],
                competitors  =row['competitors'],
            )
            for row in list_of_dict
        ]
        # return HttpResponse(list_of_dict)
        # Employee.objects.bulk_create(objs)
        try:
            msg = Semrush.objects.bulk_create(objs)
            returnmsg = {"status_code": 200}
            print('imported successfully')
        except Exception as e:
            print('Error While Importing Data: ', e)
            returnmsg = {"status_code": 500}
        return JsonResponse(returnmsg)


class SemrushList(ListView):
    model = Semrush
    template_name = 'newsApp/Semrush/semrush_list.html'
    ordering = ['-id']
    def get_context_data(self, **kwargs):
        context = super(SemrushList, self).get_context_data(**kwargs)


@method_decorator(login_required(login_url='login'), name="dispatch")
class PermissionAjaxDatatableView(AjaxDatatableView):
    model = Semrush
    title = 'SemrushData'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {
            'name': 'id',
        },
        {
            'name': 'country',
        },
        {
            'name': 'keyword',
        },
        {
            'name': 'seed_keyword',
        },
        {
            'name': 'volume',
        },
        {
            'name': 'keyword_difficulty',
        },
        {
            'name': 'created_at',
            'title': 'created_at',
            'className': 'date_input',
            'searchable': True,
            'orderable': True,
        },
        {
            'name': 'action',
            'searchable': False,
            'orderable': False
        }
    ]

    def customize_row(self, row, obj):
        row['action'] = '<a class="btn btn-info client-status" href="%s">%s</a>'% (
            # obj.id,
            reverse('semrush_serp', args=(obj.keyword,obj.pk)),
            'Get Link'
        ),
        return


class Employee1(View):
    def get(self, request):
        return render(request, 'newsApp/postAdd.html')
    def post(self, request):
        user = request.user
        paramFile = io.TextIOWrapper(request.FILES['PostAdd'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        objs = [
            Employee(
                first_name=row['first_name'],
                last_name=row['last_name'],
                gender=('F' if row['gender'] == 'Female' else ('M' if row['gender'] == 'Male' else 'F')),
                dob=(row['dob'] if row['dob'] != '' else '1970-01-01'),
                district=row['district'],
                phone_number=row['phone_number'],
            )
            for row in list_of_dict
        ]
        # return HttpResponse(list_of_dict)
        # Employee.objects.bulk_create(objs)
        try:
            msg = Employee.objects.bulk_create(objs)
            returnmsg = {"status_code": 200}
            print('imported successfully')
        except Exception as e:
            print('Error While Importing Data: ', e)
            returnmsg = {"status_code": 500}

        return JsonResponse(returnmsg)