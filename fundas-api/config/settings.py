from celery.schedules import crontab


# Flask Debug flag.
DEBUG = True

# Default log level
LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

# Server name is required by Pytest .
SERVER_NAME = '192.168.2.100:8000'

# Flask secret required for session related features.
# Should be overriden using instance properties
SECRET_KEY = 'ASecretStringGoesHere!!'

# Database properties. Override in Instance config.
SQLALCHEMY_DATABASE_URI = 'postgresql://fundas:devpassword@postgres:5432/fundas'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# OAuth config for various providers. Override in instance properties
OAUTH_CONFIG = {
    "GOOGLE": {
        "client_id": "google-client-id",
        "client_secret": "google-client-secret"
    },
    "FACEBOOK": {
        "client_id": "facebook-client-id",
        "client_secret": "facebook-client-secret"
    },
    "GITHUB": {
        "client_id": "github-client-id",
        "client_secret": "github-client-secret"
    }
}

# Disable this for production like environments
OAUTHLIB_INSECURE_TRANSPORT = "1"


# Disable redirect interception.
DEBUG_TB_INTERCEPT_REDIRECTS = False

# pagination
ITEMS_PER_PAGE = 6

# Important properties to override in instance config:
# SECRET_KEY
# OAUTH_CONFIG
# SQLALCHEMY_DATABASE_URI

#Celery
# Celery.
CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5
CELERY_ROUTES = {
    'app.blueprints.api.tasks.update_companies': {
        'queue': 'periodic'
    },
    'app.blueprints.api.tasks.update_screener': {
        'queue': 'periodic'
    }
}
CELERYBEAT_SCHEDULE = {
    'update-companies': {
        'task': 'app.blueprints.api.tasks.update_companies',
        'schedule': crontab(hour=f'*/24')
    },
    'update-screener': {
        'task': 'app.blueprints.api.tasks.update_screener',
        'schedule': crontab(hour=f'*/48')
    }

}
CELERY_ONCE_CONFIG = {
            'backend': 'celery_once.backends.Redis',
            'settings': {
                'url': CELERY_RESULT_BACKEND,
                'default_timeout': 60 * 60
            }
        }
