from flask import Flask, jsonify, make_response, request
from datetime import datetime, timezone
import os
import hvac


app = Flask(__name__)

@app.route('/')
def root():
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
            mount_point='kv'
        )        

        response = make_response(jsonify({
            'host': request.url,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'secrets': client_secrets,
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
