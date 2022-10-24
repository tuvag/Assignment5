from unicodedata import category
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from datetime import datetime
from django.contrib import messages

from .models import *

""" class CreateListingForm(forms.Form):
    item_name = forms.CharField(label ="item_name")
    item_price = forms.IntegerField(label="item_price")
    category = forms.CharField(label="l_category")
    description = forms.CharField(label= "description") """

class CreateListingForm(forms.ModelForm):

    class Meta:
        model = Listings
        fields = ('item_name', 'price', 'listing_category', 'img', 'description')

    #buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="buyer")
   # url_img = models.URLField()
   # lister = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="lister")

class CommentForm(forms.Form):
    comment = forms.Textarea()

class BidsForm(forms.Form):
    price = forms.IntegerField(label="price")

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

def create_listing(request):
    msg = ""
    if request.method == "POST":
        form = CreateListingForm(request.POST)
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
            # if request.user.is_authenticated:
            #     name = request.user
            # item_name = form.cleaned_data["item_name"]
            # price = form.cleaned_data["item_price"]
            # category = form.cleaned_data["l_category"]
            # description = form.cleaned_data["description"]
            # date_created = datetime.now()
            # picture goes here
        else:
            msg = "Invalid entry. Please try again."
            return render(request,"auctions/create.html", {"form": form, "message": msg})
        #add photo to listing
        # new_listing = Listings(name=name, item_name=item_name, description=description, price=price, date_created=date_created, category=l_category)

        # new_listing.save()
    else:
        form = CreateListingForm()
        return render(request, "auctions/create_listing.html", {"form": form, "message": msg})

def listing(request,id):
    listing = Listings.objects.get(pk=id)
    comments = Comments.objects.filter(comment_reciever = listing)
   
    return render(request, "auctions/listing.html",{"listings":listing, "comments":comments})


def categories(request):
    return render(request, "auctions/categories.html", {"l_category": Categories.objects.all()})

def filter_category(request, id):
    listings_category = Listings.objects.filter(listing_category = id)
    return render(request, "auctions/index.html", {"listings": listings_category})

def watchlist(request):
    items_to_show = Watchlist.objects.get(user = request.user)

    return render(request, "auctions/watchlist.html", {"watchlist": items_to_show.listings.all()})

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

def comment_to_listing(request, id):
    listing = Listings.objects.get(pk=id)
    if request.user.is_authenticated and request.method == "POST":
        form = CommentForm(request.POST) 
        comment = form.data["comment"]
        comment_to_save = Comments(commenter = request.user, comment_reciever = listing, comment = comment)
        comment_to_save.save()
        return redirect('listing', id = id)





