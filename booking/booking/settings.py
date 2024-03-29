"""
Django settings for booking project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# from configparser import ConfigParser
# local_config_path = os.path.join(BASE_DIR, 'conf', 'local.conf')
# config = ConfigParser()
# config.read(local_config_path)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')_11wg%dx1xri492p$vle(fw*qcila1%$42rgy8owo^z%dm6_i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp.apps.MainappConfig',
    'authapp.apps.AuthappConfig',
    'adminapp.apps.AdminappConfig',
    'constructor_app.apps.ConstructorAppConfig',
    # 'django.contrib.sites',  # added for allauth
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    'supportapp'
]


"""
[Unit]
Description=gunicorn daemon
Requires=diplom.socket
After=network.target


[Service]
User=root
Group=www-data
WorkingDirectory=/home/projects/prj/booking
ExecStart=/home/projects/prj/booking/django2/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/home/projects/prj/booking/diplom.sock \
    booking.wsgi:application

[Install]
WantedBy=multi-user.target

___________
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/home/projects/prj/booking/diplom.sock

[Install]
WantedBy=sockets.target

"""

"""
server {
    listen 80;
    server_name 89.108.103.117;

    client_max_body_size 32m;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/projects/prj/booking/;
    }

    location /media/ {
        root /home/projects/prj/booking/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/projects/prj/booking/diplom.sock;
    }
}

"""

# Changes the built-in user model to ours
AUTH_USER_MODEL = 'authapp.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

#    'mainapp.middleware.ExceptionHandlerMiddleware',


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'booking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'booking.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = ''

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'django.test04@gmail.com'
EMAIL_HOST_PASSWORD = 'book1234B'

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DOMAIN_NAME = '89.108.103.117'

HANDLE_EXCEPTION = True

# EMAIL_HOST = 'localhost'
# EMAIL_PORT = '25'
# EMAIL_USE_SSL = False
# вариант python -m smtpd -n -c DebuggingServer localhost:25
# EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = None, None
