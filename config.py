import os, uuid

class Config:
    # General Config
    SECRET_KEY = str(uuid.uuid4())
    DEBUG = os.environ.get('DEBUG', False)

    # Database Config
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:djvv1981@localhost/bootcreator'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cache Config
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = 'redis://localhost:6379/0'

    # Celery backgrnd tasks config
    CELERY = dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    )

    # Security Config
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
