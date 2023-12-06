#!/bin/bash

read -p "Build using Dockerfile-cass, upload to docker hub, and push to kubernetes? (Yes: Enter, No: Ctrl+c)"


# ensure user is in root dir of repo
if [ -e ./Dockerfile-cass ]; then
      echo "----------------------------------------------- STARTING DEPLOY -----------------------------------------------"
else
      echo "[ERROR] Deployment failed: This script MUST be run from the root of your project.  (use ./scripts/deploy.sh)"
      exit 1
fi


#build employee apis docker image
docker build -f ./Dockerfile-cass --tag=docker.io/salsanger/peoplesuite_apis:0.0.1-cass .
#push employee apis docker image to docker hub
docker push salsanger/peoplesuite_apis:0.0.1-cass
#delete old deployment of employee-svc to stop using old container image
kubectl delete deployment cass-emp-svc
#receate deployment of employee-svc
kubectl apply -f ./deployments/app/cass-emp-svc-deployment.yaml 