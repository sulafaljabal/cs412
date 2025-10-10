# blog/models.py
# define data models for the blog application

from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model): # instances of articles people write
    """ Encapsulate the data of a blog Article by an author."""
    # define data attribute of the Article object

    title = models.TextField(blank=True) # blank=true so we can create a title without specifying the title
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    #sets time of article published immediately 
    #image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True) # an actual image


    def __str__(self):
        """returns a string representation of this model instance"""
        return f"{self.title} by {self.author}"
    #end
    def get_absolute_url(self):
        """ return the URL to display one instance of this model """
        return reverse('article', kwargs={'pk': self.pk})
    #enddef

    def get_all_comments(self):
        """return all of the comments (query set ) about this article"""

        comments = Comment.objects.filter(article=self)
        return comments 
    #enddef

#end class article

class Comment(models.Model):
    """Encapsultes the idea of a Comment on an Article """

    # data attributes of a Comment:
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank = False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of this Comment object"""

        return f'{self.text}'
    #enddef
#end comment class