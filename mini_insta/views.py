# mini_insta/views.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/24/25
# Description: defining views of mini_insta application


from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile
import random 

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

# NOT SURE IF I NEED THIS FOR THE HOMEWORK JUST YET
# class RandomArticleView(DetailView):
#     """Displays a single random article"""

#     model = Article
#     template_name = "blog/article.html"
#     context_object_name = "article"

#     def get_object(self):
#         """return one instance of the Article object selected
#         at random. Overiding a function"""

#         all_articles = Article.objects.all()
#         article = random.choice(all_articles)
#         return article
#     #end get_object
# #endclass
