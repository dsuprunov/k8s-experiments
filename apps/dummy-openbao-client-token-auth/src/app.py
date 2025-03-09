import os
import json
import hvac


if __name__ == '__main__':
    try:
        token = os.getenv("OPENBAO_TOKEN")
        assert token, "The environment variable 'OPENBAO_TOKEN' is not set or is empty."

        url = os.getenv("OPENBAO_URL")
        assert url, "The environment variable 'OPENBAO_URL' is not set or is empty."
        
        client = hvac.Client(url=url)

        client.token = token
        
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
