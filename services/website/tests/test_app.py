from unittest.mock import patch
from datetime import datetime, timezone
import pytest
from src.app import app


def test_root():
    fixed_time = datetime(2025, 2, 11, 12, 0, 0, tzinfo=timezone.utc)
    
    with patch('src.app.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_time
        
        with app.test_client() as client:
            response = client.get('/')
            
            assert response.status_code == 200
            
            assert response.headers['Content-Type'] == 'application/json'
            
            json_data = response.get_json()
            
            assert 'timestamp' in json_data
            
            assert json_data['timestamp'] == fixed_time.isoformat()
            