from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)

from .utils import can_user_add_post
from .filters import PostFilter
from .models import Post, Category, Author
from .forms import PostForm


# Представление для дополнения страниц авторизованных пользователей
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/default_auth.html'


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

    # Обновить контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Отфильтровать посты
        context['filterset'] = self.filterset
        # True, если применён хотя бы один фильтр
        # Для отображения кнопки "Сбросить фильтры"
        context['has_filters'] = any(self.request.GET.values())
        # Передать информацию, есть ли подписчики у выбранных для фильтрации категорий
        selected_categories = self.filterset.form.cleaned_data.get('categories__in', [])
        if selected_categories:
            categories_with_subscription_status = []
            for category in selected_categories:
                is_subscribed = category.subscribers.filter(id=self.request.user.id).exists()
                categories_with_subscription_status.append({
                    'category': category,
                    'is_subscribed': is_subscribed,
                })
            context['categories_with_subscription_status'] = categories_with_subscription_status
        else:
            context['categories_with_subscription_status'] = []

        return context


# Представление для отдельного поста
class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


# Представление для создания новости
class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'board_news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'flatpages/news_create.html'

    def dispatch(self, request, *args, **kwargs):
        if not can_user_add_post(request.user):
            return redirect(reverse('news_limit_reacher'))
        return super().dispatch(request, *args, **kwargs)

    # Установить тип поста "новость" и определить автора
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author_post = Author.objects.get(user_id=self.request.user.id)
        post.type_post = 'nw'
        post.save()
        form.save_m2m()
        return super().form_valid(form)


# Представление для изменения новости
class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'board_news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'flatpages/news_update.html'


# Представление для удаления новости
class NewsDelete(DeleteView):
    model = Post
    template_name = 'flatpages/news_delete.html'
    success_url = reverse_lazy('post_list')


# Представление для создания статьи
class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'board_news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'flatpages/article_create.html'
    Post.type_post.choices = 'ar'

    # Установить тип поста "статья" и определить автора
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author_post = Author.objects.get(user_id=self.request.user.id)
        post.type_post = 'ar'
        post.save()
        form.save_m2m()
        return super().form_valid(form)


# Представление для изменения статьи
class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'board_news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'flatpages/article_update.html'


# Представление для удаления статьи
class ArticleDelete(DeleteView):
    model = Post
    template_name = 'flatpages/article_delete.html'
    success_url = reverse_lazy('post_list')


# Представление для подписки на категорию
@login_required
def subscribe_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.subscribers.add(request.user)
    params = request.GET.copy()
    redirect_url = reverse('post_search') + '?' + params.urlencode()
    return redirect(redirect_url)


# Представление для отписки с категории
@login_required
def unsubscribe_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.subscribers.remove(request.user)
    params = request.GET.copy()
    redirect_url = reverse('post_search') + '?' + params.urlencode()
    return redirect(redirect_url)


# Представление для информирования о превышении лимита добавления новостей в день
def news_limit_reached(request):
    return render(request, 'flatpages/news_limit_reached.html')

