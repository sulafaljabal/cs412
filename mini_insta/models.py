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
    profile_image_file = models.ImageField(blank=True) # an actual image

    def __str__(self):
        """returns a string representation of this model instance"""
        return f"{self.username}: {self.display_name}\nJoined: {self.join_date}\nBio: {self.bio_text}\nProfile Pic: {self.profile_image_url}"
    #end

    def get_all_posts(self):
        """returns all of the posts on this profile"""

        posts = Post.objects.filter(profile=self) 
        return posts 
    #enddef

    def get_profile_image(self):
        """ Method to get available profile image: can be either image file or image url if former is not available"""
        if self.profile_image_file:
            return self.profile_image_file.url 
        else:
            return self.profile_image_url
        #endif
    #enddef
    
    def get_followers(self):
        """Method to get all followers tied to an instance of profile"""

        followers_qset = Follow.objects.filter(profile=self) # getting query set of all followers to this instance of profile

        followers_list = []
        for follower in followers_qset:
            followers_list += [follower.follower_profile]
        return followers_list
    #enddef

    def get_num_followers(self):
        """Method to get number of followers an instance of a profile has """
        return len(self.get_followers())
    #enddef

    def get_following(self):
        """ Method to get all accounts this profile instance follows, opposite of
        previous two functions defined above """

        following_qset = Follow.objects.filter(follower_profile=self) # getting query set of all users this instance follows
        following_list = []
        for follower in following_qset:
            following_list += [follower.profile]
        #endfor 
        return following_list
    #enddef

    def get_num_following(self):
        """Method to get the number of accounts this profile instance follows."""
        
        return len(self.get_following())
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
        photos = Photo.objects.filter(post=self).order_by('timestamp')
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
    image_file = models.ImageField(blank=True)

    def __str__(self):
        """ return a string representation of Photo object """
        return f"Photo object tied to Post: {self.post}, uploaded at {self.timestamp}\nImage URL = {self.image_url}\nImage File: {self.image_file}"
    #end def

    def get_image_url(self):
        """ Return photo url: can be either image url or image file"""
        if self.image_file:
            return self.image_file.url 
        else:
            return self.image_url

        #endif 
    #enddef 

#end class Photo

class Follow(models.Model): # class to showcase who follows who
    """Encapsulate the data of a mini_insta follow
    attributes:
    profile (FK): profile object of the person being followed
    follower_profile: profile object of who is following the profile (defined above)
    timestamp: when the follower started following the profile"""

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='profile')#to stop django from complaining
    follower_profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='follower_profile')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return a string representation of who follows who"""
        return f"{self.profile.username} is followed by: {self.follower_profile.username}"