from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
