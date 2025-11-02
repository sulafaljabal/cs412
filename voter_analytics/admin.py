# voter_analytics/admin.py
# Sulaf Al Jabal (U78815065) 10/31/25
# File description: admin.py file, registered Voter model in admin page

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Voter)