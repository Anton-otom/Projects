from django.contrib.auth.models import Group


# В контекст всех представлений добавить поле с проверкой у пользователя принадлежности к группе "author"
def auth_context(request):
    if request.user.is_authenticated:
        return {'is_not_author': not request.user.groups.filter(name='author').exists()}
    return {}
