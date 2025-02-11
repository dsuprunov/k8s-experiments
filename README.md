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

kubectl create namespace website

docker-compose up --build

docker build -t dsuprunov/dummy-portal:latest services/website/ --no-cache

docker push dsuprunov/dummy-portal:latest

helm install website services/website/helm/