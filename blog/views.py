from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
import random 
from .forms import * # CreateArticleForm, CreateCommentForm #CreateArticleForm CreateCommentForm, UpdateArticleForm
from django.urls import reverse

# Create your views here.

class ShowAllView(ListView):
    """Define a veiw class to show all blog Articles"""

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"


class ArticleView(DetailView):
    """DIsplays a single article"""

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"
#end class

class RandomArticleView(DetailView):
    """Displays a single random article"""

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    def get_object(self):
        """return one instance of the Article object selected
        at random. Overiding a function"""

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
    #end get_object
#endclass

class CreateArticleView(CreateView):
    """A view to handle creation of a new Article
    1) display the HTML to the user (GET)
    2) process the form submission and store the new Article object (POST)
    
    """

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        """Handle the form submission to create a new Article object """
        print(f"CreateArticleView: form.cleaned_data={form.cleaned_data}")

        # delegate work to superclass version of this method
        return super().form_valid(form)
    #end form_valid method
#end class

class CreateCommentView(CreateView):
    """A view to create a new comment and save it to the database"""

    form_class = CreateCommentForm 
    template_name = "blog/create_comment_form.html"

    def form_valid(self, form):
        """This method handles form submission and saves the new object to the Django database
        Need to add foreign key (of Article) to the Comment object before saving it to db"""

        print(f"CreateCommentView.form_valid: form.cleaned_data={form.cleaned_data}")

        # get PK from URL pattern 
        pk = self.kwargs['pk'] # extracting parameter
        article = Article.objects.get(pk=pk)

        #attach this article to the comment 
        form.instance.article = article # set the FK
        
        # overriding form_valid to attach pk to comment
        # delegate work to the superclass method form_valid:
        return super().form_valid(form)
    #enddef form_valid

    def get_success_url(self) -> str:
        """Return the URL to redirect to after creating a new Comment."""
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article

        return reverse('article', kwargs={'pk': pk})
    #enddef

    def get_context_data(self):
        """return the dictionary of context variables for use in the template"""

        # Calling the superclass method 
        context = super().get_context_data()

        # find/add the article to the context data
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['article'] = article 
        return context 
    #enddef

#endclass

class UpdateArticleView(UpdateView):
    """A view to update an Article and save it to the database."""

    model = Article
    form_class = UpdateArticleForm 
    template_name = "blog/update_article_form.html"

    def form_valid(self, form):
        """Handle the form submission to create a new Article object"""
        print(f"UpdateArticleView: form.cleaned_data={form.cleaned_data}")

        return super().form_valid(form)
    #enddef
#end class UpdateArticleView

class DeleteCommentView(DeleteView):
    """ a view to delete a comment and remove it from the database"""

    template_name = "blog/delete_comment_form.html"
    model = Comment 
    context_object_name = 'comment'

    def get_success_url(self):
        """Return the URL to which we should be directed to after the delete"""

        # finding primary key of this comment
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)

        # find article to which this Comment is related by FK
        article = comment.article 

        # return reverse (instead of super class) to show the article page 

        return reverse('article', kwargs={'pk':article.pk})
#endclass

################################################################################################################################

# REST API
from rest_framework import generics # special generica api classes like DetailView, CreateView, UpdateView, etc
from .serializers import *

class ArticleListAPIView(generics.ListCreateAPIView):
    """
    An API view to return a listing of Articles and to create an Article.
    """
    queryset = Article.objects.all() # this can be customized
    serializer_class = ArticleSerializer 
#endclass