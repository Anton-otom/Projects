from django.urls import path
from .views import (
    PostList, PostDetail, PostCreate, PostSearch
)


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),  # Адрес страницы со всеми постами
    path('search/', PostSearch.as_view(), name='post_search'),  # Адрес страницы для поиска по всем постам
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),  # Адрес страницы с отдельной новостью
    path('create/', PostCreate.as_view(), name='post_create'),  # Адрес страницы добавления нового поста
]