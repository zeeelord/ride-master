# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Order


class PostOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
