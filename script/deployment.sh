#!/bin/bash

DOCKER_IMAGE_NAME="your-dockerhub-username/flask-api-service"
DOCKER_IMAGE_TAG="latest"
K8S_DEPLOYMENT_NAME="flask-api-deployment"
K8S_SERVICE_NAME="flask-api-service"

docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} .

docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Step 6: Clean up the generated YAML files
rm deployment.yaml service.yaml

echo "Deployment complete!"
