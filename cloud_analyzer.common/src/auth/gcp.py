"""GCP authentication provider with browser support."""

import json
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as GoogleCredentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from constants import AUTH_CALLBACK_PORT, DEFAULT_GCP_REGION
from models import CloudProvider
from auth.base import BrowserAuthProvider, GCPCredentials


class GCPBrowserAuthProvider(BrowserAuthProvider):
    """GCP browser-based authentication provider using OAuth 2.0."""
    
    # GCP OAuth scopes
    GCP_SCOPES = [
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-billing",
        "https://www.googleapis.com/auth/compute"
    ]
    
    # Client configuration for installed apps
    CLIENT_CONFIG = {
        "installed": {
            "client_id": "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com",
            "client_secret": "d-FL95Q19q7MQmFpd7hHD0Ty",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
        }
    }
    
    def __init__(
        self,
        project_id: Optional[str] = None,
        port: int = AUTH_CALLBACK_PORT,
        timeout: int = 300
    ) -> None:
        """Initialize GCP browser auth provider.
        
        Args:
            project_id: Default GCP project ID
            port: Local port for OAuth callback
            timeout: Timeout in seconds
        """
        super().__init__(CloudProvider.GCP, port, timeout)
        self.project_id = project_id
        self._flow = None
        self._state = None
    
    def _get_flow(self) -> Flow:
        """Get or create OAuth flow."""
        if not self._flow:
            self._flow = Flow.from_client_config(
                self.CLIENT_CONFIG,
                scopes=self.GCP_SCOPES,
                redirect_uri=self.callback_url
            )
        return self._flow
    
    async def get_auth_url(self) -> str:
        """Get GCP authentication URL."""
        flow = self._get_flow()
        
        # Generate state for CSRF protection
        self._state = secrets.token_urlsafe(32)
        
        # Get authorization URL
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=self._state,
            prompt='consent'
        )
        
        return auth_url
    
    async def handle_callback(self, code: str, state: Optional[str] = None) -> GCPCredentials:
        """Handle GCP OAuth callback."""
        # Verify state
        if state != self._state:
            raise Exception("Invalid state parameter - possible CSRF attack")
        
        flow = self._get_flow()
        
        # Exchange code for tokens
        try:
            flow.fetch_token(code=code)
        except Exception as e:
            raise Exception(f"Failed to exchange authorization code: {e}")
        
        # Get credentials
        credentials = flow.credentials
        
        # Get project ID if not provided
        if not self.project_id:
            self.project_id = await self._get_default_project(credentials)
        
        # Get user info
        user_info = await self._get_user_info(credentials)
        
        return GCPCredentials(
            provider=CloudProvider.GCP,
            project_id=self.project_id,
            access_token=credentials.token,
            expires_at=credentials.expiry,
            refresh_token=credentials.refresh_token,
            metadata={
                "scopes": credentials.scopes,
                "email": user_info.get("email", ""),
                "name": user_info.get("name", ""),
                "client_id": self.CLIENT_CONFIG["installed"]["client_id"],
                "client_secret": self.CLIENT_CONFIG["installed"]["client_secret"],
                "token_uri": credentials.token_uri
            }
        )
    
    async def _get_default_project(self, credentials: GoogleCredentials) -> str:
        """Get the default project ID from available projects."""
        try:
            # Build the resource manager service
            service = build('cloudresourcemanager', 'v1', credentials=credentials)
            
            # List projects
            result = service.projects().list().execute()
            projects = result.get('projects', [])
            
            if not projects:
                raise Exception("No GCP projects found")
            
            # Look for an active project
            for project in projects:
                if project.get('lifecycleState') == 'ACTIVE':
                    return project['projectId']
            
            # If no active project, return the first one
            return projects[0]['projectId']
            
        except Exception as e:
            raise Exception(f"Failed to get GCP projects: {e}")
    
    async def _get_user_info(self, credentials: GoogleCredentials) -> Dict[str, Any]:
        """Get user information from OAuth token."""
        try:
            # Build the OAuth2 service
            service = build('oauth2', 'v2', credentials=credentials)
            
            # Get user info
            user_info = service.userinfo().get().execute()
            return user_info
            
        except Exception:
            # User info is optional, return empty dict if it fails
            return {}
    
    async def refresh(self, credentials: GCPCredentials) -> GCPCredentials:
        """Refresh GCP credentials using refresh token."""
        if not credentials.refresh_token:
            # No refresh token, need to re-authenticate
            return await self.authenticate()
        
        try:
            # Recreate Google credentials object
            google_creds = GoogleCredentials(
                token=credentials.access_token,
                refresh_token=credentials.refresh_token,
                token_uri=credentials.metadata.get("token_uri", "https://oauth2.googleapis.com/token"),
                client_id=credentials.metadata.get("client_id"),
                client_secret=credentials.metadata.get("client_secret"),
                scopes=credentials.metadata.get("scopes", self.GCP_SCOPES)
            )
            
            # Refresh the token
            google_creds.refresh(Request())
            
            # Update credentials
            credentials.access_token = google_creds.token
            credentials.expires_at = google_creds.expiry
            
            return credentials
            
        except Exception:
            # Refresh failed, need to re-authenticate
            return await self.authenticate()
    
    async def validate(self, credentials: GCPCredentials) -> bool:
        """Validate GCP credentials."""
        if credentials.is_expired:
            return False
        
        try:
            # Create Google credentials object
            google_creds = GoogleCredentials(
                token=credentials.access_token,
                token_uri="https://oauth2.googleapis.com/token"
            )
            
            # Try to list projects
            service = build('cloudresourcemanager', 'v1', credentials=google_creds)
            service.projects().list(pageSize=1).execute()
            return True
            
        except Exception:
            return False


