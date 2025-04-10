import os

from dotenv import load_dotenv
from pathlib import Path

from news_portal.logging.formaters import CustomConsoleFormatter

BASE_DIR = Path(__file__).resolve().parent.parent


# Загрузка переменных из .env
dotenv_path = BASE_DIR / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)


SECRET_KEY = 'django-insecure-51whj5s@syzg4#l7l-r0_#7d2_(dqeshmzh$386x!l#7=ng$$n'

# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.flatpages',
    'fpages',  # Расширение админ-панели
    'django_filters',  # Кастомные фильтры

    'board_news.apps.BoardNewsConfig',  # Вывод постов и операции с ними

    'allauth',  # Расширение аутентификации и регистрации
    'allauth.account',  # Расширение аутентификации и регистрации
    'allauth.socialaccount',  # Расширение аутентификации и регистрации
    'allauth.socialaccount.providers.yandex',  # Аутентификация и регистрация через Яндекс
    'sign.apps.SignConfig',  # Приложение для кастомизации 'allauth'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'news_portal.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'board_news.context_processors.auth_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'news_portal.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SITE_ID = 1
SITE_URL = 'http://127.0.0.1:8000'


# Настройки django-allauth
AUTHENTICATION_BACKENDS = [
    # Аутентификация по 'username' из 'django'
    'django.contrib.auth.backends.ModelBackend',
    # Аутентификация по e-mail или сервис-провайдеру из 'allauth'
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_EMAIL_REQUIRED = True  # При регистрации обязательно вводить e-mail
ACCOUNT_UNIQUE_EMAIL = True  # E-mail должен быть уникальным
ACCOUNT_USERNAME_REQUIRED = True  # При регистрации обязательно вводить username
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # Аутентификация проводится по username или e-mail
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # Верификация e-mail необязательна
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Верификация e-mail обязательна
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''  # Убрать префикс "[sitename]" в теме письма подтверждения регистрации
LOGIN_URL = 'account_login'  # Адрес авторизации
LOGIN_REDIRECT_URL = 'post_list'  # Адрес после успешной авторизации
LOGOUT_REDIRECT_URL = 'post_list'  # Адрес после выходы из системы
ACCOUNT_FORMS = {
    'login': 'sign.forms.CustomLoginForm',  # Переопределение формы входа в систему
    'signup': 'sign.forms.CustomSignupForm'  # Переопределение формы регистрации
}


# Настройки эл. почты приложения
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'  # Адрес сервера Яндекс-почты
EMAIL_PORT = 465  # Порт smtp сервера
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Эл. почта без @yandex.ru
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Пароль доступа к API Яндекс-почты
EMAIL_USE_SSL = True  # SSL включен
SERVER_EMAIL = os.getenv('SERVER_EMAIL')  # Эл. почта для массовых рассылок
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER + '@yandex.ru'  # Эл. почта для отправки писем через allauth
ADMINS = [('Anton', 'an.vaseko@mal.ru')]


# Настройки кэширования
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}


# Настройки celery
CELERY_BROKER_URL = 'redis://localhost:6379'  # URL брокера сообщений
CELERY_RESULT_BACKEND = 'redis://localhost:6379'  # Хранилище результатов выполнения задач
CELERY_ACCEPT_CONTENT = ['application/json']  # Допустимый формат данных
CELERY_TASK_SERIALIZER = 'json'  # Метод сериализации задач
CELERY_RESULT_SERIALIZER = 'json'  # Метод сериализации результатов


# Настройки логирования
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'style': '{',
#     'formatters': {
#         'custom_console_formatter': {
#             '()': CustomConsoleFormatter,
#         },
#         'file_general_security_formatter': {
#             'format': '{asctime} {levelname} {module} {message}',
#             'style': '{'
#         },
#         'file_errors_formatter': {
#             'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
#             'style': '{'
#         },
#         'email_formatter': {
#             'format': '{asctime} {levelname} {message} {pathname}',
#             'style': '{'
#         },
#     },
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'custom_console_formatter'
#         },
#         'file_general': {
#             'level': 'INFO',
#             'filters': ['require_debug_false'],
#             'class': 'logging.FileHandler',
#             'filename': 'news_portal/logging/general.log',
#             'formatter': 'file_general_security_formatter'
#         },
#         'file_errors': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': 'news_portal/logging/errors.log',
#             'formatter': 'file_errors_formatter'
#         },
#         'file_security': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'news_portal/logging/security.log',
#             'formatter': 'file_general_security_formatter'
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler',
#             'formatter': 'email_formatter'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'file_general'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['file_errors', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.server': {
#             'handlers': ['file_errors', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.template': {
#             'handlers': ['file_errors',],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.db.backends': {
#             'handlers': ['file_errors',],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.security': {
#             'handlers': ['file_security'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#     }
# }
