from django.db import models
from user.models import UserInfo


class Order(models.Model):
    username = models.CharField(max_length=64, default='garble')
    session_id = models.IntegerField(default=0)
    seats = models.CharField(max_length=255)
    value = models.IntegerField(default=0)


class Films(models.Model):
    image = models.FileField(upload_to='photo', default='user1.jpg')
    name = models.CharField(max_length=30)
    classify = models.CharField(max_length=255)
    img = models.FileField(null=True)
    discription = models.CharField(max_length=255)
    movie_runtime = models.IntegerField()  # 单位分钟
    onlien_time = models.DateTimeField(auto_now=True)
    director = models.CharField(max_length=32)
    actor = models.CharField(max_length=255)
    value = models.IntegerField()


class Classify(models.Model):
    name = models.CharField(max_length=4)


class Studio(models.Model):
    name = models.CharField(max_length=8)
    length = models.IntegerField()
    width = models.IntegerField()
    seats = models.CharField(max_length=255, default='')
    num = models.IntegerField(default=0)


class Sessions(models.Model):
    begin_time = models.DateTimeField()
    seats = models.CharField(max_length=255, default='')
    film = models.ForeignKey(Films, on_delete=models.PROTECT)
    studio = models.ForeignKey(Studio, on_delete=models.PROTECT)
