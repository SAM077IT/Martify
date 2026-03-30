from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'state', 'zip_code', 'country',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'address':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'city':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'zip_code':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code'}),
            'country':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        }
