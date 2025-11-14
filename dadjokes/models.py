# dadjokes/models.py 
# Sulaf Al Jabal (U78815065) 11/11/2025
# File description: defining Joke and Picture models

from django.db import models
from django.urls import reverse

# Create your models here.
class Joke(models.Model): # instances of joke people write
    """ Encapsulate the data of a blog Joke."""

    name = models.TextField(blank=True) # blank=true so we can create a title without specifying the title
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        """returns a string representation of this model instance"""
        return f"Joke by {self.name}: {self.text}\n{self.timestamp}"
    #end

#end class Joke

class Picture(models.Model):
    """Encapsultes the idea of a Picture????? """

    # data attributes of a Picture:
    name = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of this Picture object"""

        return f'Image {self.image_url} by {self.name}\n{self.timestamp}'
    #enddef
    
    def get_image(self):
        return self.image_url # only ImageFile types have a .url method...
    #enddef

#end comment class