#!/bin/bash

read -p "Build using Dockerfile, upload to docker hub, and push to kubernetes? (Yes: Enter, No: Ctrl+c)"


# ensure user is in root dir of repo
if [ -e ./Dockerfile ]; then
      echo "----------------------------------------------- STARTING DEPLOY -----------------------------------------------"
else
      echo "[ERROR] Deployment failed: This script MUST be run from the root of your project.  (use ./scripts/deploy.sh)"
      exit 1
fi


#build employee apis docker image
docker build --tag=docker.io/salsanger/peoplesuite_apis:0.0.1 .
#push employee apis docker image to docker hub
docker push salsanger/peoplesuite_apis:0.0.1
#delete old deployment of employee-svc to stop using old container image
kubectl delete deployment employee-svc
#receate deployment of employee-svc
kubectl apply -f ./deployments/app/employee-svc-deployment.yaml 