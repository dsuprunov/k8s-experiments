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


### OpenBao General Setup

```bash
helm repo add openbao https://openbao.github.io/openbao-helm

helm install openbao openbao/openbao --namespace openbao --create-namespace --set "server.ha.enabled=false" # --set "server.dev.enabled=true"

kubectl get namespaces

helm repo add openbao https://openbao.github.io/openbao-helm

helm install openbao openbao/openbao --namespace openbao --set "server.ha.enabled=false"

kubectl get pods -n openbao

# if OpenBao PODs are in Pending mode check for possible issue with PVC/PV claim (no default StorageClass)
# https://stackoverflow.com/questions/74741993/0-1-nodes-are-available-1-pod-has-unbound-immediate-persistentvolumeclaims

kubectl exec -n openbao openbao-0 -- bao operator init -key-shares=1 -key-threshold=1 -format=json > ~/openbao-init-keys.json
OPENBAO_UNSEAL_KEY=$(cat ~/openbao-init-keys.json | jq -r ".unseal_keys_b64[0]")
OPENBAO_ROOT_TOKEN=$(cat ~/openbao-init-keys.json | jq -r ".root_token")

kubectl exec -n openbao openbao-0 -- bao operator unseal $OPENBAO_UNSEAL_KEY

kubectl exec -n openbao openbao-0 -- bao login $OPENBAO_ROOT_TOKEN

kubectl exec -n openbao openbao-0 -- bao auth enable kubernetes

kubectl apply -f staging-openbao.yaml

kubectl get pods -n openbao
```
