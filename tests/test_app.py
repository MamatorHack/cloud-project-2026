import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.app import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_healthz(client):
    """Test obligatoire: Vérifie que l'endpoint /healthz répond 200"""
    rv = client.get('/healthz')
    assert rv.status_code == 200
    assert rv.json == {"status": "alive"}

@patch('app.app.BlobServiceClient')
def test_get_events_mocked(mock_blob_service, client):
    """Test fonctionnel: Simule Azure pour vérifier /api/events sans connexion réelle"""
    #prépare le faux client Azure
    mock_client = MagicMock()
    mock_blob_service.from_connection_string.return_value.get_blob_client.return_value = mock_client
    
    #définit ce que Azure est censé renvoyer
    fake_json_content = b'{"items": [{"id": 1, "title": "Test Event"}]}'
    mock_client.download_blob.return_value.readall.return_value = fake_json_content

    #appelle l'API
    rv = client.get('/api/events')

    assert rv.status_code == 200
    assert rv.json['items'][0]['title'] == "Test Event"