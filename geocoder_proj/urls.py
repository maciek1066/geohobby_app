"""geocoder_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from geocoder.views import (
    BasicView,
    AddUserView,
    UserLoginView,
    UserLogoutView,
    HobbyView,
    HobbyDetailView,
    GeoLocationView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^$', BasicView.as_view()),
    url('^register/$', AddUserView.as_view(), name="register"),
    url('^login/$', UserLoginView.as_view(), name="login"),
    url('^logout/$', UserLogoutView.as_view(), name="logout"),
    url('^hobby/$', HobbyView.as_view(), name="hobby"),
    url('^hobby_details/(?P<hobby_id>(\d)+)$', HobbyDetailView.as_view(), name="hobby_details"),
    url('^geolocation/$', GeoLocationView.as_view(), name="geolocation"),
]
