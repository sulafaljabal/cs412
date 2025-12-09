# project/views.py
# Sulaf Al Jabal (U78815065) 11/24/25
# file description: views for final project
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from .models import * 
from .forms import CreateAppointmentForm, PatientForm, DoctorForm, NurseForm
from django.urls import reverse, reverse_lazy
from .utils import Calendar
from django.utils.safestring import mark_safe
from django.db.models import Q  # For OR queries
import datetime

# Create your views here.

class HomeView(TemplateView):
    """Home page view with system information for administrators"""
    template_name = 'project/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add system statistics
        context['total_patients'] = Patient.objects.count()
        context['total_doctors'] = Doctor.objects.count()
        context['total_nurses'] = Nurse.objects.count()
        context['total_appointments'] = Appointment.objects.count()
        
        # Add current time for footer
        context['current_time'] = datetime.datetime.now()
        
        return context
    #enddef
#endclass

class DoctorListView(ListView):
    """View responsible for showing all doctor records """
    context_object_name = 'doctors'
    template_name = 'project/doctors.html'
    model = Doctor
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class NurseListView(ListView):
    """View responsible for showing all nurse records """
    context_object_name = 'nurses'
    template_name = 'project/nurses.html'
    model = Nurse
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class PatientListView(ListView):
    """View responsible for showing all Patient records with filtering"""
    context_object_name = 'patients'
    template_name = 'project/patients.html'
    model = Patient
    paginate_by = 25  # Show 25 patients per page
    
    def get_queryset(self):
        """Override to add filtering based on query parameters"""
        queryset = Patient.objects.all()
        
        # Get query parameters from the URL
        name_search = self.request.GET.get('name')
        is_adult = self.request.GET.get('isAdult')
        is_child = self.request.GET.get('isChild')
        min_birth_year = self.request.GET.get('min_birth_year')
        max_birth_year = self.request.GET.get('max_birth_year')
        
        # Filter by name (first name OR last name)
        if name_search and name_search.strip() != '':
            queryset = queryset.filter(
                Q(firstName__icontains=name_search) | Q(lastName__icontains=name_search)
            )
        
        # Filter by adult status if checkbox is checked
        if is_adult:
            today = datetime.date.today()
            eighteen_years_ago = datetime.date(today.year - 18, today.month, today.day)
            queryset = queryset.filter(DOB__lte=eighteen_years_ago)
        
        # Filter by child status if checkbox is checked
        if is_child:
            today = datetime.date.today()
            eighteen_years_ago = datetime.date(today.year - 18, today.month, today.day)
            queryset = queryset.filter(DOB__gt=eighteen_years_ago)
        
        # Filter by minimum birth year (born AFTER this year)
        if min_birth_year and min_birth_year != '':
            min_date = datetime.date(int(min_birth_year) + 1, 1, 1)
            queryset = queryset.filter(DOB__gte=min_date)
        
        # Filter by maximum birth year (born BEFORE this year)
        if max_birth_year and max_birth_year != '':
            max_date = datetime.date(int(max_birth_year) - 1, 12, 31)
            queryset = queryset.filter(DOB__lte=max_date)
        
        return queryset.order_by('lastName', 'firstName')
    #enddef
    
    def get_context_data(self, **kwargs):
        """Add birth years list to context for dropdown"""
        context = super().get_context_data(**kwargs)
        current_year = datetime.date.today().year
        context['birth_years'] = range(1900, current_year + 1)
        context['current_time'] = datetime.datetime.now()
        return context
    #enddef
#endclass

class AppointmentListView(ListView):
    """View responsible for showing all Appointment records with filtering"""
    template_name = 'project/appointments.html'
    context_object_name = 'appointments'
    model = Appointment
    paginate_by = 25  # Show 25 appointments per page
    
    def get_queryset(self):
        """Override to add filtering and ordering by time"""
        queryset = Appointment.objects.all()
        
        # Get query parameters from the URL
        appointment_type = self.request.GET.get('appointmentType')
        doctor_id = self.request.GET.get('doctor')
        nurse_id = self.request.GET.get('nurse')
        patient_name = self.request.GET.get('patient_name')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        # Filter by appointment type
        if appointment_type and appointment_type != '':
            queryset = queryset.filter(appointmentType=appointment_type)
        
        # Filter by doctor
        if doctor_id and doctor_id != '':
            queryset = queryset.filter(doctorprovider__doctorID__pk=doctor_id)
        
        # Filter by nurse
        if nurse_id and nurse_id != '':
            queryset = queryset.filter(nurseprovider__nurseID__pk=nurse_id)
        
        # Filter by patient name
        if patient_name and patient_name.strip() != '':
            queryset = queryset.filter(
                Q(patient__firstName__icontains=patient_name) | 
                Q(patient__lastName__icontains=patient_name)
            )
        
        # Filter by date range
        if date_from and date_from != '':
            date_from_obj = datetime.datetime.strptime(date_from, '%Y-%m-%d')
            queryset = queryset.filter(dateTime__gte=date_from_obj)
        
        if date_to and date_to != '':
            date_to_obj = datetime.datetime.strptime(date_to, '%Y-%m-%d')
            date_to_end = date_to_obj + datetime.timedelta(days=1)
            queryset = queryset.filter(dateTime__lt=date_to_end)
        
        # Order by date/time (most recent first)
        return queryset.order_by('-dateTime')
    #enddef
    
    def get_context_data(self, **kwargs):
        """Add additional context for the filter form"""
        context = super().get_context_data(**kwargs)
        
        # Add appointment types for dropdown
        context['appointment_types'] = Appointment.app_choices
        
        # Add all doctors for dropdown
        context['doctors'] = Doctor.objects.all().order_by('lastName', 'firstName')
        
        # Add all nurses for dropdown
        context['nurses'] = Nurse.objects.all().order_by('lastName', 'firstName')
        
        context['current_time'] = datetime.datetime.now()
        
        return context
    #enddef
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
        apps = list(Appointment.objects.filter(patient=patient))
        context['appointments'] = apps
        context['current_time'] = datetime.datetime.now()
        return context 
    #enddef
#endclass

class DoctorDetailView(DetailView):
    """ View resposible for showing information about a particular Doctor"""
    context_object_name = 'doctor'
    template_name = 'project/doctor.html'
    model = Doctor
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class NurseDetailView(DetailView):
    """ View resposible for showing information about a particular Nurse"""
    context_object_name = 'nurse'
    template_name = 'project/nurse.html'
    model = Nurse
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class AppointmentDetailView(DetailView):
    """ View responsible for showing information about a particular appointment
    Shows patient, nurse(s), doctor, date of appointment """
    template_name = 'project/appointment.html'
    model = Appointment
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class CreatePatientView(CreateView):
    """View for administrative staff to create new patient records"""
    model = Patient
    form_class = PatientForm
    template_name = 'project/patient_form.html'
    
    def get_success_url(self):
        """Redirect to the patient detail page after creation"""
        return reverse('patient', kwargs={'pk': self.object.pk})
    #enddef
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class UpdatePatientView(UpdateView):
    """View for administrative staff to update existing patient records"""
    model = Patient
    form_class = PatientForm
    template_name = 'project/patient_form.html'
    
    def get_success_url(self):
        """Redirect back to the patient detail page after update"""
        return reverse('patient', kwargs={'pk': self.object.pk})
    #enddef
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class CreateDoctorView(CreateView):
    """View for administrative staff to create new doctor records"""
    model = Doctor
    form_class = DoctorForm
    template_name = 'project/doctor_form.html'
    
    def get_success_url(self):
        """Redirect to the doctor detail page after creation"""
        return reverse('doctor', kwargs={'pk': self.object.pk})
    #enddef
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class UpdateDoctorView(UpdateView):
    """View for administrative staff to update existing doctor records"""
    model = Doctor
    form_class = DoctorForm
    template_name = 'project/doctor_form.html'
    
    def get_success_url(self):
        """Redirect back to the doctor detail page after update"""
        return reverse('doctor', kwargs={'pk': self.object.pk})
    #enddef
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class CreateNurseView(CreateView):
    """View for administrative staff to create new nurse records"""
    model = Nurse
    form_class = NurseForm
    template_name = 'project/nurse_form.html'
    
    def get_success_url(self):
        """Redirect to the nurse detail page after creation"""
        return reverse('nurse', kwargs={'pk': self.object.pk})
    #enddef
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class UpdateNurseView(UpdateView):
    """View for administrative staff to update existing nurse records"""
    model = Nurse
    form_class = NurseForm
    template_name = 'project/nurse_form.html'
    
    def get_success_url(self):
        """Redirect back to the nurse detail page after update"""
        return reverse('nurse', kwargs={'pk': self.object.pk})
    #enddef
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class CreateAppointmentView(CreateView):
    """
    View for administrative staff to create new appointments.
    """
    model = Appointment
    form_class = CreateAppointmentForm
    template_name = 'project/create_appointment.html'
    
    def get_form_kwargs(self):
        """
        Pass initial values to the form based on URL parameters.
        """
        kwargs = super().get_form_kwargs()
        
        # Check if date and hour are provided (from day schedule time slot)
        date_str = self.request.GET.get('date')
        hour_str = self.request.GET.get('hour')
        
        if date_str and hour_str:
            try:
                year, month, day = map(int, date_str.split('-'))
                hour = int(hour_str)
                initial_datetime = datetime.datetime(year, month, day, hour, 0)
                kwargs['initial_datetime'] = initial_datetime
            except (ValueError, TypeError) as e:
                pass
        
        # Check if patient is provided (from patient detail page)
        patient_id = self.request.GET.get('patient')
        if patient_id:
            try:
                patient = Patient.objects.get(pk=int(patient_id))
                kwargs['initial_patient'] = patient
            except (ValueError, Patient.DoesNotExist) as e:
                pass
        
        return kwargs
    #enddef
    
    def form_valid(self, form):
        """
        Save the appointment and create associated provider records.
        """
        # Save the appointment first
        self.object = form.save()
        
        # Get the selected doctors and nurses from the form
        doctors = form.cleaned_data.get('doctors', [])
        nurses = form.cleaned_data.get('nurses', [])
        
        # Create DoctorProvider records for each selected doctor
        for doctor in doctors:
            DoctorProvider.objects.create(
                appointmentID=self.object,
                doctorID=doctor
            )
        
        # Create NurseProvider records for each selected nurse
        for nurse in nurses:
            NurseProvider.objects.create(
                appointmentID=self.object,
                nurseID=nurse
            )
        
        return super().form_valid(form)
    #enddef
    
    def get_success_url(self):
        """Redirect to the appointment detail page after successful creation"""
        return reverse('appointment', kwargs={'pk': self.object.pk})
    #enddef
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class DeleteAppointmentView(DeleteView):
    """
    View for administrative staff to delete appointments.
    """
    model = Appointment
    template_name = 'project/delete_appointment.html'
    context_object_name = 'appointment'
    
    def get_success_url(self):
        """Redirect to appointments list after successful deletion"""
        return reverse_lazy('appointments')
    #enddef
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

