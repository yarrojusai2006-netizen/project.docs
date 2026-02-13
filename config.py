import os
from pathlib import Path


def load_config():
    """Load configuration from .env file"""
    config = {}
    env_file = Path(__file__).parent / '.env'
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
    
    return config


def get_api_key():
    """Get API key from .env file or environment"""
    config = load_config()
    return config.get('API_KEY') or os.getenv('API_KEY')
