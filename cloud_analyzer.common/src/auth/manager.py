"""Authentication manager for handling credential storage and retrieval."""

import json
import os
from pathlib import Path
from typing import Dict, Optional, Type, Union

from cryptography.fernet import Fernet

from constants import FILE_PERMISSION_OWNER_RW
from models import CloudProvider
from auth.aws import AWSSSOAuthProvider, AWSProfileAuthProvider
from auth.azure import AzureBrowserAuthProvider, AzureServicePrincipalAuthProvider, AzureCliAuthProvider
from auth.base import AuthProvider, AWSCredentials, AzureCredentials, GCPCredentials, Credentials
from auth.gcp import GCPBrowserAuthProvider, GCPServiceAccountAuthProvider


CredentialsType = Union[AWSCredentials, AzureCredentials, GCPCredentials]


class AuthManager:
    """Manages authentication credentials for multiple cloud providers."""
    
    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """Initialize auth manager.
        
        Args:
            config_dir: Directory for storing credentials (defaults to ~/.cloud_analyzer)
        """
        self.config_dir = config_dir or Path.home() / ".cloud_analyzer"
        self.config_dir.mkdir(exist_ok=True)
        self.creds_file = self.config_dir / "credentials.json"
        self.key_file = self.config_dir / ".key"
        self._cipher = self._get_or_create_cipher()
        self._providers: Dict[CloudProvider, AuthProvider] = {}
    
    def _get_or_create_cipher(self) -> Fernet:
        """Get or create encryption cipher for credentials."""
        if self.key_file.exists():
            key = self.key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            os.chmod(self.key_file, FILE_PERMISSION_OWNER_RW)
        
        return Fernet(key)
    
    def register_provider(self, provider: AuthProvider) -> None:
        """Register an authentication provider.
        
        Args:
            provider: Authentication provider instance
        """
        self._providers[provider.provider] = provider
    
    def get_provider(self, provider: CloudProvider) -> Optional[AuthProvider]:
        """Get registered provider for cloud provider.
        
        Args:
            provider: Cloud provider type
            
        Returns:
            Authentication provider if registered
        """
        return self._providers.get(provider)
    
    async def authenticate(
        self,
        provider: CloudProvider,
        auth_type: str = "browser",
        **kwargs
    ) -> CredentialsType:
        """Authenticate with a cloud provider.
        
        Args:
            provider: Cloud provider to authenticate with
            auth_type: Type of authentication (browser, profile, service_principal, etc.)
            **kwargs: Provider-specific authentication parameters
            
        Returns:
            Provider-specific credentials
        """
        # Create appropriate auth provider
        auth_provider = self._create_auth_provider(provider, auth_type, **kwargs)
        
        # Register the provider
        self.register_provider(auth_provider)
        
        # Authenticate
        credentials = await auth_provider.authenticate(**kwargs)
        
        # Save credentials
        await self.save_credentials(credentials)
        
        return credentials
    
    def _create_auth_provider(
        self,
        provider: CloudProvider,
        auth_type: str,
        **kwargs
    ) -> AuthProvider:
        """Create authentication provider based on type.
        
        Args:
            provider: Cloud provider
            auth_type: Authentication type
            **kwargs: Provider-specific parameters
            
        Returns:
            Authentication provider instance
        """
        if provider == CloudProvider.AWS:
            if auth_type == "sso":
                return AWSSSOAuthProvider(
                    start_url=kwargs.get("start_url"),
                    region=kwargs.get("region")
                )
            elif auth_type == "profile":
                return AWSProfileAuthProvider(
                    profile=kwargs.get("profile", "default"),
                    region=kwargs.get("region")
                )
            else:
                raise ValueError(f"Unknown AWS auth type: {auth_type}")
        
        elif provider == CloudProvider.AZURE:
            if auth_type == "browser":
                return AzureBrowserAuthProvider(
                    tenant_id=kwargs.get("tenant_id", "common")
                )
            elif auth_type == "service_principal":
                return AzureServicePrincipalAuthProvider(
                    tenant_id=kwargs["tenant_id"],
                    client_id=kwargs["client_id"],
                    client_secret=kwargs["client_secret"],
                    subscription_id=kwargs["subscription_id"]
                )
            elif auth_type == "cli":
                return AzureCliAuthProvider(
                    subscription_id=kwargs.get("subscription_id")
                )
            else:
                raise ValueError(f"Unknown Azure auth type: {auth_type}")
        
        elif provider == CloudProvider.GCP:
            if auth_type == "browser":
                return GCPBrowserAuthProvider(
                    project_id=kwargs.get("project_id")
                )
            elif auth_type == "service_account":
                return GCPServiceAccountAuthProvider(
                    key_file_path=kwargs["key_file_path"],
                    project_id=kwargs.get("project_id")
                )
            else:
                raise ValueError(f"Unknown GCP auth type: {auth_type}")
        
        else:
            raise ValueError(f"Unknown cloud provider: {provider}")
    
    async def load_credentials(
        self,
        provider: CloudProvider
    ) -> Optional[CredentialsType]:
        """Load saved credentials for a provider.
        
        Args:
            provider: Cloud provider
            
        Returns:
            Credentials if found and valid
        """
        if not self.creds_file.exists():
            return None
        
        try:
            # Read encrypted credentials
            encrypted_data = self.creds_file.read_bytes()
            decrypted_data = self._cipher.decrypt(encrypted_data)
            all_creds = json.loads(decrypted_data.decode())
            
            # Get provider credentials
            provider_data = all_creds.get(provider.value)
            if not provider_data:
                return None
            
            # Create appropriate credentials object
            if provider == CloudProvider.AWS:
                credentials = AWSCredentials(**provider_data)
            elif provider == CloudProvider.AZURE:
                credentials = AzureCredentials(**provider_data)
            elif provider == CloudProvider.GCP:
                credentials = GCPCredentials(**provider_data)
            else:
                return None
            
            # Validate credentials
            auth_provider = self.get_provider(provider)
            if auth_provider and await auth_provider.validate(credentials):
                # Refresh if needed
                if credentials.is_expired and credentials.refresh_token:
                    credentials = await auth_provider.refresh(credentials)
                    await self.save_credentials(credentials)
                
                return credentials
            
            return None
            
        except Exception:
            # If anything goes wrong, return None
            return None
    
    async def save_credentials(self, credentials: CredentialsType) -> None:
        """Save credentials securely.
        
        Args:
            credentials: Credentials to save
        """
        # Load existing credentials
        all_creds = {}
        if self.creds_file.exists():
            try:
                encrypted_data = self.creds_file.read_bytes()
                decrypted_data = self._cipher.decrypt(encrypted_data)
                all_creds = json.loads(decrypted_data.decode())
            except Exception:
                # If decryption fails, start fresh
                pass
        
        # Update with new credentials
        all_creds[credentials.provider.value] = credentials.model_dump(mode='json')
        
        # Encrypt and save
        data = json.dumps(all_creds).encode()
        encrypted_data = self._cipher.encrypt(data)
        self.creds_file.write_bytes(encrypted_data)
        os.chmod(self.creds_file, FILE_PERMISSION_OWNER_RW)
    
    async def remove_credentials(self, provider: CloudProvider) -> None:
        """Remove saved credentials for a provider.
        
        Args:
            provider: Cloud provider
        """
        if not self.creds_file.exists():
            return
        
        try:
            # Load existing credentials
            encrypted_data = self.creds_file.read_bytes()
            decrypted_data = self._cipher.decrypt(encrypted_data)
            all_creds = json.loads(decrypted_data.decode())
            
            # Remove provider credentials
            all_creds.pop(provider.value, None)
            
            if all_creds:
                # Save remaining credentials
                data = json.dumps(all_creds).encode()
                encrypted_data = self._cipher.encrypt(data)
                self.creds_file.write_bytes(encrypted_data)
                os.chmod(self.creds_file, FILE_PERMISSION_OWNER_RW)
            else:
                # No credentials left, remove file
                self.creds_file.unlink()
                
        except Exception:
            # If anything goes wrong, just ignore
            pass
    
    def list_providers(self) -> Dict[CloudProvider, str]:
        """List all configured providers.
        
        Returns:
            Dictionary of provider to status
        """
        status = {}
        
        if self.creds_file.exists():
            try:
                encrypted_data = self.creds_file.read_bytes()
                decrypted_data = self._cipher.decrypt(encrypted_data)
                all_creds = json.loads(decrypted_data.decode())
                
                for provider_str in all_creds:
                    try:
                        provider = CloudProvider(provider_str)
                        status[provider] = "configured"
                    except ValueError:
                        continue
                        
            except Exception:
                pass
        
        # Add unconfigured providers
        for provider in CloudProvider:
            if provider not in status:
                status[provider] = "not configured"
        
        return status