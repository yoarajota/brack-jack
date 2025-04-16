Install MongoDB Community with Docker
You can run MongoDB community Edition as a Docker container using the official MongoDB Community image. Using a Docker image for running your MongoDB deployment is useful to:

Stand up a deployment quickly.

Help manage configuration files.

Test different features on multiple versions of MongoDB.

About This Task
This page describes the Docker install instructions for MongoDB Community edition. The MongoDB Enterprise Docker image and MongoDB Enterprise Kubernetes Operator are recommended for production deployments and should be used together. For enterprise instructions, see Install MongoDB Enterprise with Docker.

This procedure uses the official MongoDB community image, which is maintained by MongoDB.

A full description of Docker is beyond the scope of this documentation. This page assumes prior knowledge of Docker.

MongoDB 5.0+ Docker images require AVX support on your system. If your system does not support AVX, you can use a docker image of MongoDB prior to version 5.0.

Warning
Versions of MongoDB prior to 5.0 are EOL'd and no longer supported by MongoDB. These versions should be used for testing purposes only.

Before You Begin
Install Docker

Install mongosh

Procedure
1
Pull the MongoDB Docker Image
docker pull mongodb/mongodb-community-server:latest

2
Run the Image as a Container
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest