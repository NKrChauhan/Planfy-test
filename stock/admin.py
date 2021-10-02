from stock.models import Stock
from django.contrib import admin
from .models import Stock, Stock_Query
# Register your models here.

admin.site.register(Stock)
admin.site.register(Stock_Query)