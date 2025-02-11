# k8s-minikube

## Install docker

https://docs.docker.com/engine/install/ubuntu

## Install minikube

https://minikube.sigs.k8s.io/docs/start/


## Install kubectl

https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/


## Something general

minikube start --driver=docker

minikube status

minikube stop

minikube delete


## services // website

docker-compose up --build

docker build -t website:latest services/website/

