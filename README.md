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


## services // dummy-portal 

docker-compose up --build

docker build -t dsuprunov/dummy-portal:latest services/dummy-portal/ --no-cache

docker push dsuprunov/dummy-portal:latest

helm template dummy-portal services/dummy-portal/helm/ --namespace dummy-portal

helm upgrade --install dummy-portal services/dummy-portal/helm/ --namespace dummy-portal --create-namespace

kubectl get nodes -o wide

kubectl get services -n dummy-portal

minikube service dummy-portal --namespace dummy-portal --url


## sevices // dummy-openbao-client


### OpenBao General Setup

helm repo add openbao https://openbao.github.io/openbao-helm

helm install openbao openbao/openbao --namespace openbao --create-namespace --set "server.ha.enabled=false" # --set "server.dev.enabled=true" --set "agent.injector.enabled=true"

kubectl get pods -n openbao

kubectl exec -n openbao openbao-0 -- bao operator init -key-shares=1 -key-threshold=1 -format=json > openbao-init-keys.json

OPENBAO_UNSEAL_KEY=$(cat openbao-init-keys.json | jq -r ".unseal_keys_b64[0]")
OPENBAO_ROOT_TOKEN=$(cat openbao-init-keys.json | jq -r ".root_token")

kubectl exec -n openbao openbao-0 -- bao operator unseal $OPENBAO_UNSEAL_KEY

kubectl get pods -n openbao

kubectl exec -n openbao openbao-0 -- bao login $OPENBAO_ROOT_TOKEN

kubectl exec -n openbao openbao-0 -- bao secrets enable -version=2 kv


### app/service setup

kubectl exec -n openbao openbao-0 -- bao kv put -mount=kv dummy-openbao-client key1=value1 key2=value2 key3=value3

kubectl exec -n openbao openbao-0 -- bao kv get -mount=kv dummy-openbao-client


cat <<EOF | kubectl exec -n openbao -i openbao-0 -- bao policy write dummy-openbao-client-policy -
path "kv/data/dummy-openbao-client" {
  capabilities = ["read"]
}
EOF

kubectl exec -n openbao -i openbao-0 -- bao policy read dummy-openbao-client-policy

kubectl exec -n openbao openbao-0 -- bao auth enable kubernetes

kubectl exec -n openbao openbao-0 -- bao write auth/kubernetes/config kubernetes_host="https://kubernetes.default.svc.cluster.local:443"

kubectl exec -n openbao openbao-0 -- bao write auth/kubernetes/role/dummy-openbao-client-role \
  bound_service_account_names=dummy-openbao-client-serviceaccount \
  bound_service_account_namespaces=dummy-openbao-client \
  policies=dummy-openbao-client-policy \
  ttl=1h

kubectl create namespace dummy-openbao-client

kubectl create serviceaccount dummy-openbao-client-serviceaccount -n dummy-openbao-client

docker build -t dsuprunov/dummy-openbao-client:latest ./services/dummy-openbao-client/ --no-cache

docker push dsuprunov/dummy-openbao-client:latest

kubectl apply -f services/dummy-openbao-client/k8s/deployment.yaml

kubectl get pods -n dummy-openbao-client

kubectl get services -n dummy-openbao-client
