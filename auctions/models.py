from distutils.command.upload import upload
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ImageField


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

# auction listings
class Listings(models.Model):
    #place tables to database here
    item_name = models.CharField(max_length = 64)
    description = models.CharField(max_length= 256)
    price = models.IntegerField()
    # add photo query here
    date_created = models.DateField()
    sold = models.BooleanField()
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="buyer")
    picture = models.CharField(max_length = 64)
    #pic = ImageField(upload_to='images/')
    listing_category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="l_category")
    lister = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="lister")


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    listings = models.ManyToManyField(Listings, related_name="listings", blank=True)

    def __str__(self):
        return f"{self.user}'s watchlist"

# Bids
# class bids(models.Model):
#     bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
#     bid = models.IntegerField()
#     price = models.IntegerField()





# Comments made on auction listings
class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment_reciever = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing")
    comment = models.CharField(max_length= 256)