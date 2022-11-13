from queue import Empty
from unicodedata import category
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
from .forms import *

from .models import *

def index(request):
    return render(request, "auctions/index.html", {"listings": Listings.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# create a listing
def create_listing(request):
    msg = ""
    if request.method == "POST":
        form = CreateListingForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.sold = False
            if not post.img:
                msg = "Could not upload image"
            post.lister = request.user
            post.date_created = datetime.now()
            post.save()
            messages.success(request, (f'\"{ post.item_name }\" was successfully added!'))
            return redirect("index")
            
        else:
            msg = "Invalid entry. Please try again."
            return render(request,"auctions/create.html", {"form": form, "message": msg})
    else:
        form = CreateListingForm()
        return render(request, "auctions/create_listing.html", {"form": form, "message": msg})

#display a particular listing
def listing(request,id):
    listing = Listings.objects.get(pk=id)
    comments = Comments.objects.filter(comment_reciever = listing)

    if listing.sold == True:
        return redirect('close_listing', id = id)
   
    return render(request, "auctions/listing.html",{"listings":listing, "comments":comments})

#end a particular listing that you have created
def close_listing(request, id):
    listing = Listings.objects.get(pk = id)
    listing_bids = Bids.objects.filter(bid = listing)
    sales_price = listing_bids.order_by('-price').first()
    buyer = User

    for b in listing_bids:
        if b.price == sales_price.price:
            buyer = b.bidder
            listing.buyer = buyer
            listing.sold = True
            listing.save()
    return render(request, "auctions/close_listing.html", {"sales_price": sales_price, "buyer": buyer})

# showing all categories
def categories(request):
    return render(request, "auctions/categories.html", {"l_category": Categories.objects.all()})

#choose a particular category
def filter_category(request, id):
    listings_category = Listings.objects.filter(listing_category = id)
    if listings_category is Empty: 
        msg = f'There are no listings in this category.'
        return (request, "auctions/index.html", {"listings": listings_category, "message":msg})
    return render(request, "auctions/index.html", {"listings": listings_category})

# a users saved listings
def watchlist(request):
    try:
        items_to_show = Watchlist.objects.get(user = request.user)
        return render(request, "auctions/watchlist.html", {"watchlist": items_to_show.listings.all()})
    except:
        messages.error(request, (f'Log in to view your watchlist'))
        return render(request, "auctions/watchlist.html", {"watchlist": None})
    

def save_to_watchlist(request, id):
    if request.user.is_authenticated: 
        if Watchlist.objects.filter(user = request.user).exists():
            watchlist = Watchlist.objects.get(user = request.user)
        else: 
            watchlist = Watchlist(user = request.user)
        watchlist.save()
        to_add = Listings.objects.get(id = id)
        watchlist.listings.add(to_add)
        watchlist.save()

    return render(request, "auctions/watchlist.html", {"watchlist": watchlist.listings.all()})

def api_save_to_watchlist(request, id):
    if request.user.is_authenticated: 
        if Watchlist.objects.filter(user = request.user).exists():
            watchlist = Watchlist.objects.get(user = request.user)
            newstate = "unfavorite"
        else: 
            watchlist = Watchlist(user = request.user)
            newstate = "favorite"
        cnt = Watchlist.objects.filter(user=request.user).count()
        print("This is how many items is in the watchlist: ", cnt)
        watchlist.save()
        to_add = Listings.objects.get(id = id)
        watchlist.listings.add(to_add)
        watchlist.save()
        print("Inside api_save_to_watchlist, and curr_value is: ", newstate)

    return JsonResponse({'curr_value' : newstate})

def api_listing_toatals(request):
    watchlisted = Watchlist.objects.filter(user=request.user).count()
    active_listings = Listings.objects.all().count()
    totals = {
        'total_watchlisted' : watchlisted, 
        'total_active_listings' : active_listings
    }
    return JsonResponse(totals)


def remove_from_watchlist(request, id):
    if request.user.is_authenticated:
        remove = Listings.objects.get(id=id)
        w_list = Watchlist.objects.get(user=request.user)
        updated_watchlist = w_list.listings.remove(remove)
    return redirect('watchlist')


def comment_to_listing(request, id):
    listing = Listings.objects.get(pk=id)
    if request.user.is_authenticated and request.method == "POST":
        form = CommentForm(request.POST) 
        comment = form.data["comment"]
        comment_to_save = Comments(commenter = request.user, comment_reciever = listing, comment = comment)
        comment_to_save.save()
        return redirect('listing', id = id)

def place_bid(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            msg =""
            form = BidsForm(request.POST)
            new_bid = int(form.data["new_bid"])
            id = form.data["id"]
            l = Listings.objects.get(pk=id)
            curr_price = l.price

            if (curr_price < new_bid):
                l.price = new_bid
                l.save()

                bid_data = Bids(price = new_bid, bid = l, bidder= request.user)
                bid_data.save()
                messages.success(request,(f'Your bid was successful'))
            else:
                messages.error(request,(f'Your bid has to be above the current price'))

            return redirect('listing', id = id)
        
    else: 
        form = BidsForm(request.POST)
        id = form.data["id"]
        messages.error(request, (f'Log in to make a bid')) 
        return redirect('listing', id = id)

 