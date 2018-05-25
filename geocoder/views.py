from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.db import models
from geocoder.forms import AddUserForm, LoginForm, HobbyForm
from geocoder.models import Hobby
import requests


# basic view with links to login/register
class BasicView(View):
    def get(self, request):
        return render(
            request,
            template_name="main.html",
            context={}
        )


# registration
class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        ctx = {
            'form': form
        }
        return render(
            request,
            template_name='register.html',
            context=ctx
        )

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                form.add_error('username', "username already exists")
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password != password2:
                form.add_error('password', "Passwords don't match")
            if not form.errors:
                User.objects.create_user(
                    username=username,
                    password=password
                )
                return redirect("/login")
        ctx = {
            'form': form
        }
        return render(
            request,
            template_name='register.html',
            context=ctx
        )


class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {
            'form': form
        }
        return render(
            request,
            template_name='login.html',
            context=ctx
        )

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in")
                return redirect("/hobby")
            return HttpResponse("Try again")
        ctx = {
            'form': form
        }
        return render(
            request,
            template_name='login.html',
            context=ctx
        )


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/login")


class HobbyView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = HobbyForm()
        username = request.user
        user_hobbies = username.hobby_set.all()
        hobbies = Hobby.objects.exclude(pk__in=user_hobbies)
        ctx = {
            "form": form,
            "username": username,
            "user_hobbies": user_hobbies,
            "hobbies": hobbies,
        }
        return render(
            request,
            "hobby.html",
            context=ctx
        )

    def post(self, request):
        form = HobbyForm(request.POST)
        if form.is_valid():
            hobby = form.cleaned_data['hobby_name']
            if Hobby.objects.filter(
                    hobby_name__contains=hobby).exists():
                return HttpResponse("hobby already exists, "
                                    "<a href='/hobby'>go back</a>")
            else:
                new_hobby = Hobby.objects.create(hobby_name=hobby)
                new_hobby.group.add(request.user)
                new_hobby.save()
        return redirect('/hobby/')


class HobbyDetailView(View):
    @method_decorator(login_required)
    def get(self, request, hobby_id):
        hobby = Hobby.objects.get(pk=hobby_id)
        members = hobby.group.all()
        user = request.user
        if user in hobby.group.all():
            member = True
        else:
            member = False
        ctx = {
            "hobby": hobby,
            "members": members,
            "user": user,
            "member": member,
        }
        return render(
            request,
            "hobby_details.html",
            context=ctx,
        )

    def post(self, request, hobby_id):
        hobby = Hobby.objects.get(pk=hobby_id)
        user = request.user
        if "quit" in request.POST:
            hobby.group.remove(user)
        elif "join" in request.POST:
            hobby.group.add(user)
            hobby.save()
        return redirect("/hobby_details/{}".format(hobby_id))


class GeoLocationView(View):
    def get(self, request):
        user = request.user
        #  to avoid proxy
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        country = data['country']
        city = data['city']
        longitude = data['lon']
        latitude = data['lat']
        ctx = {
            "city": city,
            "ip": ip,
            "data": data,
            "country": country,
            "longitude": longitude,
            "latitude": latitude,
        }
        return render(
            request,
            "geolocation.html",
            context=ctx
        )
