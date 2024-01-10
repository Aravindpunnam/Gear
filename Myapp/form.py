from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer
from .models import ShippingAddress


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name  = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=12)



    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'phone')


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'zipcode', 'phone']