# dadjokes/serializers.py
# Sulaf Al Jabal (U78815065) 11/11/25
# File description: converts our django data models to a text-representation suitable to transmit over HTTP

from rest_framework import serializers
from .models import *


class JokeSerializer(serializers.ModelSerializer):
    """
    serializer for the Joke model
    Users can also create jokes using this
    """

    class Meta:
        """Specify which model to use"""
        model = Joke 
        fields = [ 'name', 'text', 'timestamp']
    #end Meta 


#end Joke serializer

class PictureSerializer(serializers.ModelSerializer):
    """Serializer for Picture model. 
    Users CANNOT create new pictures using"""
    
    class Meta:
        model = Picture 
        fields = ['timestamp', 'image_url', 'name']
    #end meta 
#endclass