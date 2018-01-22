from celery import Celery


class CeleryApp():
    app = None
    celery = None

    def __init__(self, app, celery_task_list=None):
        self.app = app
        self.celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], include=celery_task_list)
        self.celery.conf.update(app.config)
        TaskBase = self.celery.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
        self.celery.Task = ContextTask