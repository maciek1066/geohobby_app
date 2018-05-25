from django import forms
from .models import User, Hobby


class AddUserForm(forms.Form):
    name = forms.CharField(label='name')
    email = forms.CharField(label='email',
                            widget=forms.EmailInput)
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password',
                                widget=forms.PasswordInput)


class LoginForm(forms.Form):
    user = forms.CharField(label='name')
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput)


