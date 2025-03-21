from django.apps import AppConfig


class BoardNewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'board_news'

    # Подключить сигналы
    def ready(self):
        from . import signals
