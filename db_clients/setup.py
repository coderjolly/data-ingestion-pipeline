from setuptools import setup

setup(
    name='db_clients',
    version='0.0.1',
    description='Provides interface to query different DBs',
    packages=['elasticsearch_client', 'redis_client']
)
