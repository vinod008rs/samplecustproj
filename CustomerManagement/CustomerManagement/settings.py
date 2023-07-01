import io
import logging
import os
import google.auth
from google.cloud import secretmanager
from urllib.parse import urlparse

import environ

# Import the original settings from each template
from .basesettings import *

# Load the settings from the environment variable
env = environ.Env()
env.read_env(io.StringIO(os.environ.get("APPLICATION_SETTINGS", None)))

# Setting this value from django-environ
env = environ.Env(
    SECRET_KEY=(str, os.getenv("SECRET_KEY")),
    DATABASE_URL=(str, os.getenv("DATABASE_URL")),
    GS_BUCKET_NAME=(str, os.getenv("GS_BUCKET_NAME")),
)
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass
if os.getenv("PYTHON_ENV") == "dev":
    DEBUG = True

# Use GCP secret manager in prod mode
elif os.getenv("GOOGLE_CLOUD_PROJECT", None):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.getenv("SETTINGS_NAME", "django_app_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode(
        "UTF-8"
    )

    env.read_env(io.StringIO(payload))
else:
    raise Exception(
        "No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found."
    )

SECRET_KEY = env("SECRET_KEY")
# If defined, add service URL to Django security settings
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
else:
    ALLOWED_HOSTS = ["*"]

# Default false. True allows default landing pages to be visible
DEBUG = env("DEBUG", default=False)
logging.info(f"Database url : {env.db()}")
# Set this value from django-environ
DATABASES = {"default": env.db()}

# Change database settings if using the Cloud SQL Auth Proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "cloudsql-proxy"
    DATABASES["default"]["PORT"] = 5432

# Define static storage via django-storages[google]
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
STATICFILES_DIRS = []
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"
