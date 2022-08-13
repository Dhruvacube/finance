import configparser
import os
import secrets
from pathlib import Path
from typing import Any

import dj_database_url


class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __hash__(self):
        return 0

    def __repr__(self):
        return "..."

    def __iter__(self):
        return iter([])

    def __len__(self):
        return 0


MISSING: Any = _MissingSentinel()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


CONFIG_FILE = BASE_DIR / ".conf"


def token_get(tokenname: str = MISSING, all: bool = False) -> Any:
    """Helper function to get the credentials from the environment variables or from the configuration file

    :param tokenname: The token name to access
    :type tokenname: str
    :param all: Return all values from config filename, defaults to False
    :type all: bool, optional
    :raises RuntimeError: When all set :bool:`True` and `.ini` file is not found
    :return: The environment variables data requested if not found then None is returned
    :rtype: Any
    """
    if not all:
        if CONFIG_FILE.is_file():
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            sections = config._sections
            for i in sections:
                for j in sections[i]:
                    if j.lower() == tokenname.lower():
                        return sections[i][j]
            return
        return os.environ.get(tokenname, "False").strip("\n")
    if CONFIG_FILE.is_file():
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        return config._sections
    raise RuntimeError("Could not find .ini file")

class _envConfig:
    """A class which contains all token configuration"""

    def __init__(self):
        self.data: dict = token_get(all=True)
        for i in self.data:
            for j in self.data.get(i, MISSING):
                setattr(self, j.lower().strip("\n"), self.data[i].get(j))
                setattr(self, j.upper().strip("\n"), self.data[i].get(j))


envConfig: Any = _envConfig()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = secrets.token_urlsafe(25)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "mathfilters",
    "colorfield",
    "bootstrap5",
    "sheets.apps.SheetsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    # "htmlmin.middleware.HtmlMinifyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "finance.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, pkg, "template")
            for pkg in ["finance", "sheets"]
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "libraries": {
                #  Make `finance_extras` available to other apps
                "finance_extras": "finance.templatetags.finance_extras",  # noqa: E501
            },
            "context_processors": [
                "finance.template.context_processors.version",
                "sheets.template.context_processors.sheet_date_list",
                "sheets.template.context_processors.current_sheet_date",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "finance.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if not bool(int(getattr(envConfig, 'COCKROACH_DB', 0))):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'], engine='django_cockroachdb')}


# Auth

LOGIN_REDIRECT_URL = "/sheets/"
LOGOUT_REDIRECT_URL = "/"


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = "/static/"


# Currency formatting

CURRENCY_GROUP_SEPARATOR = getattr(envConfig, "CURRENCY_GROUP_SEPARATOR", " ")
CURRENCY_DECIMAL_SEPARATOR = getattr(envConfig, "CURRENCY_DECIMAL_SEPARATOR", ",")
CURRENCY_PREFIX = getattr(envConfig, "CURRENCY_PREFIX", "₹")
CURRENCY_SUFFIX = getattr(envConfig, "CURRENCY_SUFFIX", "")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

DEBUG = bool(int(getattr(envConfig, 'DEBUG', 0))) 

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    CACHE_MIDDLEWARE_SECONDS = 0

if bool(int(getattr(envConfig, 'WHITENOISE', 0))):
    MIDDLEWARE = ([MIDDLEWARE[0]] +
                  ["whitenoise.middleware.WhiteNoiseMiddleware"] +
                  MIDDLEWARE[1:])
    INSTALLED_APPS = (INSTALLED_APPS[0:-1] + [
        "whitenoise.runserver_nostatic",
    ] + [INSTALLED_APPS[-1]])

if bool(int(getattr(envConfig, 'PRODUCTION_SERVER', 0))):
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000 
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "same-origin"
else:
    CACHE_MIDDLEWARE_SECONDS = 0

MEDIA_ROOT = BASE_DIR/ "media"
MEDIA_URL = "/media/"

THEME_DICT = {
    'yeti': '008CBA',
    'cerulean': '2FA4E7',
    'darkly': '375A7F',
    'litera': 'FFF',
    'materia': '299AF3',
    'pulse': '593196',
    'simplex': 'FFFFFF',
    'solar': '073642',
    'united': 'E95420',
    'zephyr': '3459E6',
    'cosmo': '2780E3',
    'flatly': '2C3E50',
    'lumen': 'F6F6F6',
    'minty': '78C2AD',
    'quartz': 'E83283',
    'sketchy': 'FFFFFF',
    'spacelab': 'EEEEEE',
    'vapor': '6F42C1',
    'cyborg':'060606',
    'journal': 'FFFFFF',
    'lux': 'FFFFFF',
    'morph': '378DFC',
    'sandstone': '325D88',
    'slate': '3A3F44',
    'superhero': '20374C'
}

DJANGO_ALLOW_ASYNC_UNSAFE = True
