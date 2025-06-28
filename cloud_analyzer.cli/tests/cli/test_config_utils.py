"""Tests for configuration utility functions."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from cryptography.fernet import Fernet

from utils.config import (
    decrypt_config,
    encrypt_config,
    get_config_dir,
    get_config_file,
    get_key_file,
    get_or_create_key,
    load_config,
    save_config,
)
from constants import FILE_PERMISSION_OWNER_RW


class TestConfigPaths:
    """Test configuration path functions."""
    
    def test_get_config_dir(self):
        """Test getting config directory."""
        with patch("pathlib.Path.home") as mock_home:
            mock_home.return_value = Path("/home/user")
            config_dir = get_config_dir()
            assert config_dir == Path("/home/user/.cloud-analyzer")
    
    def test_get_config_file(self):
        """Test getting config file path."""
        with patch("utils.config.get_config_dir") as mock_dir:
            mock_dir.return_value = Path("/home/user/.cloud-analyzer")
            config_file = get_config_file()
            assert config_file == Path("/home/user/.cloud-analyzer/config.json")
    
    def test_get_key_file(self):
        """Test getting key file path."""
        with patch("utils.config.get_config_dir") as mock_dir:
            mock_dir.return_value = Path("/home/user/.cloud-analyzer")
            key_file = get_key_file()
            assert key_file == Path("/home/user/.cloud-analyzer/.key")


class TestEncryption:
    """Test encryption functions."""
    
    def test_get_or_create_key_existing(self, tmp_path):
        """Test getting existing encryption key."""
        key_file = tmp_path / ".key"
        test_key = Fernet.generate_key()
        key_file.write_bytes(test_key)
        
        with patch("utils.config.get_key_file") as mock_key_file:
            mock_key_file.return_value = key_file
            key = get_or_create_key()
            assert key == test_key
    
    def test_get_or_create_key_new(self, tmp_path):
        """Test creating new encryption key."""
        key_file = tmp_path / ".key"
        
        with patch("utils.config.get_key_file") as mock_key_file:
            mock_key_file.return_value = key_file
            key = get_or_create_key()
            
            assert key_file.exists()
            assert len(key) > 0
            # Check permissions
            assert oct(key_file.stat().st_mode)[-3:] == oct(FILE_PERMISSION_OWNER_RW)[-3:]
    
    def test_encrypt_config(self):
        """Test config encryption."""
        config = {
            "aws": {
                "profile": "default",
                "secret_access_key": "my-secret-key"
            },
            "azure": {
                "client_id": "client-123",
                "client_secret": "azure-secret"
            }
        }
        
        with patch("utils.config.get_or_create_key") as mock_key:
            mock_key.return_value = Fernet.generate_key()
            encrypted = encrypt_config(config)
            
            # Non-sensitive values should remain unchanged
            assert encrypted["aws"]["profile"] == "default"
            
            # Sensitive values should be encrypted
            assert isinstance(encrypted["aws"]["secret_access_key"], dict)
            assert encrypted["aws"]["secret_access_key"]["encrypted"] is True
            assert "value" in encrypted["aws"]["secret_access_key"]
            
            assert isinstance(encrypted["azure"]["client_secret"], dict)
            assert encrypted["azure"]["client_secret"]["encrypted"] is True
    
    def test_decrypt_config(self):
        """Test config decryption."""
        key = Fernet.generate_key()
        fernet = Fernet(key)
        
        encrypted_config = {
            "aws": {
                "profile": "default",
                "secret_access_key": {
                    "encrypted": True,
                    "value": fernet.encrypt(b"my-secret-key").decode()
                }
            }
        }
        
        with patch("utils.config.get_or_create_key") as mock_key:
            mock_key.return_value = key
            decrypted = decrypt_config(encrypted_config)
            
            assert decrypted["aws"]["profile"] == "default"
            assert decrypted["aws"]["secret_access_key"] == "my-secret-key"
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test encryption and decryption roundtrip."""
        original_config = {
            "aws": {
                "access_key_id": "AKIAIOSFODNN7EXAMPLE",
                "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
            },
            "azure": {
                "client_secret": "azure-secret-123",
                "tenant_id": "tenant-123"
            }
        }
        
        with patch("utils.config.get_or_create_key") as mock_key:
            test_key = Fernet.generate_key()
            mock_key.return_value = test_key
            
            encrypted = encrypt_config(original_config)
            decrypted = decrypt_config(encrypted)
            
            assert decrypted == original_config


class TestConfigLoadSave:
    """Test config loading and saving."""
    
    def test_load_config_not_exists(self, tmp_path):
        """Test loading config when file doesn't exist."""
        config_file = tmp_path / "config.json"
        
        with patch("utils.config.get_config_file") as mock_file:
            mock_file.return_value = config_file
            config = load_config()
            assert config is None
    
    def test_load_config_success(self, tmp_path):
        """Test successful config loading."""
        config_file = tmp_path / "config.json"
        test_config = {"aws": {"profile": "default"}}
        config_file.write_text(json.dumps(test_config))
        
        with patch("utils.config.get_config_file") as mock_file:
            with patch("utils.config.decrypt_config") as mock_decrypt:
                mock_file.return_value = config_file
                mock_decrypt.return_value = test_config
                
                config = load_config()
                assert config == test_config
    
    def test_load_config_invalid_json(self, tmp_path):
        """Test loading config with invalid JSON."""
        config_file = tmp_path / "config.json"
        config_file.write_text("invalid json")
        
        with patch("utils.config.get_config_file") as mock_file:
            mock_file.return_value = config_file
            config = load_config()
            assert config is None
    
    def test_save_config(self, tmp_path):
        """Test saving configuration."""
        config_file = tmp_path / "config.json"
        test_config = {"aws": {"profile": "default"}}
        
        with patch("utils.config.get_config_file") as mock_file:
            with patch("utils.config.encrypt_config") as mock_encrypt:
                mock_file.return_value = config_file
                mock_encrypt.return_value = test_config
                
                save_config(test_config)
                
                assert config_file.exists()
                # Check permissions
                assert oct(config_file.stat().st_mode)[-3:] == oct(FILE_PERMISSION_OWNER_RW)[-3:]
                
                # Verify content
                saved_data = json.loads(config_file.read_text())
                assert saved_data == test_config