# project/admin.py
# Sulaf Al Jabal (U78815065) 11/20/2025
# File description: registering all models within django admin tool
from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Appointment) # registering Appointment model
admin.site.register(Doctor) # registering Doctor model
admin.site.register(Patient) # registering PatientD model
admin.site.register(Nurse) # registering Nurse model
admin.site.register(NurseProvider) # registering NurseProvider model (appointment creation)
admin.site.register(DoctorProvider) # registering Nurse model (appointment creation)
