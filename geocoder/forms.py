from django import forms
from .models import User, Hobby


class AddUserForm(forms.Form):
    name = forms.CharField(label='Username')
    email = forms.CharField(label='Email',
                            widget=forms.EmailInput)
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput)


class LoginForm(forms.Form):
    user = forms.CharField(label='Username')
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)


