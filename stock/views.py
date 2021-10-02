import json
from django.http.response import HttpResponse, JsonResponse
import xlwt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Stock, Stock_Query
from django.db.models import Q
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def Home(request,*args,**kwargs):
    obj_all = []
    objs = Stock.objects.all()
    u_limit = 3
    l_limit = 0
    obj_all = objs[l_limit:u_limit]
    return render(request=request,template_name='home.html',context={'stocks':obj_all})

@login_required
def load_more(request,limit,*args,**kwargs):
    objs = list(Stock.objects.values())
    obj_all = objs[limit-3:limit]
    max_size_reached = True if len(objs) <= limit else False
    return JsonResponse({"data":obj_all,"max_reached":max_size_reached})


@login_required
def search(request):
    query=request.GET.get('q',None)
    if cache.get(query):
        qs = cache.get(query)
        print("-----------------cache is working--------------------")
    else:
        qs=Stock.objects.none()
        if query is not None:
            lookup=Q(name__icontains=query)
            qs=Stock.objects.filter(lookup).distinct()
            cache.set(query,qs)
    return render(request=request,template_name='stocks/search.html',context={'stocks':qs})

@login_required
def detail(request,slug,*args, **kwargs):   
    object = Stock.objects.get(slug=slug)
    data = {
        'stock': "not found",
    }
    if object :
        data = {
            'stock': object,
       }
    return render(request=request, template_name='stocks/detail.html', context=data)

@login_required
def stock_query(request,*args, **kwargs):
    if request.method == "POST":
        obj = Stock_Query.objects.create(query=request.POST.get("query"),user = request.user,stock = Stock.objects.get(slug=request.POST.get('stock')))
        obj.save()
    return redirect('stock:home')   

@login_required
def all_query(request,*args,**kwargs):
    if request.user.is_admin:
        qs = Stock_Query.objects.all()
        return render(request=request,template_name='stocks/queries.html',context={"queries":qs})
    return HttpResponse(content={"data":"permission_prohibited"})    

@login_required
def download_xls(request,*args,**kwargs):
    if request.user.is_admin:
        qs = Stock_Query.objects.all()
        response = HttpResponse(content_type='application/ms-excel')

        response['Content-Disposition'] = 'attachment; filename="QueryDDMMYY.xls"'

        wb = xlwt.Workbook(encoding='utf-8')

        ws = wb.add_sheet("sheet1")

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Stock', 'User', 'Query']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        for my_row in qs:
            row_num = row_num + 1
            ws.write(row_num, 0, my_row.stock.name, font_style)
            ws.write(row_num, 1, my_row.user.username, font_style)
            ws.write(row_num, 2, my_row.query, font_style)

        wb.save(response)
        return response
    return HttpResponse(content={"data":"permission_prohibited"})    