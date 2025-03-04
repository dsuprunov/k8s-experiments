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


## sevices // test-openbao-client

helm repo add openbao https://openbao.github.io/openbao-helm

helm install openbao openbao/openbao --namespace openbao --create-namespace --set "server.dev.enabled=true" --set "server.ha.enabled=false"

kubectl get pods -n openbao

kubectl exec -it openbao-0 -n openbao -- bao operator init -key-shares=1 -key-threshold=1

export BAO_ADDR=http://127.0.0.1:8200
export BAO_TOKEN=root
kubectl exec -it openbao-0 -n openbao -- bao status

kubectl exec -it openbao-0 -n openbao -- bao secrets enable -path=secret kv-v2
kubectl exec -it openbao-0 -n openbao -- bao kv put secret/myapp/credentials username=testuser password=supersecretpassword
kubectl exec -it openbao-0 -n openbao -- bao kv get secret/myapp/credentials

kubectl create namespace test-openbao-client

kubectl get namespace test-openbao-client

kubectl create serviceaccount openbao-auth -n test-openbao-client

kubectl get serviceaccount openbao-auth -n test-openbao-client

kubectl exec -it openbao-0 -n openbao -- bao policy write test-openbao-client-policy - <<EOF
path "secret/data/myapp/credentials" {
  capabilities = ["read"]
}
EOF

kubectl exec -it openbao-0 -n openbao -- bao policy read test-openbao-client-policy

kubectl exec -it openbao-0 -n openbao -- bao auth enable kubernetes

kubectl exec -it openbao-0 -n openbao -- bao write auth/kubernetes/config \
    kubernetes_host="https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT" \
    kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

kubectl exec -it openbao-0 -n openbao -- bao write auth/kubernetes/role/test-openbao-client \
    bound_service_account_names=openbao-auth \
    bound_service_account_namespaces=test-openbao-client \
    policies=test-openbao-client-policy \
    ttl=1h

docker build -t dsuprunov/test-openbao-client:latest services/test-openbao-client/ --no-cache

docker push dsuprunov/test-openbao-client:latest

kubectl run test-openbao-client -n test-openbao-client --restart=Never --rm -i --overrides='{"spec":{"serviceAccountName": "openbao-auth"}}' --image=dsuprunov/test-openbao-client:latest
