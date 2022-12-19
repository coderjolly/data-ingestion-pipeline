import logging

import celery
import steam_data_processor.task

import database


def make_celery(app):
    c = celery.Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    c.conf.update(app.config)

    class ContextTask(c.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    c.Task = ContextTask
    return c


def create_task(params, queue_name='steam_data_processor'):
    logging.info(f'Creating task for params: {params}')

    task_id = database.create_task()
    queue_options = {}

    match queue_name:
        case 'celery':
            queue_options['queue'] = 'celery'
        case _:
            queue_options['queue'] = 'celery'
    print(f'Task queue options: {queue_options}')

    task = steam_data_processor.task.steam_data_processor.signature(
        (params,),
        immutable=True,
        options=queue_options
    )

    task.apply_async()
    return task_id
