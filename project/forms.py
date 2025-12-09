# project/forms.py
# Sulaf Al Jabal (U78815065) 12/6/2024
# File description: Forms for administrative staff to create and manage appointments, patients, doctors, and nurses

from django import forms
from .models import Appointment, Patient, Doctor, Nurse, DoctorProvider, NurseProvider
import datetime

class CreateAppointmentForm(forms.ModelForm):
    """Form for administrative staff to create appointments for patients"""
    
    dateTime = forms.DateTimeField( # need to specify datetime-local or else issues arise
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Appointment Date & Time'
    )
    
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all().order_by('lastName', 'firstName'),
        label='Patient'
    )
    
    problem = forms.CharField(
        max_length=200,
        label='Chief Complaint'
    )
    
    problemDescription = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        label='Detailed Description'
    )
    
    appointmentType = forms.ChoiceField(
        choices=Appointment.app_choices,
        label='Appointment Type'
    )
    
    doctors = forms.ModelMultipleChoiceField(
        queryset=Doctor.objects.all().order_by('lastName', 'firstName'),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Assign Doctor(s)'
    )
    
    nurses = forms.ModelMultipleChoiceField(
        queryset=Nurse.objects.all().order_by('lastName', 'firstName'),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Assign Nurse(s)'
    )
    
    class Meta:
        model = Appointment
        fields = ['patient', 'dateTime', 'problem', 'problemDescription', 'appointmentType']
    #endclass
    
    def __init__(self, *args, **kwargs):
        """Initialize form with optional pre-filled values"""

        # checking for datetime and patient and assigning if possible
        initial_datetime = kwargs.pop('initial_datetime', None)
        initial_patient = kwargs.pop('initial_patient', None)
        
        super().__init__(*args, **kwargs)
        
        if initial_datetime and 'dateTime' not in self.initial:
            self.initial['dateTime'] = initial_datetime
        
        if initial_patient and 'patient' not in self.initial:
            self.initial['patient'] = initial_patient
        
        self.fields['patient'].required = True
        self.fields['dateTime'].required = True
        self.fields['problem'].required = True
        self.fields['problemDescription'].required = True
        self.fields['appointmentType'].required = True
        self.fields['doctors'].required = True
        self.fields['nurses'].required = True
    #enddef
    
    def clean_dateTime(self):
        """Validate that appointment is not in the past"""
        datetime_value = self.cleaned_data['dateTime']
        
        # Simple comparison - just use naive datetimes
        # If datetime_value has timezone info, remove it - application crashes when timezones are implemented
        if datetime_value.tzinfo is not None:
            datetime_value = datetime_value.replace(tzinfo=None)
        
        # Get current time as naive datetime
        now = datetime.datetime.now()
        one_hour_ago = now - datetime.timedelta(hours=1)
        
        if datetime_value < one_hour_ago:
            raise forms.ValidationError(
                "Cannot create an appointment more than 1 hour in the past."
            )
        
        return datetime_value
    #enddef
    
    def clean(self):
        """Additional validation for the entire form"""
        cleaned_data = super().clean()
        appointment_type = cleaned_data.get('appointmentType')
        doctors = cleaned_data.get('doctors')
        
        if appointment_type == 'NA': # nurse only appointment, no doctors needed
            self.fields['doctors'].required = False
            cleaned_data['doctors'] = []
        else: # not a nurse only appointment
            if not doctors or not doctors.exists():
                raise forms.ValidationError(
                    "At least one doctor is required for this appointment type."
                )
        
        return cleaned_data
    #enddef
    
#endclass


class PatientForm(forms.ModelForm):
    """Form for creating and updating patient records"""
    
    firstName = forms.CharField(
        max_length=100,
        label='First Name'
    )
    
    lastName = forms.CharField(
        max_length=100,
        label='Last Name'
    )
    
    middleName = forms.CharField(
        max_length=100,
        required=False,
        label='Middle Name'
    )
    
    DOB = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date of Birth'
    )
    
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        required=False,
        label='Address'
    )
    
    primaryCareDoctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all().order_by('lastName', 'firstName'),
        required=False,
        label='Primary Care Doctor',
        empty_label='No Primary Care Doctor'
    )
    
    picture = forms.ImageField(
        required=False,
        label='Profile Picture'
    )
    
    class Meta:
        model = Patient
        fields = ['firstName', 'lastName', 'middleName', 'DOB', 'address', 'primaryCareDoctor', 'picture']
    #endclass
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make required fields explicit
        self.fields['firstName'].required = True
        self.fields['lastName'].required = True
        self.fields['DOB'].required = True
    #enddef
    
    def clean_DOB(self):
        """Validate that date of birth is not in the future"""
        dob = self.cleaned_data['DOB']
        
        if dob > datetime.date.today():
            raise forms.ValidationError(
                "Date of birth cannot be in the future."
            )
        
        return dob
    #enddef
    
#endclass


class DoctorForm(forms.ModelForm):
    """Form for creating and updating doctor records"""
    
    firstName = forms.CharField(
        max_length=100,
        label='First Name'
    )
    
    lastName = forms.CharField(
        max_length=100,
        label='Last Name'
    )
    
    specialty = forms.CharField(
        max_length=200,
        required=False,
        label='Specialty'
    )
    
    picture = forms.ImageField(
        required=False,
        label='Profile Picture'
    )
    
    class Meta:
        model = Doctor
        fields = ['firstName', 'lastName', 'specialty', 'picture']
    #endclass
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make required fields explicit
        self.fields['firstName'].required = True
        self.fields['lastName'].required = True
    #enddef
    
#endclass


class NurseForm(forms.ModelForm):
    """Form for creating and updating nurse records"""
    
    firstName = forms.CharField(
        max_length=100,
        label='First Name'
    )
    
    lastName = forms.CharField(
        max_length=100,
        label='Last Name'
    )
    
    picture = forms.ImageField(
        required=False,
        label='Profile Picture'
    )
    
    class Meta:
        model = Nurse
        fields = ['firstName', 'lastName', 'picture']
    #endclass
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make required fields explicit
        self.fields['firstName'].required = True
        self.fields['lastName'].required = True
    #enddef
    
#endclass