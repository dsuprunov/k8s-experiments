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

kubectl exec -n openbao openbao-0 -- bao write auth/kubernetes/config kubernetes_host="https://kubernetes.default.svc.cluster.local:443"

kubectl exec -n openbao openbao-0 -- bao write auth/kubernetes/role/dummy-openbao-client-role \
  bound_service_account_names=dummy-openbao-client-k8s-auth-serviceaccount \
  bound_service_account_namespaces=dummy-openbao-client-k8s-auth \
  policies=dummy-openbao-client-policy \
  ttl=1h

kubectl create namespace dummy-openbao-client-k8s-auth

kubectl create serviceaccount dummy-openbao-client-k8s-auth-serviceaccount -n dummy-openbao-client-k8s-auth

echo "
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dummy-openbao-client-k8s-auth-serviceaccount
  namespace: dummy-openbao-client-k8s-auth
" | kubectl apply -f -

docker build -t dsuprunov/dummy-openbao-client-k8s-auth:latest ./apps/dummy-openbao-client-k8s-auth/ --no-cache

docker push dsuprunov/dummy-openbao-client-k8s-auth:latest

kubectl run dummy-openbao-client-token-auth-app \
  --restart=Never \
  --rm \
  -i \
  --image=dsuprunov/dummy-openbao-client-k8s-auth:latest \
  --namespace=dummy-openbao-client-k8s-auth \
  --overrides='{"spec": {"serviceAccountName": "dummy-openbao-client-k8s-auth-serviceaccount"}}'
```