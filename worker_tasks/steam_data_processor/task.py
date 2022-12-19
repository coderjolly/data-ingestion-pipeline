import logging
import uuid
from sys import stdout

from celery import shared_task
from elasticsearch_client.elasticsearch_client import ElasticSearchClient

from redis_client.redis_client import RedisClient

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

logging.basicConfig(stream=stdout, format="%(asctime)s - %(filename)s:%(lineno)d: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

error_logger = logging.getLogger(__name__)
error_logger.setLevel(logging.ERROR)

redis_client = RedisClient()
elasticsearch_client = ElasticSearchClient()


@shared_task
def steam_data_processor(params):
    if not isinstance(params, dict) or 'app_name' not in params:
        logger.info(
            f'isinstance of dict: {isinstance(params, dict)} app_name not in params: {"app_name" not in params}')
        return 'NOK'

    print(params)

    add_review_to_es(params)

    update_game_cache(params['app_name'])

    print('============================================')
    print('============================================')

    return 'OK'


def add_review_to_es(params):
    if not elasticsearch_client.check_and_create_index(STEAM_REVIEWS_INDEX_NAME, STEAM_REVIEWS_INDEX_MAPPING):
        error_logger.error(f'Error creating ES index for index name: {STEAM_REVIEWS_INDEX_NAME}')
        return

    elasticsearch_client.index_document(STEAM_REVIEWS_INDEX_NAME, uuid.uuid4(), params)
    logger.info(f'Data set for game: {params["app_name"]}')


def update_game_cache(game_name):
    if not redis_client.acquire_lock():
        error_logger.error(f'Not able to acquire log for game_name: {game_name}')
        return

    number_of_remaining_messages = redis_client.get_data(game_name)
    logger.info(f'number_of_remaining_messages: {number_of_remaining_messages}')
    redis_client.set_data(game_name, number_of_remaining_messages - 1)

    redis_client.release_lock()
