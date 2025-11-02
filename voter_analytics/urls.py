# file: voter_analytics/urls.py
# Sulaf Al Jabal (sulafaj@bu.edu) 10/31/25
# URL patterns for voter_analytics


from django.urls import path
from django.conf import settings 

from.views import * 

# URL patterns specific to the voter_analytics app

urlpatterns = [
    path(r'', VoterListView.as_view(), name="voters"), # main page
    path('voter/<int:pk>/', VoterDetailView.as_view(), name="voter"), # individual voter pages
    path('graphs', GraphsListView.as_view(), name="graphs"), # graphs page 

]