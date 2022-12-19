import datetime
import logging
import os

import flask
from elasticsearch_client.elasticsearch_client import ElasticSearchClient
from flask import request

import database
import settings
import tasks
from redis_client.redis_client import RedisClient

flask_app = flask.Flask(__name__)
flask_app.logger.setLevel(logging.INFO)
flask_app.config.update(
    CELERY_RESULT_BACKEND=os.environ.get('CELERY_RESULT_BACKEND'),
    CELERY_BROKER_URL=os.environ['CELERY_BROKER_URL']
)

celery_app = tasks.make_celery(flask_app)

redis_client = RedisClient()
elasticsearch_client = ElasticSearchClient()

STEAM_REVIEWS_INDEX_MAPPING = {
    'mappings': {
        'properties': {
            'app_id': {
                'type': 'integer'
            },
            'app_name': {
                'type': 'text'
            },
            'review_id': {
                'type': 'integer'
            },
            'language': {
                'type': 'text'
            },
            'review': {
                'type': 'text'
            },
            'timestamp_updated': {
                'type': 'date',
                'format': 'epoch_second'
            },
            'recommended': {
                'type': 'boolean'
            }
        }
    }
}

STEAM_REVIEWS_INDEX_NAME = 'steam_reviews_data'

QUERY_BASE = {
    'query': {
        'match': {
            'app_name': ''
        }
    }
}


def timestamp2iso(t):
    return '' if t is None else datetime.datetime.fromtimestamp(t).isoformat()


@flask_app.route('/', methods=['GET'])
def get_index():
    return flask.render_template('index.html')


@flask_app.route('/show-data', methods=['GET'])
def get_show_data():
    return flask.render_template('show.html')


@flask_app.route('/task', methods=['POST'])
def post_task():
    if not flask.request.is_json:
        flask_app.logger.warning(f'Invalid non-JSON request with content type {flask.request.content_type}')
        flask.abort(405)

    try:
        data = flask.request.get_json()
        flask_app.logger.info(f'{data}')
    except Exception as e:
        flask_app.logger.warning(
            f'Exception parsing data from request, content type: {flask.request.content_type} {flask.request}', e
        )
        flask.abort(401)

    task_id = None
    try:
        task_id = tasks.create_task(params=data)
        update_cache(data)

        flask_app.logger.info(
            f'Created new task {task_id} for worker data: {data}'
        )
    except Exception as e:
        flask_app.logger.warning(
            f'Exception while creating task: ', e
        )

    return {'task_id': task_id}


@flask_app.route('/game-json', methods=['GET'])
def get_game_processors_json():
    game_name = request.args.get('game_name')
    if game_name is None or game_name == '' or game_name.strip() == '':
        return {}

    value = redis_client.get_data(game_name)
    if value is None:
        return {}

    return {game_name: value}


@flask_app.route('/tasks-json', methods=['GET'])
def get_tasks_json():
    all_tasks = [
        {'id': id,
         'created': timestamp2iso(created),
         'finished': timestamp2iso(finished),
         'result': result or ''}
        for id, created, finished, result in database.get_all()]

    return {'all_tasks': all_tasks}


@flask_app.route('/reviews-data', methods=['GET'])
def get_reviews_data():
    game_name = request.args.get('game_name')

    data = get_game_review(game_name)

    return {'reviews': data}


def get_game_review(game_name):
    data = []
    query = QUERY_BASE
    query['query']['match']['app_name'] = game_name
    flask_app.logger.info(f'Executing query: {str(query)}')

    try:
        flask_app.logger.info('Executing query with size=1000')
        query_result = elasticsearch_client.execute_query(STEAM_REVIEWS_INDEX_NAME, query, size=1000)
        flask_app.logger.info(f'{query_result}')
        flask_app.logger.info(f'{str(query_result)}')
        if 'hits' not in query_result or 'hits' not in query_result['hits']:
            return data

        data_objs = query_result['hits']['hits']
        for data_obj in data_objs:
            if isinstance(data_obj, dict) and '_source' in data_obj:
                data.append(data_obj['_source'])
    except Exception as e:
        flask_app.logger.warning(f'Unable to execute ES query: ', e)

    return data


def update_cache(data):
    value = None

    if not redis_client.acquire_lock():
        return

    if data is not None and isinstance(data, dict) and 'app_name' in data:
        value = redis_client.get_data(data['app_name'])

    if value is None:
        redis_client.set_data(data['app_name'], 1)
    else:
        redis_client.set_data(data['app_name'], value + 1)

    redis_client.release_lock()


if __name__ == '__main__':
    if not os.path.exists(settings.database_path):
        database.init()
        flask_app.logger.info(f'Created database {settings.database_path}')
    else:
        flask_app.logger.info(f'Using existing database {settings.database_path}')
    flask_app.run()
