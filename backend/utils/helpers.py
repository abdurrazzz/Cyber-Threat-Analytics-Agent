import json
import time
from functools import wraps
from flask import jsonify

def timing_decorator(f):
    """Decorator to measure execution time of functions."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Add timing to result if it's a dictionary
        if isinstance(result, dict):
            result['processing_time'] = execution_time
        
        return result
    return wrapper

def create_error_response(message: str, status_code: int = 400):
    """Create standardized error response."""
    return jsonify({
        'error': True,
        'message': message,
        'status_code': status_code
    }), status_code

def create_success_response(data: dict, message: str = "Success"):
    """Create standardized success response."""
    return jsonify({
        'success': True,
        'message': message,
        'data': data
    }), 200

def load_sample_data(file_path: str):
    """Load sample host data from JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []