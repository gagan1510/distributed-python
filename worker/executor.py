from celery import Celery
from celery.signals import after_task_publish
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import config


app = Celery('task', broker = config.CELERY_BROKER_URL, backend="mongodb", include = ['worker.task'])

task_conf = {}
task_conf['result_backend'] = config.MONGODB_URI
task_conf['database'] = config.MONGO_JOB_DB
task_conf['taskmeta_collection'] = config.MONGO_JOB_COLLECTION
task_conf['redis_socket_keepalive'] = True
task_conf['redis_socket_connect_timeout'] = 20
task_conf['redis_retry_on_timeout'] = True
task_conf['result_backend_always_retry'] = True

app.conf.update(task_conf)

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

app.conf.task_default_queue=config.CELERY_QUEUE_NAME

@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
    # the task may not exist if sent using `send_task` which
    # sends tasks by name, so fall back to the default result backend
    # if that is the case.
    task = app.tasks.get(sender)
    backend = task.backend if task else app.backend
    backend.store_result(headers['id'], None, "RUNNING")

if __name__ == '__main__':
    app.start()