from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    grade = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
