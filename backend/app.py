from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import logging
import time
from datetime import datetime

from config import Config
from services.ai_service import AIService
from services.data_processor import DataProcessor
from utils.helpers import timing_decorator, create_error_response, create_success_response, load_sample_data

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize services
ai_service = AIService()
data_processor = DataProcessor()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return create_success_response({
        'status': 'healthy',
        'version': '1.0.0',
        'ai_provider': Config.AI_PROVIDER,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/summarize', methods=['POST'])
@timing_decorator
def summarize_hosts():
    """Main endpoint for host data summarization."""
    try:
        data = request.get_json()
        
        if not data or 'hosts' not in data:
            return create_error_response("Missing 'hosts' field in request data")
        
        hosts = data['hosts']
        summary_type = data.get('summary_type', 'detailed')
        
        if not isinstance(hosts, list):
            return create_error_response("'hosts' must be a list")
        
        if len(hosts) == 0:
            return create_error_response("Host list cannot be empty")
        
        # Clean and validate host data
        cleaned_hosts = data_processor.clean_host_data(hosts)
        
        if not cleaned_hosts:
            return create_error_response("No valid host data found")
        
        # Generate summary using AI
        summary_result = ai_service.summarize_hosts(cleaned_hosts, summary_type)
        
        # Get basic statistics
        stats = data_processor.get_summary_stats(cleaned_hosts)
        
        # Combine results
        result = {
            **summary_result,
            'stats': stats,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return create_success_response(result, "Summary generated successfully")
        
    except Exception as e:
        logger.error(f"Error in summarize_hosts: {str(e)}")
        return create_error_response(f"Internal server error: {str(e)}", 500)

@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    """Get sample host data for testing."""
    sample_data = load_sample_data('./data/sample_hosts.json')
    
    # Handle both wrapped (with metadata) and unwrapped formats
    if isinstance(sample_data, dict) and 'hosts' in sample_data:
        hosts = sample_data['hosts']
    elif isinstance(sample_data, list):
        hosts = sample_data
    else:
        hosts = []
    
    if not hosts:
        # Create some sample data if file doesn't exist or is empty
        hosts = [
            {
                "ip": "8.8.8.8",
                "services": [{"port": 53, "protocol": "tcp"}],
                "location": {"country": "United States", "country_code": "US"},
                "autonomous_system": {"asn": 15169, "name": "Google LLC"}
            }
        ]
    
    return create_success_response({
        'hosts': hosts,
        'count': len(hosts)
    })

@app.route('/api/upload', methods=['POST'])
def upload_data():
    """Handle file upload for host data."""
    try:
        if 'file' not in request.files:
            return create_error_response("No file uploaded")
        
        file = request.files['file']
        
        if file.filename == '':
            return create_error_response("No file selected")
        
        if not file.filename.endswith('.json'):
            return create_error_response("Only JSON files are supported")
        
        # Read and parse JSON file
        content = file.read().decode('utf-8')
        data = json.loads(content)
        
        # Handle both wrapped (with metadata/hosts) and unwrapped formats
        if isinstance(data, dict) and 'hosts' in data:
            hosts_data = data['hosts']
        elif isinstance(data, list):
            hosts_data = data
        else:
            return create_error_response("Invalid JSON structure. Expected 'hosts' array or list of hosts")
        
        if not isinstance(hosts_data, list):
            return create_error_response("Hosts data must be a list")
        
        return create_success_response({
            'hosts': hosts_data,
            'count': len(hosts_data)
        }, "File uploaded successfully")
        
    except json.JSONDecodeError:
        return create_error_response("Invalid JSON format")
    except Exception as e:
        logger.error(f"Error in upload_data: {str(e)}")
        return create_error_response(f"Upload failed: {str(e)}", 500)

# Serve static files for frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )