from iotsink import iotsink

from iotsink.core.Config import Config


bind = '0.0.0.0:8080'
workers = Config.get('gunicorn')['workers']
loglevel = Config.get('gunicorn')['log_level']
accesslog = '-'
errorlog = '-'

on_starting = iotsink.on_starting
