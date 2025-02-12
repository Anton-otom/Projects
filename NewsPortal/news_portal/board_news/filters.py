from django.forms import DateTimeInput
from django_filters import FilterSet, CharFilter, IsoDateTimeFilter
from .models import Post


# Фильтры для поиска в списке постов
class PostFilter(FilterSet):
    title__icontains = CharFilter(
        field_name='title',
        label='Название поста содержит:',
        lookup_expr='icontains'
    )
    author_post__icontains = CharFilter(
        field_name='author_post__user__username',
        label='Имя автора поста содержит:',
        lookup_expr='icontains'
    )
    date_time_in__gt = IsoDateTimeFilter(
        field_name='date_time_in',
        label='Пост опубликован после:',
        lookup_expr='gt',
        widget=DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Post
        fields = []
