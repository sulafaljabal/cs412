# file: project/urls.py
# Sulaf Al Jabal (sulafaj@bu.edu) 11/24/25
# URL patterns for final project application


from django.urls import path
from django.conf import settings 
from . import views

from.views import * #ShowAllView, ProfileView CreatePostView, etc...
# from django.contrib.auth import views as auth_views ##new

# URL patterns specific to the quotes app
#app_name = "mini_insta"

urlpatterns = [
    path('', AppointmentListView.as_view(), name='home'),
    path('doctors', DoctorListView.as_view(), name='doctors'),
    path('nurses', NurseListView.as_view(), name='nurses'),
    path('patients', PatientListView.as_view(), name='patients'),
    path('appointments', AppointmentListView.as_view(), name='appointments'),

    path('patient/<int:pk>', PatientDetailView.as_view(), name='patient'),
    path('nurse/<int:pk>', NurseDetailView.as_view(), name='nurse'),
    path('doctor/<int:pk>', DoctorDetailView.as_view(), name='doctor'),
    path('appointment/<int:pk>', AppointmentDetailView.as_view(), name='appointment'),

    path(r"appointment_calendar/", views.CalendarView.as_view(), name="appointment_calendar"),

]