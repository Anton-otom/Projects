from django.views.generic import (
    ListView, DetailView, CreateView)

from .filters import PostFilter
from .models import Post
from .forms import PostForm


# Представление для ленты постов
class PostList(ListView):
    model = Post
    ordering = '-date_time_in'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 10


# Представление для поиска по фильтрам в списке постов
class PostSearch(PostList):
    template_name = 'flatpages/posts_search.html'

    # Применить фильтр "PostFilter" к списку постов
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    # Добавить в контекст отфильтрованные посты
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


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
