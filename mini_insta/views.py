# mini_insta/views.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/24/25
# Description: defining views of mini_insta application


from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import * # Profile, Post, Photos
from django.urls import reverse
from .forms import * #CreatePostForm, more incoming


# Create your views here.

class ShowAllView(ListView):
    """Define a veiw class to show all profile Profiles"""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

#endclass


class ProfileView(DetailView):
    """Displays a single Profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"
#end class

class CreatePostView(CreateView):
    """A view to handle creation of a new Post on a certain Profile"""

    form_class = CreatePostForm
    model = Post
    template_name = "mini_insta/create_post_form.html"
    
    def form_valid(self, form):
        """This method handles form submission and saves the new object to the Django database
        Need to add foreign key (of Profile) to the Post object before saving it to db"""

        print(f"CreatePostView.form_valid: form.cleaned_data={form.cleaned_data}")

        # get PK from URL pattern 
        pk = self.kwargs['pk'] 
        profile = Profile.objects.get(pk=pk)

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

        pk = self.kwargs['pk']

        return reverse('show_profile', kwargs={'pk': pk})
    #enddef

    def get_context_data(self):
        """return the dictionary of context variables for use in the template"""

        # Calling the superclass method 
        context = super().get_context_data()

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile 
        return context 
    #enddef
#end class

class DeletePostView(DeleteView):
    """This method lets users delete instances of Post objects, automatically deletes instances of Photos
    connected to those Posts as well."""

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

        profile = self.object.profile # getting profile via post field
        
        # redirect user to the profile of the user after the post has been deleted
        return reverse('show_profile', kwargs={'pk': profile.pk})
    #enddef
#end class DeletePost View

class UpdateProfileView(UpdateView):
    """Updates instance of Profile object"""
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

        pk = self.kwargs['pk']

        return reverse('show_profile', kwargs={'pk': pk})
    #enddef
#end class UpdateProfile


class UpdatePostView(UpdateView):
    """Updates instance of Post object"""
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