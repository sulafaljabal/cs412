# file: quotes/views.py

# Sulaf Al Jabal (sulafaj@bu.edu) 09/09/25
# Description: functions here control the view of our quotes page


from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

images = ["https://i.scdn.co/image/ab6761610000e5ebee3852e6b5500f0af5315609",
    "https://upload.wikimedia.org/wikipedia/commons/c/cf/Rex_Orange_County_-_Photo_by_Skyler_Pradhan_%28cropped%29.jpg", 
    "https://images.squarespace-cdn.com/content/v1/5b0dd7581aef1d319395b854/3e40b126-e45f-48cb-93ca-a8b19fe61b83/ROC+by+alexandra+waespi.jpg", 
    "https://s3-us-west-2.amazonaws.com/onestowatch-v2/rex-orange-county-who-cares_1647291131.jpg",
]

quotes = [
    "The moment you start thinking about what other people and other artists think, you're going to start writing like other people.", 
    "I think there's no limit to ambition, and if you want something, you can make anything happen, so go for it.", 
    "I just want to tell people how I am.", 
    "I'm afraid of peacocks."
]




# Create your views here.

def home_page(request):
    """ Respond to the URL '', delegate work to a template"""

    template_name = "quotes/home_page.html"
    # a list with a dictionary of context variables (key-value pairs)
    # first value of list: dictionary of quotes
    # second value of list: dictionary of photos

    random_int = random.randint(0,len(images)-1)

    image = images[random_int]
    quote = quotes[random_int]

    context = {
        "image" : image,
        "quote" : quote,
        "time": time.ctime(),

    }

    return render(request, template_name, context)
#end home_page

def about_page(request):
    """ Respond to the URL 'about', delegate work to a template"""

    template_name = "quotes/about_page.html"

    # a dictionary of context variables (key-value pairs)
    context = {
        "wiki_link": "https://en.wikipedia.org/wiki/Rex_Orange_County",
        "time": time.ctime(),
    }

    return render(request, template_name, context)
#end def

def show_all_page(request):
    """ Respond to the URL 'show_all', delegate work to a template """

    template_name = "quotes/show_all_page.html"


    context = {
        "images" : images,
        "quotes" : quotes,
        "time": time.ctime(),
    }

    return render(request, template_name, context)
# end show_all_page def

def quote_OTD_page(request):
    """ Respond to the URL 'quote_OTD', delegate work to a template """

    template_name = "quotes/quote_OTD_page.html"

    random_int = random.randint(0,len(images)-1)

    image = images[random_int]
    quote = quotes[random_int]
    
    context = {
        "image" : image,
        "quote" : quote,
        "time": time.ctime(),
    }

    return render(request, template_name, context)
# end show_all_page def