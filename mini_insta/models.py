# mini_insta/models.py
# Sulaf Al Jabal (09/24/25)
# define data models for the mini_insta application

from django.db import models

class Profile(models.Model): # instances of users Profiles
    """ Encapsulate the data of a mini_insta Profile. Contains user's username, display name, 
    profile picture, join date and some biographical information."""

    username = models.TextField(blank=True) 
    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        """returns a string representation of this model instance"""
        return f"{self.username}: {self.display_name}\nJoined: {self.join_date}\nBio: {self.bio_text}\nProfile Pic: {self.profile_image_url}"
    #end

    def get_all_posts(self):
        """returns all of the posts on this profile"""

        posts = Post.objects.filter(profile=self) 
        return posts 
    #enddef

#end class Profile

class Post(models.Model): # instances of users Post on a Profile
    """ Encapsulate the data of a mini_insta Post on a user's Profile. Contains post's timestamp,
    caption, and profile it is connected to """

    # define data attribute of the Post object

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """returns a string representation of this model instance"""
        return f"Post by {self.profile}: {self.caption}\nPosted at: {self.timestamp}"
    #end

    def get_all_photos(self):
        """accessor method that gets all photos related to a certain post."""
        photos = Photo.objects.filter(post=self)
        return photos 
    #enddef


#end class Post

class Photo(models.Model): # instances of users Profiles
    """ Encapsulate the data of a mini_insta Photo. Contains a photo's timestamp, image_URL
    and what Post it is connected to ."""

    # define data attribute of the Photo object

    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)


#end class Photo