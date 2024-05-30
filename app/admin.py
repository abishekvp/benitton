from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AdminProduct)
admin.site.register(ProductEnquiry)
admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(PlumberRequest)