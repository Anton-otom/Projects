from datetime import timedelta

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution

from board_news.models import Post, Category
from news_portal.settings import SITE_URL, DEFAULT_FROM_EMAIL


# Функция еженедельной рассылки подписчикам
def my_job():
    print("Начать отправку")
    # Получить почты за неделю
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
    print("Отправка закончена")


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)