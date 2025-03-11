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
    'board_news',  # Вывод постов и операции с ними
    'allauth',  # Расширение аутентификации и регистрации
    'allauth.account',  # Расширение аутентификации и регистрации
    'allauth.socialaccount',  # Расширение аутентификации и регистрации
    'allauth.socialaccount.providers.yandex',  # Аутентификация и регистрация через Яндекс
    'sign',  # Приложение для кастомизации 'allauth'
]

SITE_ID = 1

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
                'django.template.context_processors.request',  # Расширение аутентификации и регистрации
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

ACCOUNT_EMAIL_REQUIRED = True  # При регистрации обязательно вводить e-mail
ACCOUNT_UNIQUE_EMAIL = True  # E-mail должен быть уникальным
ACCOUNT_USERNAME_REQUIRED = True  # При регистрации обязательно вводить username
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # Аутентификация проводится по username
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Верификация e-mail отсутствует

LOGIN_URL = 'account_login'  # Адрес авторизации

LOGIN_REDIRECT_URL = 'post_list'  # Адрес после успешной авторизации

LOGOUT_REDIRECT_URL = 'post_list'  # Адрес после выходы из системы

ACCOUNT_FORMS = {
    'login': 'sign.forms.CustomLoginForm',  # Переопределение формы входа в систему
    'signup': 'sign.forms.CustomSignupForm'  # Переопределение формы регистрации
}

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
