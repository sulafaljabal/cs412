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

class UpdateProfileForm(forms.ModelForm):
    """A form to update a Profile"""
    class Meta:
        """Associate the form with a model from our db"""
        model = Profile 
        fields = ['profile_image_file', 'display_name', 'bio_text'] # cant change username or joindate

    #endMeta
#end class UpdateProfileForm

class UpdatePostForm(forms.ModelForm):
    """A form to update a Post""" # not entirely sure how to code this...
    class Meta:
        """Associate the form with a model from our db"""
        model = Post 
        fields = ['caption'] # cant change timestamp or profile

    #endMeta
#end class UpdateProfileForm