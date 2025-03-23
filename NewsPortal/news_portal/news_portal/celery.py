import os

from celery import Celery


# Cвязать настройки Django с настройками Celery через переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')


# Создать экземпляр приложения Celery
app = Celery('news_portal')
# Установить файл конфигурации для "app", указать пространство имен
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически искать задания в файлах tasks.py каждого приложения проекта
app.autodiscover_tasks()
