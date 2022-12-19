import logging
from pathlib import Path

import pandas as pd
import requests

ASYNC_SERVICE_BASE_URL = 'http://localhost:5000/task'
DEFAULT_CHUNK_SIZE = 10
DEFAULT_FILENAME = str(Path.home() / 'Downloads/steam_reviews.csv')
PROPERTIES = ['app_id', 'app_name', 'review_id', 'language', 'review', 'timestamp_updated', 'recommended']


def parse_data_chunk(data_chunk, properties=PROPERTIES):
    data = [{}] * 10

    print(data_chunk)

    for property_name in properties:
        for idx, property_value in enumerate(data_chunk[property_name]):
            data[idx][property_name] = property_value

    return data


def send_data_for_processing(data_obj, processor_url=ASYNC_SERVICE_BASE_URL):
    response = requests.post(processor_url, json=data_obj, headers={'Content-type': 'application/json; charset=utf-8'})
    print(response)

    return response


def read_and_process_csv(filename, chunk_size=DEFAULT_CHUNK_SIZE):
    idx = 0

    for chunk in pd.read_csv(filename, chunksize=chunk_size):
        data_objects = parse_data_chunk(chunk)

        for data_object in data_objects:
            try:
                response = send_data_for_processing(data_object)
                logging.info(f'{idx} Successfully sent chunk for processing, response code: {response.status_code}')
            except Exception as e:
                logging.error(f'{idx} Exception encountered while sending chunk for processing: ', e)
            idx += 1


if __name__ == '__main__':
    read_and_process_csv(DEFAULT_FILENAME)
