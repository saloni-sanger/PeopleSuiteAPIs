FROM python:3-slim-bookworm
# FROM publisher/image-name:specific-version, some images don't have a publisher (this is just "python")
WORKDIR /PeopleSuite
# if you don't do a WORKDIR, all the systems libraries and your stuff will get mixed up (hard to debug), call it whatever
COPY . ./
ENTRYPOINT ["flask", "--app", "app", "run"]

# entrypoint is for starting the app in the container
# entrpoint is runtime, everything else is build-time