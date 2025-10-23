# file: blog/urls.py
# Sulaf Al Jabal (sulafaj@bu.edu) 09/23/25


from django.urls import path
from django.conf import settings 
from django.contrib.auth import views as auth_views ##new

from.views import *

# URL patterns specific to the quotes app
urlpatterns = [
    path('',RandomArticleView.as_view(), name="random"),
    path('show_all',ShowAllView.as_view(), name="show_all"),
    path('article/<int:pk>', ArticleView.as_view(), name="article"),
    path('article/create', CreateArticleView.as_view(), name="create_article"),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name="create_comment"),
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article"),
    path('comment/<int:pk>/delete', DeleteCommentView.as_view(), name="delete_comment"),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('lougout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'),
]