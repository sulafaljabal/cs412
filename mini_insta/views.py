# mini_insta/views.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/24/25
# Description: defining views of mini_insta application


from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
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
        

        # need to create new instance of Photo
        print(f"Profile: {profile}")
        print(f"Post: {self}")

        image_URL = self.request.POST.get('image_url') # just in case theres no photo
        if not image_URL:
            image_URL = 'No image available...'
        #endif

        photo = Photo(post_id=self.object.pk, image_url=image_URL) # creating new instance of Photo
        photo.save()
        print(f"Photo: {photo}") # debugging

        return super().form_valid(form)
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