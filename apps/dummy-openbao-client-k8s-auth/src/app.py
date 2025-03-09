import json
import hvac


if __name__ == '__main__':
    try:
        token_path = '/var/run/secrets/kubernetes.io/serviceaccount/token'
        
        with open(token_path, 'r') as file:
            jwt_token = file.read().strip()
        
        client = hvac.Client(url='http://openbao.openbao.svc.cluster.local:8200')
        
        client.auth.kubernetes.login(
            role='dummy-openbao-client-role',
            jwt=jwt_token
        )
        
        client_secrets = client.secrets.kv.v2.read_secret_version(
            path='dummy-openbao-client',
            mount_point='test',
            raise_on_deleted_version=False
        )        

        print(json.dumps(client_secrets, indent=4, ensure_ascii=False))
    except Exception as e:
        error = {
            'error': str(e),
            'type': str(type(e).__name__)
        }
        print(json.dumps(error, indent=4, ensure_ascii=False))