class GCPServiceAccountAuthProvider(BrowserAuthProvider):
    """GCP authentication using service account key file."""
    
    def __init__(
        self,
        key_file_path: str,
        project_id: Optional[str] = None
    ) -> None:
        """Initialize GCP service account auth provider.
        
        Args:
            key_file_path: Path to service account JSON key file
            project_id: GCP project ID (will use from key file if not provided)
        """
        super().__init__(CloudProvider.GCP)
        self.key_file_path = key_file_path
        self.project_id = project_id
        self._key_data = None
    
    async def get_auth_url(self) -> str:
        """Not used for service account auth."""
        raise NotImplementedError("Service account auth doesn't use browser flow")
    
    async def handle_callback(self, code: str, state: Optional[str] = None) -> GCPCredentials:
        """Not used for service account auth."""
        raise NotImplementedError("Service account auth doesn't use browser flow")
    
    async def authenticate(self, **kwargs) -> GCPCredentials:
        """Authenticate using service account key file."""
        try:
            # Load key file
            with open(self.key_file_path, 'r') as f:
                self._key_data = json.load(f)
            
            # Extract project ID if not provided
            if not self.project_id:
                self.project_id = self._key_data.get('project_id')
                if not self.project_id:
                    raise Exception("No project_id found in service account key file")
            
            # Create credentials from service account
            from google.oauth2 import service_account
            
            credentials = service_account.Credentials.from_service_account_info(
                self._key_data,
                scopes=GCPBrowserAuthProvider.GCP_SCOPES
            )
            
            # Get access token
            credentials.refresh(Request())
            
            return GCPCredentials(
                provider=CloudProvider.GCP,
                project_id=self.project_id,
                access_token=credentials.token,
                service_account_key=self._key_data,
                credentials_path=self.key_file_path,
                expires_at=credentials.expiry,
                metadata={
                    "type": "service_account",
                    "service_account_email": self._key_data.get("client_email", ""),
                    "private_key_id": self._key_data.get("private_key_id", "")
                }
            )
            
        except FileNotFoundError:
            raise Exception(f"Service account key file not found: {self.key_file_path}")
        except json.JSONDecodeError:
            raise Exception(f"Invalid service account key file: {self.key_file_path}")
        except Exception as e:
            raise Exception(f"Service account authentication failed: {e}")
    
    async def refresh(self, credentials: GCPCredentials) -> GCPCredentials:
        """Refresh service account credentials."""
        # Service account credentials are refreshed by getting a new token
        return await self.authenticate()
    
    async def validate(self, credentials: GCPCredentials) -> bool:
        """Validate GCP credentials."""
        if credentials.is_expired:
            return False
        
        try:
            from google.oauth2 import service_account
            from google.auth.transport.requests import Request
            
            # Recreate credentials
            google_creds = service_account.Credentials.from_service_account_info(
                credentials.service_account_key,
                scopes=GCPBrowserAuthProvider.GCP_SCOPES
            )
            google_creds.token = credentials.access_token
            
            # Try to list projects
            service = build('cloudresourcemanager', 'v1', credentials=google_creds)
            service.projects().get(projectId=credentials.project_id).execute()
            return True
            
        except Exception:
            return False