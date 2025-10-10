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

    def get_success_url(self):
        """Return the URL which we redirect the browser to after successfully
        deleting a Post """

        pk = self.kwargs.get("pk")
        post = Post.objects.get(pk=pk) # getting post

        profile = post.Profile # getting profile via post field
        
        # redirect user to the profile of the user after the post has been deleted
        return reverse('profile', kwargs={'pk': profile.pk})
    #enddef

    def form_valid(self):
        """This method handles form submission and deletes the Post object from the Django database
        """

        pk = self.kwargs['pk'] #primary key of the post object
        profile = Profile.objects.get(pk=pk) # getting profile connected to post needing to be deleted

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
#end class UpdatePostView