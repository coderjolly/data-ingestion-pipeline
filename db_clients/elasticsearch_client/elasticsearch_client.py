import logging
import os
import uuid
from sys import stdout
from time import sleep

from elasticsearch import Elasticsearch

logging.basicConfig(stream=stdout, format="%(asctime)s - %(filename)s:%(lineno)d: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

error_logger = logging.getLogger(__name__)
error_logger.setLevel(logging.ERROR)

es_server_url = f"http://{os.environ.get('ES_USERNAME')}:{os.environ.get('ES_PASSWORD')}@" \
                f"elasticsearch-service.default.svc.cluster.local:9200"


# es_server_url = f"http://{os.environ.get('ES_USERNAME')}:{os.environ.get('ES_PASSWORD')}@" \
#                 f"localhost:9200"


class ElasticSearchClient:
    def __init__(self):
        self._esclient = None
        self._connect_to_elasticsearch()

    def _connect_to_elasticsearch(self):
        try:
            self._esclient = Elasticsearch(es_server_url)
        except Exception as e:
            error_logger.error('Exception encountered while connecting to elasticsearch: ', e)

    def refresh_connection(self):
        attempts = 0
        sleep_time = 1

        while attempts < 3 and self._esclient is None:
            sleep(sleep_time)
            self._connect_to_elasticsearch()
            attempts += 1
            sleep_time += 5

    def check_and_create_index(self, index_name: str, mapping: dict) -> bool:
        try:
            index_exists = self._esclient.indices.exists(index=index_name)
        except Exception as e:
            error_logger.error('Exception encountered while running check_and_create_index -> find index exists: ', e)
            return False

        if index_exists:
            return True
        else:
            try:
                self._esclient.indices.create(index=index_name, body=mapping)
            except Exception as e:
                error_logger.error('Exception encountered while running check_and_create_index -> creating index: ', e)
                return False

        return True

    def index_document(self, index_name: str, doc_id: str, doc: dict) -> dict:
        response = {}

        try:
            response = self._esclient.index(index=index_name, id=doc_id, body=doc)
        except Exception as e:
            error_logger.error('Exception encountered while indexing document: ', e)

        return response

    def get_count(self, index_name: str) -> dict:
        response = {}

        try:
            response = self._esclient.count(index=index_name)
        except Exception as e:
            error_logger.error('Exception encountered while getting document count: ', e)

        return response

    def execute_query(self, index_name: str, body: dict, size=100) -> dict:
        response = {}

        try:
            response = self._esclient.search(index=index_name, body=body, size=size)
        except Exception as e:
            error_logger.error(f'Exception encountered while executing query {body}: ', e)

        return response
