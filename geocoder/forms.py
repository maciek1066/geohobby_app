from django.forms import ModelForm
from django import forms
from .models import User, Hobby


class AddUserForm(forms.Form):
    username = forms.CharField(label='Name')
    email = forms.CharField(label='Email',
                            widget=forms.EmailInput)
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(label='Name')
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)


class HobbyForm(ModelForm):
    class Meta:
        model = Hobby
        fields = ['hobby_name']



