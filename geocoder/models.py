from django.contrib.auth.models import User
from django.db import models


class Hobby(models.Model):
    hobby_name = models.CharField(max_length=64)
    group = models.ManyToManyField(User)
