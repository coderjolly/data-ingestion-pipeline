import uuid

from elasticsearch_client.elasticsearch_client import ElasticSearchClient

esclient = ElasticSearchClient()
index_name = 'retail_store'

mapping = {
    'mappings': {
        'properties': {
            'item_name': {
                'type': 'keyword'
            },
            'price': {
                'type': 'float'
            }
        }
    }
}

query_apple = {
    'query': {
        'bool': {
            'must': {
                'term': {
                    'item_name': 'apple'
                }
            }
        }
    }
}

query_orange = {
    'query': {
        'bool': {
            'must': {
                'term': {
                    'item_name': 'orange'
                }
            }
        }
    }
}

response = esclient.check_and_create_index(index_name, mapping)
print(response)

doc = {'item_name': 'orange', 'price': 200}
response = esclient.index_document(index_name, uuid.uuid4(), doc)
print(response)

response = esclient.get_count(index_name)
print(response)

response = esclient.execute_query(index_name, query_apple)
print(response)

response = esclient.execute_query(index_name, query_orange)
print(response)
