from django.contrib import admin
from .models import Product


# just to have a search based on search_fields and display all listed columns in list_display in admin model
# not necessary
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'price', 'created', 'updated',)


admin.site.register(Product, ProductAdmin)
