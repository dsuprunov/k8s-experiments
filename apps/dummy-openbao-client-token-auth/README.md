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

docker build -t dsuprunov/dummy-openbao-client-token-auth:latest ./apps/dummy-openbao-client-token-auth/ --no-cache

docker push dsuprunov/dummy-openbao-client-token-auth:latest

kubectl patch svc openbao -n openbao -p '{"spec": {"type": "NodePort"}}'

export MINIKUBE_IP=$(minikube ip)

export OPENBAO_PORT=$(kubectl get svc openbao -n openbao -o jsonpath='{.spec.ports[?(@.port==8200)].nodePort}')

kubectl exec -n openbao openbao-0 -- bao token create --policy dummy-openbao-client-policy -format=json > ~/openbao-client-keys.json
OPENBAO_CLIENT_TOKEN=$(cat ~/openbao-client-keys.json | jq -r ".auth.client_token")
# --- OR ---
OPENBAO_CLIENT_TOKEN=$(kubectl exec -n openbao openbao-0 -- bao token create --policy dummy-openbao-client-policy -format=json | jq -r ".auth.client_token")

kubectl run dummy-openbao-client-token-auth-app \
  --restart=Never \
  --rm \
  -i \
  --image=dsuprunov/dummy-openbao-client-token-auth:latest \
  --env="OPENBAO_URL=http://openbao.openbao.svc.cluster.local:8200" \
  --env="OPENBAO_TOKEN=$OPENBAO_CLIENT_TOKEN"

kubectl run dummy-openbao-client-token-auth-app \
  --restart=Never \
  --rm \
  -i \
  --image=dsuprunov/dummy-openbao-client-token-auth:latest \
  --env="OPENBAO_URL=http://$MINIKUBE_IP:$OPENBAO_PORT" \
  --env="OPENBAO_TOKEN=$OPENBAO_CLIENT_TOKEN"
```