# file: restaurant/urls.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/16/25
# Description: urls for restaurant application

from django.urls import path
from django.conf import settings 
from . import views

# URL patterns specific to the hw app
urlpatterns = [
    path(r'main', views.main, name="main_page"),
    path(r'order', views.order, name="order_page"),
    path(r'submit', views.submit, name="submit"),
    path(r'', views.main, name="main_page"),
]