def prev_month(d):
    """Helper function to get the previous month"""
    first = d.replace(day=1)
    prev_month_date = first - datetime.timedelta(days=1)
    month = 'month=' + str(prev_month_date.year) + '-' + str(prev_month_date.month)
    return month

def next_month(d):
    """Helper function to get the next month"""
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if d.year % 4 == 0 and (d.year % 100 != 0 or d.year % 400 == 0):
        days_in_month[1] = 29
    days = days_in_month[d.month - 1]
    last = d.replace(day=days)
    next_month_date = last + datetime.timedelta(days=1)
    month = 'month=' + str(next_month_date.year) + '-' + str(next_month_date.month)
    return month

def get_date(req_day):
    """Helper function to get date from request"""
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.date.today()

def get_full_date(req_date):
    """Helper function to get a specific date (including day) from request"""
    if req_date:
        year, month, day = (int(x) for x in req_date.split('-'))
        return datetime.date(year, month, day)
    return datetime.date.today()

def prev_day(d):
    """Helper function to get the previous day"""
    prev = d - datetime.timedelta(days=1)
    return f'date={prev.year}-{prev.month}-{prev.day}'

def next_day(d):
    """Helper function to get the next day"""
    next_d = d + datetime.timedelta(days=1)
    return f'date={next_d.year}-{next_d.month}-{next_d.day}'

class CalendarView(ListView):
    """ View responsible for showing calendar with appointments """
    model = Appointment
    template_name = 'project/appointment_calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))

        # Filter appointments for the current month being viewed
        appointments_this_month = Appointment.objects.filter(
            dateTime__year=d.year, 
            dateTime__month=d.month
        )
        
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['current_month'] = d
        context['appointments_this_month'] = appointments_this_month
        context['current_time'] = datetime.datetime.now()
        return context
#endclass

class DayScheduleView(ListView):
    """View responsible for showing day-by-day schedule"""
    model = Appointment
    template_name = 'project/day_schedule.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_full_date(self.request.GET.get('date', None))
        
        # Get all appointments for this specific day
        appointments_today = Appointment.objects.filter(
            dateTime__year=d.year,
            dateTime__month=d.month,
            dateTime__day=d.day
        ).order_by('dateTime')
        
        # Create a time slot structure (8 AM to 8 PM by default)
        hours = range(0, 24)
        time_slots = []
        
        for hour in hours:
            slot = {
                'hour': hour,
                'display_time': datetime.time(hour, 0).strftime('%I:%M %p'),
                'appointments': [],
                'date': d,
            }
            
            # Find appointments that fall within this hour
            for appt in appointments_today:
                if appt.dateTime.hour == hour:
                    slot['appointments'].append(appt)
            
            time_slots.append(slot)
        
        context['current_date'] = d
        context['appointments_today'] = appointments_today
        context['time_slots'] = time_slots
        context['prev_day'] = prev_day(d)
        context['next_day'] = next_day(d)
        context['current_time'] = datetime.datetime.now()
        
        return context
#endclass