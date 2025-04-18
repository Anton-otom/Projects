from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('posts/', include('board_news.urls')),
    path('accounts/', include('allauth.urls')),
    path('sign/', include('sign.urls')),
]
