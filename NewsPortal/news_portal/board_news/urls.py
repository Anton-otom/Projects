from django.urls import path
from .views import (
    PostList, PostDetail, PostSearch,
    NewsCreate, NewsUpdate, NewsDelete,
    ArticleCreate, ArticleUpdate, ArticleDelete,
)


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),  # Адрес страницы со всеми постами
    path('search/', PostSearch.as_view(), name='post_search'),  # Адрес страницы для поиска по всем постам
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),  # Адрес страницы просмотра поста
    path('news/create/', NewsCreate.as_view(), name='news_create'),  # Адрес страницы добавления новости
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),  # Адрес страницы изменения новости
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),  # Адрес страницы удаления новости
    path('article/create/', ArticleCreate.as_view(), name='article_create'),  # Адрес страницы добавления статьи
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),  # Адрес страницы изменения статьи
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),  # Адрес страницы удаления статьи
]
