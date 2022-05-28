from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import *
# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyCustomer)
admin.site.register(CompanyProduct)
admin.site.register(CustomerOrder)