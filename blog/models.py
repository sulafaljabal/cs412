# blog/models.py
# define data models for the blog application

from django.db import models

# Create your models here.
class Article(models.Model): # instances of articles people write
    """ Encapsulate the data of a blog Article by an author."""
    # define data attribute of the Article object

    title = models.TextField(blank=True) # blank=true so we can create a title without specifying the title
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    #sets time of article published immediately 
    image_url = models.URLField(blank=True)

    def __str__(self):
        """returns a string representation of this model instance"""
        return f"{self.title} by {self.author}"
    #end

#end class article