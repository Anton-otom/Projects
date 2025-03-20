from django.contrib.auth.models import User, Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from board_news.models import Author


@receiver(m2m_changed, sender=User.groups.through)
def create_or_delete_author(sender, instance, action, pk_set, **kwargs):
    if isinstance(instance, User):
        group_names = []
        for pk in pk_set:
            group = Group.objects.filter(id=pk).first()
            if group:
                group_names.append(group.name)
        check_on_author = Author.objects.filter(user=instance).exists()
        if action == 'post_add':
            if 'author' in group_names and not check_on_author:
                Author.objects.create(user=instance)
        if action == 'post_remove':
            if 'author' in group_names and check_on_author:
                instance.author.delete()