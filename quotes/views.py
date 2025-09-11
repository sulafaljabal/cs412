# file: quotes/views.py

# Sulaf Al Jabal (sulafaj@bu.edu) 09/09/25
# Description: functions here control the view of our quotes page


from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time # importing time for footer
import random # helps choose random image and quote

images = ["https://i.scdn.co/image/ab6761610000e5ebee3852e6b5500f0af5315609",
    "https://upload.wikimedia.org/wikipedia/commons/c/cf/Rex_Orange_County_-_Photo_by_Skyler_Pradhan_%28cropped%29.jpg", 
    "https://images.squarespace-cdn.com/content/v1/5b0dd7581aef1d319395b854/3e40b126-e45f-48cb-93ca-a8b19fe61b83/ROC+by+alexandra+waespi.jpg", 
    "https://s3-us-west-2.amazonaws.com/onestowatch-v2/rex-orange-county-who-cares_1647291131.jpg",
    "https://www.nme.com/wp-content/uploads/2022/03/nme-cover-2022-rex-orange-county-hero@2560x1625.jpg"
] # 5 images of Rex Orange County

quotes = [
    "The moment you start thinking about what other people and other artists think, you're going to start writing like other people.", 
    "I think there's no limit to ambition, and if you want something, you can make anything happen, so go for it.", 
    "I just want to tell people how I am.", 
    "I'm afraid of peacocks.",
    "As long as you're being yourself and putting out what you want to put out, it'll be the best thing you could do."
] # 5 quotes by Rex Orange County from BrainyQuote.com



def home_page(request):
    """ Respond to the URL '', delegate work to a template"""

    template_name = "quotes/home_page.html"
    # a list with a dictionary of context variables (key-value pairs)
    # first value of list: dictionary of quotes
    # second value of list: dictionary of photos

    # picking random image and quote
    image = images[random.randint(0,len(images)-1)]
    quote = quotes[random.randint(0,len(images)-1)]

    # passing three context variables to the template
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

    # a dictionary of context variables 
    context = {
        "wiki_link": "https://en.wikipedia.org/wiki/Rex_Orange_County", # wiki link for more info on artist
        "time": time.ctime(),
    }

    return render(request, template_name, context)
#end def

def show_all_page(request):
    """ Respond to the URL 'show_all', delegate work to a template """

    template_name = "quotes/show_all_page.html"

    # dictionary of context variables, this page needs all quotes and images
    context = {
        "images" : images,
        "quotes" : quotes,
        "time": time.ctime(),
    }

    return render(request, template_name, context)
# end show_all_page def

def quote_page(request):
    """ Respond to the URL 'quote', redirect to home page """
    return home_page(request)
# end quote_page def