SECRET_KEY = "fake-key"
ROOT_URLCONF = "tests.urls"
INSTALLED_APPS = [
    "tests",
    "urlauth",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    # import session
    "django.contrib.sessions",
]

# import session
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "urlauth.middleware.AuthKeyMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}