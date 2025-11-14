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
    # API urls
    path('api/jokes', JokeListAPIView.as_view(), name = 'joke_list_api'),
    path('api/joke/<int:pk>', JokeRetrieveAPIView.as_view(), name = 'joke_api'),
    path('api/', RandomJokeAPIView.as_view(), name = 'api'),
    path('api/random', RandomJokeAPIView.as_view(), name = 'random_joke_api'),
    path('api/pictures', PictureListAPIView.as_view(), name='picture_list_api'),
    path('api/random_picture', RandomPictureAPIView.as_view(), name='random_picture_api'),
    path('api/picture/<int:pk>', PictureRetrieveAPIView.as_view(), name='picture_api'),
]