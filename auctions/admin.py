from django.contrib import admin

# Register your models here.
from .models import Listings, Categories, Comments, Bids, Watchlist

class ListingsAdmin(admin.ModelAdmin):
    list_display = ("id", "item_name", "price", "img", "date_created")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "category")

class BidsAdmin(admin.ModelAdmin):
    list_display=("bidder", "bid", "price")

class CommentsAdmin(admin.ModelAdmin):
    list_display=("commenter", "comment_reciever", "comment")

class WatchlistAdmin(admin.ModelAdmin):
    list_display =("id", "user")

admin.site.register(Categories,CategoriesAdmin)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Watchlist, WatchlistAdmin)

