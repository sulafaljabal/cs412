# mini_insta/models.py
# Sulaf Al Jabal (09/24/25)
# define data models for the mini_insta application

from django.db import models

class Profile(models.Model): # instances of articles people write
    """ Encapsulate the data of a mini_insta Profile
    Contains user's username, display name, profile picture, join date
    and some biographical information."""

    # define data attribute of the Article object

    username = models.TextField(blank=True) # blank=true so we can create a title without specifying the title
    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        """returns a string representation of this model instance"""
        return f"{self.username}: {self.display_name}\nJoined: {self.join_date}"
    #end
    # not sure if this needs more in it 

#end class article