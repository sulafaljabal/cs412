# mini_insta/forms.py
# Sulaf Al Jabal (sulafaj@bu.edu) 10/03/2025
# Define the forms that we use for create/update/delete

from django import forms
from .models import * # AProfile, Photo, Post



class CreatePostForm(forms.ModelForm):
    """A form to add an Post to a certain Profile"""

    class Meta:
        """Asociate this form with a model from our database"""
        model = Post 
        fields = ['caption'] # timestamp collected automatically, profile linked already
#end class


