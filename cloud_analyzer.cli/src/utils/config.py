"""Configuration management utilities."""

import json
import logging
from pathlib import Path
from typing import Dict, Optional

from cryptography.fernet import Fernet

from cli_constants import FILE_PERMISSION_OWNER_RW

logger = logging.getLogger(__name__)


def get_config_dir() -> Path:
    """Get configuration directory path."""
    config_dir = Path.home() / ".cloud-analyzer"
    config_dir.mkdir(exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    """Get configuration file path."""
    return get_config_dir() / "config.json"


def get_key_file() -> Path:
    """Get encryption key file path."""
    return get_config_dir() / ".key"


def get_or_create_key() -> bytes:
    """Get or create encryption key."""
    key_file = get_key_file()
    
    if key_file.exists():
        return key_file.read_bytes()
    
    # Generate new key
    key = Fernet.generate_key()
    key_file.write_bytes(key)
    
    # Set restrictive permissions (owner read/write only)
    key_file.chmod(FILE_PERMISSION_OWNER_RW)
    
    return key


def encrypt_config(config: dict) -> dict:
    """Encrypt sensitive configuration values."""
    encryption_key = get_or_create_key()
    fernet = Fernet(encryption_key)
    
    encrypted_config = {}
    sensitive_keys = ["secret", "password", "key", "token", "credentials"]
    
    for provider, provider_config in config.items():
        encrypted_config[provider] = {}
        
        for config_key, value in provider_config.items():
            # Check if this is a sensitive field
            is_sensitive = any(s in config_key.lower() for s in sensitive_keys)
            
            if is_sensitive and isinstance(value, str):
                # Encrypt the value
                encrypted_value = fernet.encrypt(value.encode()).decode()
                encrypted_config[provider][config_key] = {
                    "encrypted": True,
                    "value": encrypted_value,
                }
            else:
                encrypted_config[provider][config_key] = value
    
    return encrypted_config


def decrypt_config(encrypted_config: dict) -> dict:
    """Decrypt sensitive configuration values."""
    encryption_key = get_or_create_key()
    fernet = Fernet(encryption_key)
    
    config = {}
    
    for provider, provider_config in encrypted_config.items():
        config[provider] = {}
        
        for config_key, value in provider_config.items():
            if isinstance(value, dict) and value.get("encrypted"):
                # Decrypt the value
                decrypted_value = fernet.decrypt(
                    value["value"].encode()
                ).decode()
                config[provider][config_key] = decrypted_value
            else:
                config[provider][config_key] = value
    
    return config


def load_config() -> Optional[Dict[str, Dict[str, str]]]:
    """Load configuration from file."""
    config_file = get_config_file()
    
    if not config_file.exists():
        return None
    
    try:
        with open(config_file, "r") as f:
            encrypted_config = json.load(f)
        
        return decrypt_config(encrypted_config)
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"Failed to load config file: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading config: {e}")
        raise


def save_config(config: Dict[str, Dict[str, str]]) -> None:
    """Save configuration to file."""
    config_file = get_config_file()
    
    # Encrypt sensitive values
    encrypted_config = encrypt_config(config)
    
    # Save to file
    with open(config_file, "w") as f:
        json.dump(encrypted_config, f, indent=2)
    
    # Set restrictive permissions
    config_file.chmod(FILE_PERMISSION_OWNER_RW)


def get_config() -> Dict[str, Dict[str, str]]:
    """Get configuration with defaults."""
    import os
    
    config = load_config() or {}
    
    # Set default database configuration
    if 'database' not in config:
        config['database'] = {}
    
    # Allow environment variable overrides for database
    db_env_mapping = {
        'host': 'DB_HOST',
        'port': 'DB_PORT', 
        'database': 'DB_DATABASE',
        'username': 'DB_USERNAME',
        'password': 'DB_PASSWORD'
    }
    
    db_defaults = {
        'host': 'localhost',
        'port': '5432',
        'database': 'azure_metrics',
        'username': 'postgres',
        'password': ''
    }
    
    for config_key, env_key in db_env_mapping.items():
        env_value = os.getenv(env_key)
        if env_value:
            config['database'][config_key] = env_value
        elif config_key not in config['database']:
            config['database'][config_key] = db_defaults[config_key]
    
    return config


def get_azure_credentials(config: Dict[str, Dict[str, str]]) -> Dict[str, str]:
    """Get Azure credentials from configuration."""
    import os
    
    azure_config = config.get('azure', {})
    
    # Allow environment variable overrides
    env_mapping = {
        'subscription_id': 'AZURE_SUBSCRIPTION_ID',
        'tenant_id': 'AZURE_TENANT_ID',
        'client_id': 'AZURE_CLIENT_ID',
        'client_secret': 'AZURE_CLIENT_SECRET'
    }
    
    for config_key, env_key in env_mapping.items():
        env_value = os.getenv(env_key)
        if env_value:
            azure_config[config_key] = env_value
    
    if not azure_config:
        raise ValueError("Azure configuration not found. Please run 'cloud-analyzer configure' first or set environment variables.")
    
    required_fields = ['subscription_id']
    for field in required_fields:
        if field not in azure_config or not azure_config[field]:
            raise ValueError(f"Missing required Azure configuration: {field}")
    
    return azure_config