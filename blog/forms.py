# blog/forms.py
# Define the forms that we use for create/update/delete

from django import forms
from .models import Article, Comment # Article, Comment

class CreateArticleForm(forms.ModelForm):
    """A form to add an Article to the database"""

    class Meta:
        """Asociate this form with a model from our database"""
        model = Article 
        fields = ['author', 'title', 'text', 'image_file']
#end class

class CreateCommentForm(forms.ModelForm):
    """A form to add a Comment about an Article"""

    class Meta:
        """associate this form with the Comment model; select fields"""
        model = Comment 
        fields = [ 'author', 'text'] # specifies which fields from model we should use
    #end class meta
#end class CreateCommentForm

class UpdateArticleForm(forms.ModelForm):
    """A form to update a quote to the database """

    class Meta:
        """associate this form with the Article Model"""
        model = Article 
        fields = ['title', 'text']
    #end meta
#end class UpdateArticle Form