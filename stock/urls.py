from .views import search, detail, Home,stock_query, download_xls,load_more,all_query
from django.urls import path
app_name = 'stock'

urlpatterns = [
    path('',Home, name='home'),
    path('load_more/<int:limit>/',load_more, name='load_more'),
    path('download/',download_xls, name='download_xls'),
    path('queries/',all_query, name='all_query'),
    path('query/',stock_query, name='stock_query'),
    path('detail/<slug>/',detail, name='detail'),
    path('search/',search, name='search'),
]