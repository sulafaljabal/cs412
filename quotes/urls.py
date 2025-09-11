# file: quotes/urls.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/09/25
# Description: URL patterns for the quotes app. Contains 4 paths: '', 'about', 'quote', and 'show_all'
# day, and show all quotes.


from django.urls import path
from django.conf import settings 
from . import views

# URL patterns specific to the quotes app
urlpatterns = [
    path(r'', views.home_page, name="home_page"),
    path(r'about', views.about_page, name="about_page"),
    path(r'quote', views.quote_page, name="quote_page"),
    path(r'show_all', views.show_all_page, name="show_all_page"),
]