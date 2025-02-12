from django.views.generic import (
    ListView, DetailView, CreateView)

from .models import Post
from .forms import PostForm


# Представление для ленты постов
class PostList(ListView):
    model = Post
    ordering = '-date_time_in'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'


# Представление для отдельного поста
class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'new'


# Представление для создания поста
class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'
