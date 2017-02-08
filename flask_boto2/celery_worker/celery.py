from __future__ import absolute_import

from celery import Celery
from config import Config

app = Celery('celery_worker',
             broker=Config.BROKER_URL,
             backend=Config.BROKER_URL,
             include=['celery_worker.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
