from django.urls import path
from .views import NewList, NewDetail


urlpatterns = [
    path('', NewList.as_view()),  # Адрес страницы со всеми новостями
    path('<int:pk>', NewDetail.as_view()),  # Адрес страницы с отдельной новостью
]