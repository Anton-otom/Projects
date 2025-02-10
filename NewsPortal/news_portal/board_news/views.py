from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post


class NewList(ListView):
    model = Post
    ordering = '-date_time_in'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'new'
