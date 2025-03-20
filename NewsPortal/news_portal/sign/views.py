from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect


# Представление для добавления пользователя в группу "author"
@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not user.groups.filter(name='author').exists():
        user.groups.add(author_group)
    return redirect('post_list')
