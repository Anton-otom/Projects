from django.urls import path
from .views import (
    PostList, PostDetail, PostCreate
)


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),  # Адрес страницы со всеми постами
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),  # Адрес страницы с отдельной новостью
    path('create/', PostCreate.as_view(), name='post_create'),  # Адрес страницы добавления нового поста
]