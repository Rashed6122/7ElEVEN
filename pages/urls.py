# pages/urls.py

from django.urls import path
from pages import views

urlpatterns = [
    path("", views.home, name='home'),
    path("map", views.map , name='map'),
]