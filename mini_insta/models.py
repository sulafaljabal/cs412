# mini_insta/models.py
# Sulaf Al Jabal (09/24/25)
# define data models for the mini_insta application

from django.db import models

class Profile(models.Model): # instances of users Profiles
    """ Encapsulate the data of a mini_insta Profile. Contains user's username, display name, profile picture, join date and some biographical information."""

    # define data attribute of the Profile object

    username = models.TextField(blank=True) 
    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        """returns a string representation of this model instance"""
        return f"{self.username}: {self.display_name}\nJoined: {self.join_date}\nBio: {self.bio_text}\nProfile Pic: {self.profile_image_url}"
    #end

#end class article