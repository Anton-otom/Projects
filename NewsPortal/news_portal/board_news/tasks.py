from datetime import timedelta

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from news_portal.settings import DEFAULT_FROM_EMAIL, SITE_URL
from .models import Post, Category


# Отправить письма подписчикам после публикации нового поста
@shared_task
def send_email_on_post_create(post_id):
    # Получить "username" и "email" подписчиков всех категорий поста
    post = Post.objects.get(id=post_id)
    categories = post.categories.all()

    unique_subscribers = {}
    for category in categories:
        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            if subscriber.email and subscriber.username not in unique_subscribers:
                unique_subscribers[subscriber.username] = subscriber.email

    # Отправить письмо каждому подписчику
    for key_username, value_email in unique_subscribers.items():
        html_content = render_to_string(
            'flatpages/message_about_new_post.html',
            {
                'post': post,
                'username': key_username,
                'site_url': SITE_URL,
            }
        )

        msg = EmailMultiAlternatives(
            subject=post.title,
            body=post.text,
            from_email=DEFAULT_FROM_EMAIL,
            to=[value_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


# Отправить подписчикам письмо с постами за прошедшую неделю
@shared_task
def send_emails_every_week():
    # Получить посты за неделю
    week_ago = timezone.now() - timedelta(days=7)
    new_posts = Post.objects.filter(date_time_in__gte=week_ago)

    # Отфильтровать по категориям и сделать рассылку
    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        if not subscribers:
            continue

        posts_in_category = new_posts.filter(categories=category)
        if not posts_in_category:
            continue

        for user in subscribers:
            html_content = render_to_string(
                'flatpages/weekly_newsletter_to_subscribers.html',
                {
                    'category': category,
                    'posts': posts_in_category,
                    'site_url': SITE_URL,
                    'username': user.username,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Еженедельная рассылка в категории {category.category_name}',
                body='',
                from_email=DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
