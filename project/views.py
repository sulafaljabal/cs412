# project/views.py
# Sulaf Al Jabal (U78815065) 11/24/25
# file description: views for final project
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from .models import * 
from django.urls import reverse, reverse_lazy # will need to use this later
from .utils import Calendar

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

    def get_context_data(self, **kwargs):
        """Overriding get context data method to add previous appointments """
        context = super().get_context_data()
        patient = Patient.objects.filter(pk=self.object.pk)[0]
        print(f"THIS IS THE PATIENT: {patient}")
        apps = list(Appointment.objects.filter(patient=patient))
        context['appointments'] = apps 
        return context 
    #enddef
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
#endclass

class CalendarView(ListView):
    """ View responsible for showing calendar with appointments """
    model = Appointment
    template_name = 'project/appointment_calendar.html'
    success_url = reverse_lazy("appointment_calendar")
    # success_url = reverse("appointment_calendar")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # d = get_date(self.request.GET.get('month', None))
        d = datetime.date.today()

        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context