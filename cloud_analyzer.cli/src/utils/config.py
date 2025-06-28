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