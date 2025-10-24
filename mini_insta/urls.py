# file: mini_insta/urls.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/24/25
# URL patterns for mini_insta application


from django.urls import path
from django.conf import settings 
from . import views

from.views import * #ShowAllView, ProfileView CreatePostView, etc...
from django.contrib.auth import views as auth_views ##new

# URL patterns specific to the quotes app
#app_name = "mini_insta"

urlpatterns = [
    path('', ShowAllView.as_view(), name="show_all_profiles"),
    path('show_all_profiles',ShowAllView.as_view(), name="show_all_profiles"),

    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk/update', UpdatePostView.as_view(), name="update_post"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="show_post"),

    path('profile/<int:pk>/followers/', ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following/', ShowFollowingDetailView.as_view(), name="show_following"),
    path('profile/<int:pk>/', ProfileView.as_view(), name="show_profile"),

    path('profile/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path('profile/feed', PostFeedListView.as_view(), name="show_feed"),
    path('profile/search', SearchView.as_view(), name="search"),

    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logged_out'), name='logout'),
    path('logged_out/', LoggedOutView.as_view(), name='logged_out'),

]