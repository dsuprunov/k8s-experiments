from flask import Flask, jsonify, make_response, request
from datetime import datetime, timezone
import os
import hvac


app = Flask(__name__)

def by_service_account():
        token_path = '/var/run/secrets/kubernetes.io/serviceaccount/token'
        
        with open(token_path, 'r') as file:
            jwt_token = file.read().strip()
        
        client = hvac.Client(url='http://openbao.openbao.svc.cluster.local:8200')
        
        client.auth.kubernetes.login(
            role='dummy-openbao-client-role',
            jwt=jwt_token
        )
        
        return client.secrets.kv.v2.read_secret_version(
            path='dummy-openbao-client',
            mount_point='test',
            raise_on_deleted_version=False
        )        


def by_token(token: str, url: str):
        assert token, "The 'token' request parameter is missing or empty."

        assert url, "The 'url' request parameter is missing or empty."
        
        client = hvac.Client(url=url)

        client.token = token
        
        return client.secrets.kv.v2.read_secret_version(
            path='dummy-openbao-client',
            mount_point='test',
            raise_on_deleted_version=False
        )


@app.route('/')
def root():
    try:
        response = make_response(jsonify({
            'host': request.url,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'by_service_account': by_service_account(),
            'by_token': by_token(token=request.args.get('token'), url=request.args.get('url')),
        }))
        
        response.headers['Content-Type'] = 'application/json'
        
        return response
    except Exception as e:
        error_message = {
            'error': str(e),
            'type': str(type(e).__name__)
        }
        return make_response(jsonify(error_message), 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)