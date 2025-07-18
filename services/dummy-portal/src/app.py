from flask import Flask, jsonify, make_response, request
import os
from datetime import datetime, timezone


app = Flask(__name__)

@app.route('/')
def root():
    response = make_response(jsonify({
        'host': request.url,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'ip': request.remote_addr,
    }))
    
    response.headers['Content-Type'] = 'application/json'
    
    return response

@app.route('/healthz')
def healthz():
    return 'OK'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    