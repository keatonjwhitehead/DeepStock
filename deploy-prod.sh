#!/bin/bash

set -e

# build images
# technically unnec
# docker build -t us.gcr.io/deep-stock-268818/deep-stock-backend:latest -f backend/Dockerfile ./backend
# docker build -t us.gcr.io/deep-stock-268818/deep-stock-frontend:latest -f frontend/Dockerfile ./frontend
# docker build -t us.gcr.io/deep-stock-268818/deep-stock-nginx:latest -f nginx/Dockerfile ./nginx


gcloud auth activate-service-account --key-file ./deep-stock-268818-fce7b0e95509.json

gcloud --quiet config set project deep-stock-268818
# usable by necessity

# gcloud app versions list | grep -v SERVING | awk '{print $2}' | tail -n +1 | xargs -I {} gcloud app versions delete {}
gcloud app deploy frontend/ --stop-previous-version
gcloud app deploy backend/ --stop-previous-version
# gcloud app deploy nginx/ --stop-previous-version

# send images to gcr
# gcloud docker -- push us.gcr.io/deep-stock-268818/deep-stock-frontend
# gcloud docker -- push us.gcr.io/deep-stock-268818/deep-stock-backend
# gcloud docker -- push us.gcr.io/deep-stock-268818/deep-stock-nginx

# deploy from gcr
# doing this deployed both images to default rather than deploying backend image to the backend service
# gcloud app deploy --image-url=us.gcr.io/deep-stock-268818/deep-stock-frontend
# gcloud app deploy --image-url=us.gcr.io/deep-stock-268818/deep-stock-backend

# add tags?
# yes | gcloud beta container images add-tag us.gcr.io/deep-stock-268818/deep-stock-backend:latest gcr.io/${PROJECT_PROD}/${NGINX_IMAGE}:latest
# yes | gcloud beta container images add-tag us.gcr.io/deep-stock-268818/deep-stock-backend:latest gcr.io/${PROJECT_PROD}/${NODE_IMAGE}:latest
