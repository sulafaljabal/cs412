# mini_insta/views.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/24/25
# Description: defining views of mini_insta application


from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import * # Profile, Post, Photos
from django.urls import reverse
from .forms import * #CreatePostForm, more incoming
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileRequiredMixin(LoginRequiredMixin):
    """Profile subclass of LoginRequiredMixin"""

    def get_profile(self):
        """Get Profile object associated with user to grant them access to profile-related views"""
        return self.request.user.profile 
    #enddef

    def get_login_url(self):
        """Get login url for user to login"""
        return reverse('login')
    #enddef

#endclass

# Create your views here.

class ShowAllView(ListView):
    """Define a veiw class to show all profile Profiles"""
    # this does not require authentication

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

#endclass


class ProfileView(DetailView):
    """Displays a single Profile.
    Requires logic that to figure out if a user is viewing their own profile or if they are
    viewing another profile (also have to figure out if both profiles follow each other or not)"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        """returning profile context data needed for a user to view their own profile"""
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        print(f"DEBUG: profile = {profile}, profile.pk = {profile.pk}")
        if self.request.user.is_authenticated: # if user is logged in
            user_profile = Profile.objects.get(user=self.request.user) # getting profile tied to a certain user instance
            context['user_is_owner'] = (user_profile == profile) # if this is true then user is viewing their own profile 
            context['user_is_following'] = Follow.objects.filter(
                follower_profile = user_profile, # user
                profile = profile # person being followed
            ).exists() # if this is false, then the user does not follow the profile they are viewing
            # if this is true then the user DOES follow the profile they are viewing
            # this is necessary in case the user wants to unfollow the profile
        else: # if the user IS NOT authenticated 
            context['user_is_owner'] = False # user is not logged in
            context['user_is_following'] = False # user is not logged in, therefore can't follow the profile they're currently viewing
#end class

class CreatePostView(ProfileRequiredMixin, CreateView):
    """A view to handle creation of a new Post on a certain Profile
    This requires authentication"""

    form_class = CreatePostForm
    model = Post
    template_name = "mini_insta/create_post_form.html"
    
    def form_valid(self, form):
        """This method handles form submission and saves the new object to the Django database
        Need to add foreign key (of Profile) to the Post object before saving it to db"""

        print(f"CreatePostView.form_valid: form.cleaned_data={form.cleaned_data}")

        profile = self.get_profile()

        #attach this profile to the post 
        form.instance.profile = profile
        response = super().form_valid(form)

        # need to create new instance of Photo
        #print(f"Profile: {profile}")
        #print(f"Post: {self}")

        if self.request.FILES:
            files = self.request.FILES.getlist('image_file')
            photo_list = []
            for file in files:
                photo = Photo(post=self.object, image_file = file)
                photo.save()
                photo_list.append(photo)
            #endfor
            print(f"photos: {photo_list}")
        #endif

        return response
    #enddef form_valid

    def get_success_url(self) -> str:
        """Return the URL to redirect to after creating a new Post."""

        profile = self.get_profile()

        return reverse('show_profile', kwargs={'pk': profile.pk})
    #enddef

    def get_context_data(self):
        """return the dictionary of context variables for use in the template"""

        # Calling the superclass method 
        context = super().get_context_data()

        profile = self.get_profile()

        context['profile'] = profile 
        return context 
    #enddef
#end class

class DeletePostView(ProfileRequiredMixin, DeleteView):
    """This method lets users delete instances of Post objects, automatically deletes instances of Photos
    connected to those Posts as well. This requires authentication"""

    template_name = "mini_insta/delete_post_form.html"
    model = Post 
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """Adding post to template context"""
        
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        context['post'] = self.object

        return context
    #enddef

    def get_success_url(self):
        """Return the URL which we redirect the browser to after successfully
        deleting a Post """

        profile = self.get_profile() # getting profile via post field
        
        # redirect user to the profile of the user after the post has been deleted
        return reverse('show_profile', kwargs={'pk': profile.pk})
    #enddef
#end class DeletePost View

class UpdateProfileView(ProfileRequiredMixin, UpdateView):
    """Updates instance of Profile object.
    This requires authentication """
    model = Profile 
    form_class = UpdateProfileForm 
    template_name = "mini_insta/update_profile_form.html"

    def form_valid(self, form):
        """Handle the form submission to update a Profile object"""
        print(f"UpdateProfileView: form.cleaned_data={form.cleaned_data}")

        return super().form_valid(form)
    #enddef

    def get_success_url(self) -> str:
        """Return the URL to redirect to after successfully updating a Profile."""

        profile = self.get_profile()

        return reverse('show_profile', kwargs={'pk': self.pk})
    #enddef
#end class UpdateProfile


class UpdatePostView(ProfileRequiredMixin, UpdateView):
    """Updates instance of Post object
    This requires authentication"""
    model = Post 
    form_class = UpdatePostForm 
    template_name = "mini_insta/update_post_form.html"    
    #context_object_name = 'post'


    def form_valid(self, form):
        """Handle the form submission to update a Post object"""
        print(f"UpdatePostView: form.cleaned_data={form.cleaned_data}")

        return super().form_valid(form)
    #enddef

    def get_success_url(self) -> str:
        """Return the URL to redirect to after successfully updating a Profile."""

    
        return reverse('show_post', kwargs={'pk': self.object.pk})
    #enddef
    def get_context_data(self, **kwargs):
        """return the dictionary of context variables for use in the template"""

        # Calling the superclass method 
        context = super().get_context_data(**kwargs)

        # pk = self.kwargs['pk']
        profile = self.object.profile

        context['profile'] = profile 
        return context 
    #enddef
#end class UpdatePostView

class PostDetailView(DetailView):
    """Shows an instance of a Post tied to a certain Profile object"""

    context_object_name = 'post'
    model = Post 
    template_name = "mini_insta/show_post.html"

#endclass

class ShowFollowersDetailView(DetailView):
    """Detail view of followers tied to a certain profile instance"""
    model = Profile 
    context_object_name = 'profile'
    template_name = "mini_insta/show_followers.html"
#endclass

class ShowFollowingDetailView(DetailView):
    """Detail view of who a profile instance follows"""
    model = Profile 
    context_object_name = 'profile'
    template_name = "mini_insta/show_following.html"
#endclass

class PostFeedListView(ProfileRequiredMixin, ListView):
    """List view of a profile's feed (based off of who they're following)
    Requires authentication """
    model = Post  # former profile... html code wouldn't run when this was the case
    context_object_name = 'post'
    template_name = 'mini_insta/show_feed.html'

    def get_feed_list(self):
        """return post feed for profile"""
        profile_pk = self.kwargs.get('pk')
        profile = Profile.objects.get(pk=profile_pk)
        return profile.get_post_feed()
    #enddef

    def get_context_data(self, **kwargs):
        """get context dictionary for html page
        adding profile object"""
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs.get('pk')
        context['profile'] = Profile.objects.get(pk=profile_pk)
        return context
    #enddef
#endclass

class SearchView(ProfileRequiredMixin, ListView):
    """Class to search up Profiles and Posts based off text
    Search done through Profile 
    This requires authentication """

    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        """overriding dispatch method, checking if query is present"""

        if 'query' not in self.request.GET: # show search.html template if query is not present 
            profile_pk = self.kwargs.get('pk')
            profile = Profile.objects.get(pk=profile_pk)
            template = 'mini_insta/search.html'
            return render(request, template, {'profile': profile})
        else: # if query IS PRESENT
            return super().dispatch(request, *args, **kwargs)
        #endif 
    #enddef

    def get_context_data(self, **kwargs):
        """returning context dictionary for template. Adding profile, query, posts and profiles
        to the dictionary """

        context = super().get_context_data(**kwargs)

        # grabbing query 
        query = self.request.GET.get('query', '') # null val incase its empty
        context['query'] = query 

        # profile logic
        profile_pk = self.kwargs.get('pk')
        profile = Profile.objects.get(pk=profile_pk)
        context['profile'] = profile 

        # getting posts 
        context['posts'] = self.get_queryset()

        # matching profiles
        if query:
            username_result = Profile.objects.filter(username__icontains=query)
            display_name_result = Profile.objects.filter(display_name__icontains=query)
            bio_result = Profile.objects.filter(bio_text__icontains=query)

            all_profiles = (username_result | display_name_result | bio_result)
            all_profiles.distinct()
            context['profiles'] = all_profiles 
        else:
            context['profiles'] = Profile.objects.none()
        #endif

        return context 
    #enddef


    def get_queryset(self):
        """ return posts that match our search query """
        query = self.request.GET.get('query', '')
        if query:
            return Post.objects.filter(caption__icontains=query).order_by('timestamp')
            # filtering posts by timestamp
        #endif
        return Post.objects.none()
    #enddef
#endclass