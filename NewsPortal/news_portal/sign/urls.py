from django.urls import path
from .views import upgrade_me

urlpatterns = [
    path('upgrade/', upgrade_me, name='upgrade')  # Добавить пользователя в группу "author"
]