# mini_insta/admin.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/25/25
# Description: registering models within admin page
from django.contrib import admin

# Register your models here.

from .models import Profile
admin.site.register(Profile)
