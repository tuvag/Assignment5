from datetime import datetime
from distutils.command.upload import upload
from unicodedata import category
from urllib import request
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ImageField
from urllib.request import urlopen
from django.core.files import File
from tempfile import NamedTemporaryFile


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

# auction listings
class Listings(models.Model):
    item_name = models.CharField(max_length = 64)
    description = models.CharField(max_length= 256)
    price = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    sold = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="buyer")
    img = models.ImageField(upload_to='images/', blank=True)
    url_img = models.URLField()
    listing_category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="l_category")
    lister = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="lister")

    def save(self, *args, **kwargs):
        if self.url_img and not self.img:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.url_img).read())
            img_temp.flush()
            self.img.save(f"image_{self.pk}", File(img_temp))
        super(Listings, self).save(*args, **kwargs)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    listings = models.ManyToManyField(Listings, related_name="listings", blank=True)

    def __str__(self):
        return f"{self.user}'s watchlist"

# Bids
class Bids(models.Model):
     bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
     bid = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
     price = models.IntegerField()

     def __str__(self):
        return f'{self.price}'

# Comments made on auction listings
class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment_reciever = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing")
    comment = models.TextField()