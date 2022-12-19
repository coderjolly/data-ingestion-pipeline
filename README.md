```elasticsearch-setup-passwords auto```

```kcdev apply -f async_backend/deployment_config/service.yaml```

```kcdev apply -f async_backend/deployment_config/deployment.yaml```

```kcdev apply -f debug_pod/debug_pod.yaml```

```kcdev apply -f elasticsearch_config/elasticsearch_deployment.yaml```

```kcdev apply -f elasticsearch_config/elasticsearch_pv.yaml```

```kcdev apply -f elasticsearch_config/elasticsearch_service.yaml```

```kcdev apply -f message_queue/rabbitmq_deployment.yaml```

```kcdev apply -f message_queue/rabbitmq_deployment.yaml```

```kcdev apply -f redis/redis_pv.yaml```

```kcdev apply -f redis/redis_deployment.yaml```

```kcdev apply -f redis/redis_service.yaml```