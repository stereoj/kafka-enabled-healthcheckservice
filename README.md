# Kafka-Enabled HealthCheckService Deployment on Kubernetes

## Scenario
You are working for a company that is building a microservices architecture with Kafka as the messaging backbone. The team is responsible for deploying and managing these services on a Kubernetes cluster.

## Task Requirements

### Set up Local Kubernetes Cluster
1. Install Minikube:
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube

2. Start Minikube:
    minikube start

3. Ensure `kubectl` is configured:
    kubectl config use-context minikube

### Set up Kafka Cluster on Kubernetes
1. Install Helm:
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

2. Add Kafka Helm repository and update:
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm repo update

3. Deploy Kafka with 3 nodes:
    helm install my-kafka bitnami/kafka --set replicaCount=3

4. Create Kafka topic:
    kubectl port-forward svc/my-kafka 9092:9092 &
    kafka-topics.sh --create --topic health_checks_topic --bootstrap-server localhost:9092 --replication-factor 3 --partitions 1

### Deploy Python Services

#### HealthCheckService
Write a Python service named HealthCheckService that periodically performs health checks on various
microservices in the system.
The service should have a REST API endpoint /check_health that retrieves the health status of different
microservices from the Kafka topic (health_checks_topic) and prints the results along with some text to the logs.
`health_check_service.py`


#### ConsumerHealthCheckService
Write another Python service named ConsumerHealthCheckService that consumes health check messages from
the health_checks_topic.
The service should have a REST API endpoint /get_latest_health_check that retrieves and prints the latest health
check results from the Kafka topic.
`consumer_health_check_service.py`


### Kubernetes Manifests
Create Kubernetes deployment manifests for both the HealthCheckService and ConsumerHealthCheckService.
Implement a rolling deployment strategy for these services.
Use ConfigMaps/Secrets to manage any configuration that needs to be externalized. Ensure that the services can
scale horizontally.
`health-check-service-deployment.yaml` in `deployments/` directory
`consumer-health-check-service-deployment.yaml` in `deployments/` directory


### Monitoring and Logging
Set up monitoring for the Kafka cluster, HealthCheckService, and ConsumerHealthCheckService.
Implement logging for both services, including printing health check results along with some text.
1. Install Prometheus and Grafana using Helm:
    ```bash
    helm install prometheus bitnami/prometheus
    helm install grafana bitnami/grafana
    ```
2. Install Fluent Bit for logging:
    ```bash
    helm install fluent-bit bitnami/fluent-bit
    ```
3. Update deployment manifests to include logging configurations:
    ```yaml
    # Add volumes and volume mounts to your deployment spec
    spec:
      containers:
      - name: health-check-service
        ...
        volumeMounts:
        - name: varlog
          mountPath: /var/log
      volumes:
      - name: varlog
        emptyDir: {}
    ```