from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .filters import PostFilter
from .models import Post
from .forms import PostForm


# Представление для ленты постов
class PostList(ListView):
    model = Post
    ordering = '-date_time_in'
    template_name = 'flatpages/posts.html'
    context_object_name = 'posts'
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
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


# Представление для создания новости
class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/news_create.html'

    # Установить тип поста "новость" и определить автора
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author_post_id = 1
        post.type_post = 'nw'
        post.save()
        return super().form_valid(form)


# Представление для изменения новости
class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/news_update.html'


# Представление для удаления новости
class NewsDelete(DeleteView):
    model = Post
    template_name = 'flatpages/news_delete.html'
    success_url = reverse_lazy('post_list')


# Представление для создания статьи
class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/article_create.html'
    Post.type_post.choices = 'ar'

    # Установить тип поста "статья" и определить автора
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author_post_id = 2
        post.type_post = 'ar'
        post.save()
        return super().form_valid(form)


# Представление для изменения статьи
class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/article_update.html'


# Представление для удаления статьи
class ArticleDelete(DeleteView):
    model = Post
    template_name = 'flatpages/article_delete.html'
    success_url = reverse_lazy('post_list')
