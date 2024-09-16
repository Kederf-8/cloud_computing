#!/bin/bash

# Build and push Docker images
docker build -f Dockerfile.backend -t gcr.io/solarcaroncloud/backend:latest .
docker push gcr.io/solarcaroncloud/backend:latest

docker build -f Dockerfile.frontend -t gcr.io/solarcaroncloud/frontend:latest .
docker push gcr.io/solarcaroncloud/frontend:latest

docker build -f Dockerfile.data-sender -t gcr.io/solarcaroncloud/data-sender:latest .
docker push gcr.io/solarcaroncloud/data-sender:latest

# Apply Kubernetes deployments
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f data-sender-deployment.yaml
