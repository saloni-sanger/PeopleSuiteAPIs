echo "To create database, once in shell run \"CREATE DATABASE peoplesuite;\""
kubectl run -it --rm --image=mysql:5.6 --restart=Never mysql-client -- mysql -h mysql -ppassword