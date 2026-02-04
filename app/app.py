import os
import json
import yaml
from flask import Flask, jsonify, render_template
from azure.storage.blob import BlobServiceClient
from cachetools import cached, TTLCache

app = Flask(__name__)

# Configuration via variables d'environnement (12 Factor App)
AZURE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = "content"

# Cache: TTL de 60 secondes 
cache = TTLCache(maxsize=100, ttl=60)

def get_blob_content(filename):
    """Récupère et parse le contenu depuis Azure Blob Storage"""
    if not AZURE_CONNECTION_STRING:
        return {"error": "Azure Connection String missing"}
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=filename)
        data = blob_client.download_blob().readall()
        
        if filename.endswith('.json'):
            return json.loads(data)
        elif filename.endswith('.yaml') or filename.endswith('.yml'):
            return yaml.safe_load(data)
    except Exception as e:
        return {"error": str(e)}

@app.route('/healthz')
def healthz():
    """Vérification de vie"""
    return jsonify({"status": "alive"}), 200

@app.route('/readyz')
def readyz():
    """Vérification de disponibilité (Check connexion Azure) [cite: 40]"""
    if not AZURE_CONNECTION_STRING:
         return jsonify({"status": "not ready", "reason": "No storage config"}), 503
    return jsonify({"status": "ready"}), 200

@app.route('/api/events')
@cached(cache)
def get_events():
    """Endpoint Events"""
    return jsonify(get_blob_content("events.json"))

@app.route('/api/news')
@cached(cache)
def get_news():
    """Endpoint News"""
    return jsonify(get_blob_content("news.yaml"))

@app.route('/api/faq')
@cached(cache)
def get_faq():
    """Endpoint FAQ"""
    return jsonify(get_blob_content("faq.json"))

@app.route('/')
def index():
    """Interface web minimale"""
    return "<h1>Plateforme Cloud-Native</h1><p>API Running</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)