from celery import Celery


class CeleryApp:
    app = None
    celery = None

    CELERY_TASK_LIST = [
        'app.blueprints.api.tasks'
        ]

    def __init__(self, app):
        self.app = app
        self.celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], include=self.CELERY_TASK_LIST)
        self.celery.conf.update(app.config)
        self.celery.conf.ONCE = app.config['CELERY_ONCE_CONFIG']
        TaskBase = self.celery.Task
        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
        self.celery.Task = ContextTask