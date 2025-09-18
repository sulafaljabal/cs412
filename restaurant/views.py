
# restaurant/views.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/16/25
# Description: views for restaurant application

from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime, timedelta
import random

image = "https://farm6.staticflickr.com/5519/10419588133_fce1ee6637_c.jpg"

menu_items = { # dictionary of all menu items and their prices
    "chicken_shawarma" : 3.0,
    "beef_shawarma" : 3.5,
    "beef_chicken_shawarma" : 6.0,
    "french_fries" : 2.0,
    "pepsi" : 1.0,
    "seven_up" : 1.0,
    "fanta_orange" : 1.0,
    "fanta_lemon" : 1.0,
    "coffee" : 2.0,
}

specials = { # dictionary of all specials, random one will be chosen
    "Lamb_Plate" : 5,
    "Shish_Tawook_(chicken)" : 4,
    "Chicken_Corn_Soup" : 2,
}

# Start of views

def main(request):
    """ Respond to url '/main', delegates work to a template"""
    template_name = "restaurant/main.html"

    context = {
        "time" : datetime.now(), # time for footer
        "image" : image,
    }

    return render(request, template_name=template_name, context=context)
# end def

def order(request):
    """Responds to url '/order'. Shows the form to user. Delegates work to a template"""

    template_name = "restaurant/order.html"

    random_special = random.choice(list(specials.keys())) # picking a random special
    special_price = specials[random_special] 

    random_special_processed = random_special.replace('_', ' ') # changing name of special to a more appropriate version for end user

    context = {
        "time" :datetime.now(),
        "special_item": random_special,
        "special_item_name" : random_special_processed, # separating the displayed name from the variable name to avoid crashes
        "special_price": special_price
    }
    #print(context)

    return render(request, template_name=template_name, context=context)
#end show_form

def submit(request):
    """ Process the form submission, and generate a result. Delegate work to a template"""

    template_name = "restaurant/confirmation.html"

    # check if POST data was sent with the HTTP POST message, else return time
    if request.method == "POST":

        # extract form fields into variables:

        name = request.POST.get('name', '') # establishing default value for important fields
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        special_instructions = request.POST.get('special_instructions', '')

        context = {
            'name' : name,
            'phone' : phone,
            'email' : email,
            'special_instructions' : special_instructions,
            'time' : datetime.now(),

        }


        selected_menu_items = {} # creating separate dictionary for easier iteration in html templates
        total_price = 0.0 

        for item in menu_items.keys(): # going through every menu item
            if request.POST.get(item): # checking if menu item has been selected
                        
                selected_menu_items[request.POST.get(item)] = menu_items[item] # creating new menu item in dictionary and adding price

            #go to next menu item
        #endfor 

        if request.POST.get('special'): # check if specials was checked or not
                
            special_name = request.POST.get('special') # grabbing name of the variable special, not the display name
            special_price = specials[special_name] # grabbing special price before changing name 
            special_name = special_name.replace('_', ' ') # removing underscore to pass more acceptable version of special name to end user
            selected_menu_items[special_name] = special_price
        #endif


        context["selected_menu_items"] = selected_menu_items # adding selected menu items to context
        context["total_price"] = sum(selected_menu_items.values()) # adding price of food/drinks

        current_time = datetime.now()
        random_minutes = random.randint(30, 60)
        ready_time = current_time + timedelta(minutes=random_minutes) # adding random amount of time between half and hour to an hour for 
        # food preparation
        ready_time_formatted = ready_time.strftime("%I:%M %p") # formatting time for user

        context["order_time"] = ready_time_formatted
        
    else:
        context = {"time" : datetime.now()}
    #endif

    return render(request, template_name, context)
#end submit
