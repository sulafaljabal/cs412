# file: voter_analytics/urls.py
# Sulaf Al Jabal (sulafaj@bu.edu) 10/31/25
# URL patterns for voter_analytics


from django.urls import path
from django.conf import settings 

from.views import * 
# from django.contrib.auth import views as auth_views ##new

# URL patterns specific to the quotes app

urlpatterns = [
    path(r'', VoterListView.as_view(), name="voters"),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name="voter"),
    path('graphs', GraphsListView.as_view(), name="graphs"),

]