from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post


class NewList(ListView):
    model = Post
    ordering = '-date_time_in'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'


class NewDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'new'
