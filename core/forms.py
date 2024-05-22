# forms.py
from django import forms
from .models import CartOrderItems

class UpdateQuantityForm(forms.ModelForm):
    class Meta:
        model = CartOrderItems
        fields = ['qty']

class DeleteItemForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())
