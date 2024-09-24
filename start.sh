#!/bin/bash

# Build and push Docker images
docker build -f Backend/Dockerfile -t gcr.io/solarcaroncloud/backend:latest .
docker push gcr.io/solarcaroncloud/backend:latest

docker build -f Frontend/Dockerfile -t gcr.io/solarcaroncloud/frontend:latest .
docker push gcr.io/solarcaroncloud/frontend:latest

docker build -f Data-Sender/Dockerfile -t gcr.io/solarcaroncloud/data-sender:latest .
docker push gcr.io/solarcaroncloud/data-sender:latest

# Apply Kubernetes deployments
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f sender-deployment.yaml
