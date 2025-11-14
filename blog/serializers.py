# blog/serializers.py
# converts our django data models to a text-representation suitable to transmit over HTTP

from rest_framework import serializers
from .models import *
# from django.auth


class ArticleSerializer(serializers.ModelSerializer):
    """serializer for the Article model
    Specify which model and which fields to send in the API
    ???"""

    class Meta:
        """Specify which model to use"""
        model = Article 
        fields = ['id', 'title', 'author', 'text']
    #end Meta 

    # add methods to customize the Create/eRead/Update/Delete operations
    # if you have multiple models, you create one seralizer model for each


    def create(self, validated_data):
        """ override the superclass method that handles object creation """
        print(f"ArticleSerializer.create, validated_data= {validated_data}")
        # old method, changed below
        # # create an Article object
        # article = Article(**validated_data)
        # # attach a FK for the user 
        # article.user = User.objects.first()
        # # save the object to the database 
        # article.save()
        # #this needs to return an object instance

        # you can collect logged in user information to create a new article tied to the correct person instead
        # of using the superuser: 
        # session token: uniquely identifies who's logged in 


        # do the create and save all together
        return Article.objects.create(**validated_data) 

    #enddef