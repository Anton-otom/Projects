from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from news_portal.settings import SITE_URL

from .models import Post

# Переменная для хранения "id" новых постов
new_posts = set()


# Сигнал, добавляющий "id" новых постов в "new_posts"
@receiver(post_save, sender=Post)
def new_post(sender, instance, created, **kwargs):
    if created:
        new_posts.add(instance.id)


# Сигнал, отправляющий письма подписчикам категорий постов на их email
@receiver(m2m_changed, sender=Post.categories.through)
def send_mail_on_post_create(sender, instance, action, **kwargs):
    # Проверить, что связь добавляется в только что созданный пост
    if action == "post_add" and instance.id in new_posts:
        new_posts.discard(instance.id)

        # Получить "username" и "email" подписчиков всех категорий поста
        post_categories = instance.categories.all()
        unique_subscribers = {}
        for category in post_categories:
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                if subscriber.email and subscriber.username not in unique_subscribers:
                    unique_subscribers[subscriber.username] = subscriber.email

        # Отправить письмо каждому подписчику
        for key_username, value_email in unique_subscribers.items():
            html_content = render_to_string(
                'flatpages/message_about_new_post.html',
                {
                    'post': instance,
                    'site_url': SITE_URL,
                    'username': key_username,
                }
            )

            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=instance.text,
                from_email='anthon.sev@yandex.ru',
                to=[value_email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()