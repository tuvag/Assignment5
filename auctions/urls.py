from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:id>/close_listing", views.close_listing, name="close_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:id>", views.save_to_watchlist, name="save_to_watchlist"),
    path("api_toggle_watchlist/<int:id>", views.api_toggle_watchlist, name="api_toggle_watchlist"),
    path("remove_from_watchlist/<int:id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("api_listing_toatals", views.api_listing_toatals, name="api_listing_toatals"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:id>", views.filter_category, name="filter_category"),
    path("<int:id>", views.listing, name="listing"),
    path("<int:id>/", views.comment_to_listing, name="comment_to_listing"),
    path("place_bid", views.place_bid, name="place_bid"),

    path("api_toggle_watchlist/<int:id>", views.api_toggle_watchlist, name="api_toggle_watchlist"),
    path("api_watchlist_state/<int:id>", views.api_watchlist_state, name="api_watchlist_state"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
