# project/views.py
# Sulaf Al Jabal (U78815065) 11/24/25
# file description: views for final project
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from .models import * 
from django.urls import reverse # will need to use this later
# from .forms import * # administrative staff and patients should be able to schedule appointments

# Create your views here.

class DoctorListView(ListView):
    """View responsible for showing all doctor records """
    context_object_name = 'doctors'
    template_name = 'project/doctors.html'
    model = Doctor
#endclass

class NurseListView(ListView):
    """View responsible for showing all nurse records """
    context_object_name = 'nurses'
    template_name = 'project/nurses.html'
    model = Nurse
#endclass

class PatientListView(ListView):
    """View responsible for showing all Patient records"""
    context_object_name = 'patients'
    template_name = 'project/patients.html'
    model = Patient 
#endclass

class AppointmentListView(ListView):
    """ View resposible for showing all Appointment records"""
    template_name = 'project/appointments.html'
    context_object_name = 'appointments'
    model = Appointment
#endclass

class PatientDetailView(DetailView):
    """ View resposible for showing information about a particular Patient """
    context_object_name = 'patient'
    template_name = 'project/patient.html'
    model = Patient
#endclass

class DoctorDetailView(DetailView):
    """ View resposible for showing information about a particular Doctor"""
    context_object_name = 'doctor'
    template_name = 'project/doctor.html'
    model = Doctor 
#endclass

class NurseDetailView(DetailView):
    """ View resposible for showing information about a particular Nurse"""
    context_object_name = 'nurse'
    template_name = 'project/nurse.html'
    model = Nurse 
#endclass

class AppointmentDetailView(DetailView):
    """ View responsible for showing information about a particular appointment
    Shows patient, nurse(s), doctor, date of appointment """
    template_name = 'project/appointment.html'
    model = Appointment 

    def get_context_data(self, **kwargs):
        """ overriding context data method to add respective nurses and doctors"""
        context = super().get_context_data()
        # returns QuerySet of nurses and doctors
        app = self.object
        
        nurse_list = []
        doctor_list = []

        nurse_provider = list(NurseProvider.objects.filter(appointmentID=app.pk))
        for n in nurse_provider:
            nurse_list.append(Nurse.objects.filter(pk=n.pk)[0]) # this might be a queryset
        #endfor
        
        doctor_provider = list(DoctorProvider.objects.filter(appointmentID=app.pk))
        for d in doctor_provider:
            doctor_list.append(Doctor.objects.filter(pk=d.pk)[0])
        #endfor

        context['nurses'] = nurse_list
        context['doctors'] = doctor_list
        print(doctor_list)
        print(nurse_list)

        return context
