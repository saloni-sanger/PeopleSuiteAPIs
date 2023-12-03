#!/bin/bash
echo "Opening up cloud application for traffic on \"localhost:8080\""
echo "--> Press Ctrl+c to stop forwarding traffic & exit"
kubectl port-forward --namespace=ingress-nginx service/ingress-nginx-controller 8080:80
