#!/bin/bash

# Delete Kubernetes deployments and services
kubectl delete -f backend-deployment.yaml
kubectl delete -f frontend-deployment.yaml
kubectl delete -f data-sender-deployment.yaml

# Delete the cluster
gcloud container clusters delete solar-car-cluster --zone us-central1-a
