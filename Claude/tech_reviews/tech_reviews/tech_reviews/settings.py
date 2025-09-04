from pathlib import Path
import os

# BASE_DIR points to project root (where manage.py lives)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me-in-production")
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = ["techgadget.it.com", "tech-reviews-e3yp.onrender.com", "127.0.0.1", "localhost"]

# INSTALLED APPS
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "tech_reviews",
    "reviews",
    "users",
    "monetization",
    "categories",
    "compare",
    "deals",
    "products",
    "about",

    # Third-party apps
    "widget_tweaks",
    "crispy_forms",
    "crispy_bootstrap4",
]

# MIDDLEWARE
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tech_reviews.urls"

# TEMPLATES - FIXED: Templates are one level up from BASE_DIR
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.parent / "templates"],  # Go up one level to find templates folder
        "APP_DIRS": True,  # look inside app folders too
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tech_reviews.wsgi.application"

# DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# AUTH PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# STATIC & MEDIA - Static files are in outer tech_reviews directory
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR.parent / "static"]  # Static files one level up from manage.py
STATIC_ROOT = BASE_DIR / "staticfiles"  # Keep staticfiles in the inner directory

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CRISPY FORMS
CRISPY_TEMPLATE_PACK = "bootstrap4"

# AUTH REDIRECTS
LOGIN_REDIRECT_URL = "home"
LOGIN_URL = "login"

# STRIPE KEYS
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")

# DEFAULT PRIMARY KEY TYPE
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"