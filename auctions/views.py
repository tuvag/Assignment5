from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from datetime import datetime

from .models import *

""" class CreateListingForm(forms.Form):
    item_name = forms.CharField(label ="item_name")
    item_price = forms.IntegerField(label="item_price")
    category = forms.CharField(label="tag")
    description = forms.CharField(label= "description") """

class CreateListingForm(forms.ModelForm):
        class Meta:
            model = Listings
            fields = ('item_name', 'price', 'tag', 'description')

def index(request):
    return render(request, "auctions/index.html")


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
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("auctions/index.html")
            # if request.user.is_authenticated:
            #     name = request.user
            # item_name = form.cleaned_data["item_name"]
            # price = form.cleaned_data["item_price"]
            # category = form.cleaned_data["tag"]
            # description = form.cleaned_data["description"]
            # date_created = datetime.now()
            # picture goes here
        else:
            msg = "Invalid entry. Please try again."
            return render(request,"auctions/create.html", {"form": form, "message": msg})
        #add photo to listing
        # new_listing = Listings(name=name, item_name=item_name, description=description, price=price, date_created=date_created, tag=category)

        # new_listing.save()
    else:
        form = CreateListingForm()
        return render(request, "auctions/create_listing.html", {"form": form})

def listing(request, listing_id):
    listing = Listings.objects.get(pk=listing_id)
   
    return render(request, "auctions/listing.html",{"listing":listing,})


def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})

def watchlist(request):
    items_to_show = Watchlist.objects.get(user = request.user) 

    return render(request, "auctions/watchlist.html", {"watchlist": items_to_show.listings.all()})