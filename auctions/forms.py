from django import forms
from .models import * 


class CreateListingForm(forms.ModelForm):

    class Meta:
        model = Listings
        fields = ('item_name', 'price', 'listing_category', 'img', 'description')
        labels = {'item_name': "Product", 'listing_category': "Category", 'img':"Picture:" }

class CommentForm(forms.Form):
    comment = forms.IntegerField(label="comment")

class BidsForm(forms.Form):
    new_bid = forms.IntegerField(label="price", required=False)
