from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login),
    path('register', views.user_register),
    path('home', views.home),
    path('buy', views.buy),
    path('choice_session',views.choice_session)
]
