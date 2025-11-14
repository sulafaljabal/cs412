# dadjokes/views.py
# Sulaf Al Jabal (U78815065) 11/11/2025
# File description: defining all the views within the dadjokes application

from django.shortcuts import render
# from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import random 

# API imports
from rest_framework import generics # special generica api classes like DetailView, CreateView, UpdateView, etc
from .serializers import *

# Create your views here.

def randomJokeView(request):
    """ View responsible choosing random picture and joke """
    template_name = "dadjokes/random.html"
    context = {}
    joke = random.choice(list(Joke.objects.all()))
    picture = random.choice(list(Picture.objects.all()))
    context['joke'] = joke 
    context['picture'] = picture 

    return render(request, context=context, template_name=template_name) 
    #enddef
#enddef

class JokeListView(ListView):
    """Showcases all instances of Joke object"""
    template_name  = "dadjokes/show_all_jokes.html"
    context_object_name = 'jokes'
    model = Joke 

#endclass

class JokeDetailView(DetailView):
    """ Showcases information about a partical Joke instance"""
    template_name = "dadjokes/joke.html"
    context_object_name = 'joke'
    model = Joke 
#endclass 

class PictureListView(ListView):
    """ View responsible for showcasing all Picture object instances"""
    template_name = "dadjokes/show_all_pictures.html"
    context_object_name = 'pictures'
    model = Picture 
#endclass

class PictureDetailView(DetailView):
    """ Showcases information about a partical Picture instance """
    template_name = "dadjokes/picture.html"
    context_object_name = "picture"
    model = Picture 
#endclass
