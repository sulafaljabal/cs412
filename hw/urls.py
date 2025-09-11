# file: hw/urls.py

from django.urls import path
from django.conf import settings #?
from . import views

# URL patterns specific to the hw app
urlpatterns = [
    #path(r'', views.home, name='home'),
    path(r'', views.home_page, name="home_page"),
    path(r'about', views.about_page, name="about_page"),
]