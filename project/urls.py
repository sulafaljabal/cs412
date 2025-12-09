# file: project/urls.py
# Sulaf Al Jabal (sulafaj@bu.edu) 11/24/25
# URL patterns for final project application

from django.urls import path
from django.conf import settings 
from .views import *

urlpatterns = [
    # Home page
    path('', HomeView.as_view(), name='home'),
    
    # Main list views
    path('doctors', DoctorListView.as_view(), name='doctors'),
    path('nurses', NurseListView.as_view(), name='nurses'),
    path('patients', PatientListView.as_view(), name='patients'),
    path('appointments', AppointmentListView.as_view(), name='appointments'),

    # Detail views
    path('patient/<int:pk>', PatientDetailView.as_view(), name='patient'),
    path('nurse/<int:pk>', NurseDetailView.as_view(), name='nurse'),
    path('doctor/<int:pk>', DoctorDetailView.as_view(), name='doctor'),
    path('appointment/<int:pk>', AppointmentDetailView.as_view(), name='appointment'),

    # Calendar views
    path('appointment_calendar/', CalendarView.as_view(), name='appointment_calendar'),
    path('day_schedule/', DayScheduleView.as_view(), name='day_schedule'),
    
    # Appointment management
    path('create_appointment/', CreateAppointmentView.as_view(), name='create_appointment'),
    path('delete_appointment/<int:pk>/', DeleteAppointmentView.as_view(), name='delete_appointment'),
    
    # Patient management
    path('create_patient/', CreatePatientView.as_view(), name='create_patient'),
    path('update_patient/<int:pk>/', UpdatePatientView.as_view(), name='update_patient'),
    
    # Doctor management
    path('create_doctor/', CreateDoctorView.as_view(), name='create_doctor'),
    path('update_doctor/<int:pk>/', UpdateDoctorView.as_view(), name='update_doctor'),
    
    # Nurse management
    path('create_nurse/', CreateNurseView.as_view(), name='create_nurse'),
    path('update_nurse/<int:pk>/', UpdateNurseView.as_view(), name='update_nurse'),
]