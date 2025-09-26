from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random 

# Create your views here.

class ShowAllView(ListView):
    """Define a veiw class to show all blog Articles"""

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"


class ArticleView(DetailView):
    """DIsplays a single article"""

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"
#end class

class RandomArticleView(DetailView):
    """Displays a single random article"""

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    def get_object(self):
        """return one instance of the Article object selected
        at random. Overiding a function"""

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
    #end get_object
#endclass
