# mini_insta/admin.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/25/25
# Description: registering models within admin page
from django.contrib import admin

# Register your models here.

from .models import * # Profile, Photo, Post
admin.site.register(Profile) # registering Profile model
admin.site.register(Photo) # registering Photo model
admin.site.register(Post) # registering Post model
admin.site.register(Follow) # registering Follow model
