import multiprocessing
from os import getenv
bind = '127.0.0.1:8001'
workers = multiprocessing.cpu_count() * 4 + 1
# Read the DEBUG setting from env var
try:
    if getenv('DOCKER_SAL_DEBUG').lower() == 'true':
        errorlog = '/var/log/gunicorn/gunicorn-error.log'
        accesslog = '/var/log/gunicorn/gunicorn-access.log'
        loglevel = 'info'
except:
    pass
