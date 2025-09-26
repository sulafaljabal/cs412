# file: mini_insta/urls.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/24/25
# URL patterns for mini_insta application


from django.urls import path
from django.conf import settings 
from . import views

from.views import ShowAllView, ProfileView # change later for other things???

# URL patterns specific to the quotes app
#app_name = "mini_insta"
urlpatterns = [
    # path('',RandomArticleView.as_view(), name="random"),
    path('show_all_profiles',ShowAllView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>/', ProfileView.as_view(), name="show_profile"),
]