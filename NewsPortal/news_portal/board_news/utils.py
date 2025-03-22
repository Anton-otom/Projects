from datetime import date

from django.contrib.auth.models import AnonymousUser

from .models import Post


# Функция, принимающая True, если пользователь создал меньше 4-х постов в день
def can_user_add_post(user):
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return False

    today = date.today()
    posts_count = Post.objects.filter(
        author_post__user=user,
        type_post='nw',
        date_time_in__date=today
    ).count()
    return posts_count < 4
