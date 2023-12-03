FROM python:3-slim-bookworm
# FROM publisher/image-name:specific-version, some images don't have a publisher (this is just "python")
WORKDIR /PeopleSuite
# if you don't do a WORKDIR, all the systems libraries and your stuff will get mixed up (hard to debug), call it whatever
COPY . ./ 
#copy this directory's files into the container (dependancies and app files)
#ENV PATH=/PeopleSuite/bin:$PATH
#ENV PYTHONPATH=`pwd`:$PYTHONPATH
#computer looks through folders listed in the PATH environment veriable to know where to find the executable file
#w the same name as what you typed (in this case it couldn't find gunicorn), i included path for gunicorn executable folder
RUN pip3 install -r requirements.txt
#build python environment inside docker container
#.dockerignore excludes our local python venv
EXPOSE 5000
# default port for flask is 5000, flask will listen on this port
#ENTRYPOINT ["/PeopleSuite/bin/gunicorn", "-b", "0.0.0.0:5000", "app:app" ]
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "src.EmployeeService:app" ]
#path:flask_app_name

# entrypoint is for starting the app in the container
# 0.0.0.0 is proper name for localhost
#host 0.0.0.0 port 5000 is the entry point to access our container (which holds our pod/replicas, which hold our app)
# entrpoint is runtime, everything else is build-time

#Dockerfile defines container image, which can be run by docker or k8