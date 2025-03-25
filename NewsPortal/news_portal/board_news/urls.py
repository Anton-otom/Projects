from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    PostList, PostDetail, PostSearch,
    NewsCreate, NewsUpdate, NewsDelete,
    ArticleCreate, ArticleUpdate, ArticleDelete,
    subscribe_category, unsubscribe_category, news_limit_reached,
)


urlpatterns = [
    # Адрес страницы со всеми постами
    path('',
         cache_page(60)(PostList.as_view()),
         name='post_list'),
    # Адрес страницы для поиска по всем постам
    path('search/',
         PostSearch.as_view(),
         name='post_search'),
    # Адрес страницы просмотра поста
    path('<int:pk>',
         PostDetail.as_view(),
         name='post_detail'),
    # Адрес страницы добавления новости
    path('news/create/',
         NewsCreate.as_view(),
         name='news_create'),
    # Адрес страницы изменения новости
    path('news/<int:pk>/update/',
         NewsUpdate.as_view(),
         name='news_update'),
    # Адрес страницы удаления новости
    path('news/<int:pk>/delete/',
         NewsDelete.as_view(),
         name='news_delete'),
    # Адрес страницы с сообщением о превышении лимита публикаций
    path('news/limit_reached/',
         news_limit_reached,
         name='news_limit_reacher'),
    # Адрес страницы добавления статьи
    path('article/create/',
         ArticleCreate.as_view(),
         name='article_create'),
    # Адрес страницы изменения статьи
    path('article/<int:pk>/update/',
         ArticleUpdate.as_view(),
         name='article_update'),
    # Адрес страницы удаления статьи
    path('article/<int:pk>/delete/',
         ArticleDelete.as_view(),
         name='article_delete'),
    # Адрес страницы подписки на категорию
    path('subscribe_category/<int:category_id>/',
         subscribe_category,
         name='subscribe_category'),
    # Адрес страницы отписки с категории
    path('unsubscribe_category/<int:category_id>/',
         unsubscribe_category,
         name='unsubscribe_category'),
]
