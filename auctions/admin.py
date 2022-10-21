from django.contrib import admin

# Register your models here.
from .models import Listings, Categories, Comments, Watchlist

class ListingsAdmin(admin.ModelAdmin):
    list_display = ("id", "item_name", "price", "date_created", "picture", "sold", "buyer", "lister")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "category")

admin.site.register(Categories,CategoriesAdmin)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Comments)