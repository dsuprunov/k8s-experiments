```bash
kubectl exec -n openbao openbao-0 -- bao secrets enable -version=2 -path=test kv

kubectl exec -n openbao openbao-0 -- bao kv put -mount=test dummy-openbao-client key1=value1 key2=value2 key3=value3

kubectl exec -n openbao openbao-0 -- bao kv get -mount=test dummy-openbao-client

cat <<EOF | kubectl exec -n openbao -i openbao-0 -- bao policy write dummy-openbao-client-policy -
path "test/data/dummy-openbao-client" {
  capabilities = ["read"]
}
EOF

kubectl exec -n openbao -i openbao-0 -- bao policy read dummy-openbao-client-policy

#
# service account setup
#
kubectl exec -n openbao openbao-0 -- bao write auth/kubernetes/config kubernetes_host="https://kubernetes.default.svc.cluster.local:443"

kubectl exec -n openbao openbao-0 -- bao write auth/kubernetes/role/dummy-openbao-client-role \
  bound_service_account_names=dummy-openbao-client-serviceaccount \
  bound_service_account_namespaces=dummy-openbao-client \
  policies=dummy-openbao-client-policy \
  ttl=1h

kubectl create namespace dummy-openbao-client

kubectl create serviceaccount dummy-openbao-client-serviceaccount -n dummy-openbao-client

kubectl apply -f services/dummy-openbao-client/k8s/deployment.yaml

#
# token setup
#
OPENBAO_CLIENT_TOKEN=$(kubectl exec -n openbao openbao-0 -- bao token create --policy dummy-openbao-client-policy -format=json | jq -r ".auth.client_token")


#
# test
#
docker build -t dsuprunov/dummy-openbao-client:latest ./services/dummy-openbao-client/ --no-cache

docker push dsuprunov/dummy-openbao-client:latest

kubectl get pods -n dummy-openbao-client

kubectl get services -n dummy-openbao-client

export MINIKUBE_IP=$(minikube ip)

export OPENBAO_PORT=$(kubectl get svc openbao -n openbao -o jsonpath='{.spec.ports[?(@.port==8200)].nodePort}')

curl "http://192.168.49.2:32718?token=$OPENBAO_CLIENT_TOKEN&url=http://$MINIKUBE_IP:$OPENBAO_PORT"
```