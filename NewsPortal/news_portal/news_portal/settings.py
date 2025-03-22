import os

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-51whj5s@syzg4#l7l-r0_#7d2_(dqeshmzh$386x!l#7=ng$$n'

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

    'django_apscheduler',
]

SITE_ID = 1
SITE_URL = 'http://127.0.0.1:8000'

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
                # 'django.template.context_processors.request',  # Расширение аутентификации и регистрации
                'board_news.context_processors.auth_context',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    # Аутентификация по 'username' из 'django'
    'django.contrib.auth.backends.ModelBackend',
    # Аутентификация по e-mail или сервис-провайдеру из 'allauth'
    'allauth.account.auth_backends.AuthenticationBackend',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


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
EMAIL_HOST = 'smtp.yandex.ru'  # Адрес сервера Яндекс-почты
EMAIL_PORT = 465  # Порт smtp сервера
EMAIL_HOST_USER = ''  # Эл. почта без @yandex.ru
EMAIL_HOST_PASSWORD = ''  # Пароль доступа к API Яндекс-почты
EMAIL_USE_SSL = True  # SSL включен
SERVER_EMAIL = ''  # Эл. почта для массовых рассылок
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER + '@yandex.ru'  # Эл. почта для отправки писем через allauth


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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]


# Настройки форматов даты\времени и времени на выполнение задач модуля apscheduler
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25
