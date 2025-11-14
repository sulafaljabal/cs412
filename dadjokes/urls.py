from django.urls import path
from django.conf import settings 
# from django.contrib.auth import views as auth_views ##new

from . import views
from .views import *

urlpatterns = [
    path('', randomJokeView, name='home'),
    path('random', randomJokeView, name='random'),
    path('jokes', JokeListView.as_view(), name='jokes'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name='joke'),
    path('pictures', PictureListView.as_view(), name='pictures'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name='picture'),
    # path(r'', RandomJokeView.as_view(), name='random'),
    # path(r'r',RandomPictureView.as_view(), name='random_picture'),
]