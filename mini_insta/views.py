# mini_insta/views.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/24/25
# Description: defining views of mini_insta application


from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from .models import * # Profile, Post, Photos
from django.urls import reverse
from .forms import * #CreatePostForm, more incoming
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login
from django.shortcuts import redirect



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

        # print(f"DEBUG: profile = {profile}, profile.pk = {profile.pk}")

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
        #endif 
        return context
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

        return reverse('show_profile', kwargs={'pk': profile.pk})
    #enddef

    def get_object(self):
        """Return profile of logged in user"""
        return self.get_profile()
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
        profile = self.get_profile()

        context['post'] = self.object
        context['profile'] = profile 
        return context 
    #enddef
#end class UpdatePostView

class PostDetailView(DetailView):
    """Shows an instance of a Post tied to a certain Profile object"""

    context_object_name = 'post'
    model = Post 
    template_name = "mini_insta/show_post.html"

    def get_context_data(self, **kwargs):
        """Add is_owner and has_liked to context"""

        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user=self.request.user) # self.get_profile()
            context['is_owner'] = (user_profile == post.profile)
            context['has_liked'] = Like.objects.filter(
                profile=user_profile,
                post=post
            ).exists()
        else:
            context['is_owner'] = False
            context['has_liked'] = False
        
        return context
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

        profile = self.get_profile()
        return profile.get_post_feed()
    #enddef

    def get_context_data(self, **kwargs):
        """get context dictionary for html page
        adding profile object"""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
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
            profile = self.get_profile()
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
        profile = self.get_profile()
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

class LoggedOutView(TemplateView):
    """A view to show confirmation that user has been logged out"""
    template_name = 'mini_insta/logged_out.html'
#endclass

class CreateProfileView(CreateView):
    """View to let user create a profile"""
    model = Profile
    form_class = CreateProfileForm 
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        """add UserCreationForm to context (creating django user)"""
        context = super().get_context_data(**kwargs)

        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context 
    #enddef

    def form_valid(self, form):
        """Create the associated User object before associating it with and saving the Profile object"""

        signup_form = UserCreationForm(self.request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user 
            return super().form_valid(form)
        else:
            return super().form_invalid(form) # failed
        #endif
    #enddef

    def get_success_url(self):

        profile = self.get_profile()

        return reverse('show_profile', kwargs={'pk': profile.pk})
    #enddef
#endclass

class FollowProfileView(ProfileRequiredMixin, TemplateView):
    """View to follow a profile."""
    template_name = 'mini_insta/show_profile.html'

    def dispatch(self, request, *args, **kwargs):
        """Handle following the profile before rendering the template."""
        
        user_profile = self.get_profile()
        profile_to_follow = Profile.objects.get(pk=kwargs['pk'])
        
        if user_profile != profile_to_follow:
            existing_follow = Follow.objects.filter(
                follower_profile=user_profile,
                profile=profile_to_follow
            ).first()
            
            if not existing_follow:
                Follow.objects.create(
                    follower_profile=user_profile,
                    profile=profile_to_follow
                )
        return redirect('show_profile', pk=profile_to_follow.pk)
    #enddef
#endclass

class DeleteFollowView(ProfileRequiredMixin, TemplateView):
    """View to unfollow a profile."""
    template_name = 'mini_insta/show_profile.html'

    def dispatch(self, request, *args, **kwargs):
        """Handle unfollowing the profile before rendering the template."""
        
        user_profile = self.get_profile()
        profile_to_unfollow = Profile.objects.get(pk=kwargs['pk'])
        
        Follow.objects.filter(
            follower_profile=user_profile,
            profile=profile_to_unfollow
        ).delete() # deleting follow
        
        return redirect('show_profile', pk=profile_to_unfollow.pk)
    #enddef
#endclass

class LikePostView(ProfileRequiredMixin, TemplateView):
    """View to like a post."""
    template_name = 'mini_insta/show_post.html'

    def dispatch(self, request, *args, **kwargs):
        """Handle liking the post before rendering the template."""
        
        user_profile = self.get_profile()
        post_to_like = Post.objects.get(pk=kwargs['pk'])
        
        if user_profile != post_to_like.profile:
            existing_like = Like.objects.filter(
                profile=user_profile,
                post=post_to_like
            ).first()
            
            if not existing_like:
                Like.objects.create(
                    profile=user_profile,
                    post=post_to_like
                )
        return redirect('show_post', pk=post_to_like.pk)
    #enddef
#endclass

class DeleteLikeView(ProfileRequiredMixin, TemplateView):
    """View to unlike a post."""
    template_name = 'mini_insta/show_post.html'

    def dispatch(self, request, *args, **kwargs):
        """Handle unliking the post before rendering the template."""
        
        user_profile = self.get_profile()
        post_to_unlike = Post.objects.get(pk=kwargs['pk'])
        
        Like.objects.filter(
            profile=user_profile,
            post=post_to_unlike
        ).delete() # removing like
        
        return redirect('show_post', pk=post_to_unlike.pk)
    #enddef
#end class