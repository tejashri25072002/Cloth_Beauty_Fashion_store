from django.contrib import admin
from clothapp.models import cloth_product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails','cat','occa','is_active']
    list_filter=['cat','price','is_active']
admin.site.register(cloth_product,ProductAdmin)