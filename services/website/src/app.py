from flask import Flask, jsonify, make_response
import os
from datetime import datetime, timezone


app = Flask(__name__)

@app.route('/')
def root():
    response = make_response(jsonify({
        'timestamp': datetime.now(timezone.utc).isoformat()
    }))
    
    response.headers['Content-Type'] = 'application/json'
    
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    