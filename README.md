## Data Ingestion Pipeline
Gaming industry is currently one of the most prominent industries in the market. Of all the factors that   determine the popularity of a game, reviews are paramount. This project aims to analyse [Steam reviews](https://www.kaggle.com/datasets/najzeko/steam-reviews-2021) dataset using Elasticsearch engine deployed in a Kubernetes environment where data ingestion queues are handled by RabbitMQ, processes are handled by Celery and data is cached in Redis.

![architecture](/figures/architecture.png)

## Demo Scenario
Whenever dealing with Kubernetes, one can use `micr8s` or `minikube` for kubernetes installation on the base system. MicroK8s is the easiest and fastest way to get Kubernetes up and running. High availability in a Kubernetes cluster, is one of the premiere qualities one should look for when dealing with clusters so as to withstand a failure on any component and continue serving workloads without interruption, therefore the following three factors are necessary for a Highly Available Kubernetes cluster and micro8s serves them all.

## Installation
Simply following the canonical documentation, one can get started with kubernetes installation by using these commands:
- `sudo snap install microk8s –classic`
- `microk8s status –wait-ready`
- `microk8s enable dashboard dns registry istio`

There are a few python based dependies which can be installed
using: `pip3 install -r requirements.txt` for the following directories:
- async_backend
- celery_app
- ingestion_engine

I am also aliasing `microk8s kubectl` to `kcdev` for using kubernetes as a short form for my convenience which was done by adding this alias in the bashrc/zshrc profile.

The directory structure is representative of the commands used to start the kubernetes environment which are as follows: 

- ```elasticsearch-setup-passwords auto```
- ```kcdev apply -f async_backend/deployment_config/service.yaml```
- ```kcdev apply -f async_backend/deployment_config/deployment.yaml```
- ```kcdev apply -f debug_pod/debug_pod.yaml```
- ```kcdev apply -f elasticsearch_config/elasticsearch_deployment.yaml```
- ```kcdev apply -f elasticsearch_config/elasticsearch_pv.yaml```
- ```kcdev apply -f elasticsearch_config/elasticsearch_service.yaml```
- ```kcdev apply -f message_queue/rabbitmq_deployment.yaml```
- ```kcdev apply -f message_queue/rabbitmq_service.yaml```
- ```kcdev apply -f redis/redis_pv.yaml```
- ```kcdev apply -f redis/redis_deployment.yaml```
- ```kcdev apply -f redis/redis_service.yaml```

## Kubernetes Pods
Using Kubernetes, we have setup 6 microservice pods in this project which can be seen in the firgure below. These microservices run in an even driven architecture which are given persistent volumes for claiming the resources.

![pods](/figures/pods.png)

In Kubernetes, a HorizontalPodAutoscaler automatically updates a workload resource (such as a Deployment or StatefulSet), with the aim of automatically scaling the workload to match demand.

![hpa](/figures/hpa.png)

## Persistent Volumes
A PersistentVolume (PV) as shown in the figure below is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using Storage Classes. It is a resource in the cluster just like a node is a cluster resource.

![pv](/figures/pv.png)

A PersistentVolumeClaim (PVC) as shown in the figure below is a request for storage by a user. It is similar to a Pod. Pods consume node resources and PVCs consume PV resources. Pods can request specific levels of resources (CPU and Memory).

![pvc](/figures/pvc.png)

## Results
Using port forwarding to render the results on a Flask application, I am able to show the processes and ids of celery workers running concurrently and scaling at the same time. In the figure below, the process ids are seen on a scaffoled flask template.

![processresult](/figures/processresult.png)

For quering the Steam Reviews for exploration, relevant columns are extracted such as language of review, the review itself, game name and whether it is recommended or not. In the figure below, the process ids are seen on a scaffoled flask template.

![queryresult](/figures/queryresult.png)

## Credits
- [Shlok Walia](https://github.com/coderhyno)
