# mini_insta/views.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/24/25
# Description: defining views of mini_insta application


from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.

class ShowAllView(ListView):
    """Define a veiw class to show all profile Profiles"""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

#endclass


class ProfileView(DetailView):
    """Displays a single Profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

#end class
