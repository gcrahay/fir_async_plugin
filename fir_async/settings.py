CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Paris'
CELERY_ENABLE_UTC = True
BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'redis://localhost'

ASYNC_EMAIL_FROM = 'fir@example.com'

EXTERNAL_URL = 'http://127.0.0.1:8000'
