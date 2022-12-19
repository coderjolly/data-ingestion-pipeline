"""
CLI Celery app for handling steam_data_processor calls asynchronously.
"""
import os

import celery

app = celery.Celery('steam_data_processor',
                    backend=os.environ.get('CELERY_RESULT_BACKEND'),
                    broker=os.environ['CELERY_BROKER_URL'])

if __name__ == '__main__':
    worker = app.Worker(
        include=['steam_data_processor.task']
    )
    worker.start()
