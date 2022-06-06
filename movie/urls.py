from django.urls import path
from . import views

urlpatterns = [
    path('film_management', views.film_management),
    path('film_create', views.film_create),
    path('studio_management', views.studio_management),
    path('studio_create', views.studio_create),
    path('studio_fix', views.studio_fix),
    path('controller_management', views.controller_management),
    path('controller_create', views.controller_create),
    path('session_management', views.session_management),
    path('session_create', views.session_create),
    path('user_order', views.order_management),
]
