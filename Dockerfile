#Dockerfile defines container image, which can be run by docker or k8, k8 will use yaml deployment

# FROM publisher/image-name:specific-version, some images don't have a publisher (this is just "python")
FROM python:3.9-slim-bookworm

# if you don't do a WORKDIR, all the systems libraries and your stuff will get mixed up (hard to debug), call it whatever
WORKDIR /PeopleSuite

# install toolchain for building mysqlclient
RUN apt-get update
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkgconf

#copy just requirements so this build step can be cached unless specifically requirements.txt changes
COPY requirements.txt .

#build python environment inside docker container
#.dockerignore excludes our local python venv
RUN pip3 install -r requirements.txt

#copy src directory's files into the container (app files only)
COPY src ./src

# default port for flask is 5000, flask will listen on this port
EXPOSE 5000

# entrypoint is for starting the app in the container
# 0.0.0.0 is proper name for localhost
#host 0.0.0.0 port 5000 is the entry point to access our container (which holds our pod/replicas, which hold our app)
#last argument: path:flask_app_name
# entrpoint is runtime, everything else is build-time
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "src.EmployeeService:app" ]