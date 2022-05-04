import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'simpleapp.tasks.news_every_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}

# import os
# from celery import Celery
# from django.conf import settings
#
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
#
# app = Celery('project')
#
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
