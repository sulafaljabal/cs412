# dadjokes/serializers.py
# Sulaf Al Jabal (U78815065) 11/11/25
# File description: converts our django data models to a text-representation suitable to transmit over HTTP

from rest_framework import serializers
from .models import *


class JokeSerializer(serializers.ModelSerializer):
    """
    serializer for the Joke model
    Specify which model and which fields to send in the API
    """

    class Meta:
        """Specify which model to use"""
        model = Joke 
        fields = [ 'name', 'text', 'timestamp']
    #end Meta 

    # add methods to customize the Create/eRead/Update/Delete operations
    # if you have multiple models, you create one seralizer model for each


    # def create(self, validated_data):
    #     """ override the superclass method that handles object creation """
    #     print(f"ArticleSerializer.create, validated_data= {validated_data}")

    #     validated_data['user'] = User.objects.first()
    #     # do the create and save all together
    #     return Article.objects.create(**validated_data) 

    #enddef
#end Joke serializer

class PictureSerializer(serializers.ModelSerializer):
    """???"""
    class Meta:
        model = Picture 
        fields = ['timestamp', 'image_url', 'name']
    #end meta 

    # might need a create function...
#endclass