# To start the server localy
set ENVIRONMENT=local
celery -A app.task_engine worker -l info --pool=eventlet