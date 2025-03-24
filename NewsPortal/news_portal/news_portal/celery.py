import os

from celery import Celery
from celery.schedules import crontab


# Cвязать настройки Django с настройками Celery через переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')


# Создать экземпляр приложения Celery
app = Celery('news_portal')
# Установить файл конфигурации для "app", указать пространство имен
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически искать задания в файлах tasks.py каждого приложения проекта
app.autodiscover_tasks()


# Словарь с периодическими задачами
app.conf.beat_schedule = {
    'send_emails_subscribers_every_monday': {
        'task': 'board_news.tasks.send_emails_every_week',
        'schedule': crontab(hour='8', minute='0', day_of_week='monday'),
        'args': (),
    }
}
