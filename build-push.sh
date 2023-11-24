#!/bin/bash

# Stop execution if any command fails
set -e

# Pull the latest changes from the git repository
echo "Pulling latest changes from git..."
git pull

# Build the Docker image without using cache
echo "Building Docker image..."
docker build --no-cache -t deoldify_api -f Dockerfile-api .

# Tag the Docker image
echo "Tagging Docker image..."
docker image tag deoldify_api:latest registry.digitalocean.com/neimuc/deoldify_api:latest

# Push the Docker image to the registry
echo "Pushing Docker image to registry..."
docker push registry.digitalocean.com/neimuc/deoldify_api

echo "Deployment completed successfully."