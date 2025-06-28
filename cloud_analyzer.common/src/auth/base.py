"""Base authentication interfaces."""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from models import CloudProvider


class Credentials(BaseModel):
    """Base credentials model."""
    
    provider: CloudProvider = Field(..., description="Cloud provider")
    expires_at: Optional[datetime] = Field(None, description="Token expiration time")
    refresh_token: Optional[str] = Field(None, description="Refresh token if available")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @property
    def is_expired(self) -> bool:
        """Check if credentials are expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    @property
    def expires_in_minutes(self) -> Optional[int]:
        """Get minutes until expiration."""
        if not self.expires_at:
            return None
        delta = self.expires_at - datetime.utcnow()
        return int(delta.total_seconds() / 60)


class AWSCredentials(Credentials):
    """AWS-specific credentials."""
    
    access_key_id: Optional[str] = Field(None, description="AWS Access Key ID")
    secret_access_key: Optional[str] = Field(None, description="AWS Secret Access Key")
    session_token: Optional[str] = Field(None, description="AWS Session Token")
    region: str = Field("us-east-1", description="Default AWS region")
    profile: Optional[str] = Field(None, description="AWS profile name")
    sso_session: Optional[Dict[str, Any]] = Field(None, description="SSO session data")


class AzureCredentials(Credentials):
    """Azure-specific credentials."""
    
    tenant_id: str = Field(..., description="Azure Tenant ID")
    subscription_id: str = Field(..., description="Azure Subscription ID")
    access_token: Optional[str] = Field(None, description="Azure access token")
    client_id: Optional[str] = Field(None, description="Azure Client ID")
    client_secret: Optional[str] = Field(None, description="Azure Client Secret")


class GCPCredentials(Credentials):
    """GCP-specific credentials."""
    
    project_id: str = Field(..., description="GCP Project ID")
    access_token: Optional[str] = Field(None, description="GCP access token")
    service_account_key: Optional[Dict[str, Any]] = Field(None, description="Service account key")
    credentials_path: Optional[str] = Field(None, description="Path to credentials file")


class AuthProvider(ABC):
    """Abstract authentication provider interface."""
    
    def __init__(self, provider: CloudProvider) -> None:
        """Initialize auth provider.
        
        Args:
            provider: Cloud provider type
        """
        self.provider = provider
    
    @abstractmethod
    async def authenticate(self, **kwargs) -> Credentials:
        """Authenticate and return credentials.
        
        Args:
            **kwargs: Provider-specific authentication parameters
            
        Returns:
            Provider-specific credentials
        """
        pass
    
    @abstractmethod
    async def refresh(self, credentials: Credentials) -> Credentials:
        """Refresh expired credentials.
        
        Args:
            credentials: Current credentials
            
        Returns:
            Refreshed credentials
        """
        pass
    
    @abstractmethod
    async def validate(self, credentials: Credentials) -> bool:
        """Validate credentials are still valid.
        
        Args:
            credentials: Credentials to validate
            
        Returns:
            True if credentials are valid
        """
        pass


class BrowserAuthProvider(AuthProvider):
    """Authentication provider that uses browser-based flow."""
    
    def __init__(
        self, 
        provider: CloudProvider,
        port: int = 8080,
        timeout: int = 300
    ) -> None:
        """Initialize browser auth provider.
        
        Args:
            provider: Cloud provider type
            port: Local port for OAuth callback
            timeout: Timeout in seconds for auth flow
        """
        super().__init__(provider)
        self.port = port
        self.timeout = timeout
        self.callback_url = f"http://localhost:{port}/callback"
    
    @abstractmethod
    async def get_auth_url(self) -> str:
        """Get the authentication URL to open in browser.
        
        Returns:
            URL to open in browser
        """
        pass
    
    @abstractmethod
    async def handle_callback(self, code: str, state: Optional[str] = None) -> Credentials:
        """Handle OAuth callback.
        
        Args:
            code: Authorization code from callback
            state: State parameter from callback
            
        Returns:
            Credentials from successful authentication
        """
        pass
    
    async def start_local_server(self) -> asyncio.Queue:
        """Start local server to handle OAuth callback.
        
        Returns:
            Queue to receive callback parameters
        """
        from aiohttp import web
        
        callback_queue = asyncio.Queue()
        
        async def handle_callback(request):
            """Handle OAuth callback request."""
            code = request.query.get('code')
            state = request.query.get('state')
            error = request.query.get('error')
            
            if error:
                await callback_queue.put({"error": error})
                return web.Response(
                    text="Authentication failed. You can close this window.",
                    content_type="text/html"
                )
            
            if code:
                await callback_queue.put({"code": code, "state": state})
                return web.Response(
                    text="Authentication successful! You can close this window.",
                    content_type="text/html"
                )
            
            return web.Response(
                text="Invalid callback parameters.",
                status=400
            )
        
        app = web.Application()
        app.router.add_get('/callback', handle_callback)
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', self.port)
        await site.start()
        
        # Store runner for cleanup
        self._runner = runner
        
        return callback_queue
    
    async def stop_local_server(self) -> None:
        """Stop the local OAuth server."""
        if hasattr(self, '_runner'):
            await self._runner.cleanup()
    
    async def authenticate(self, **kwargs) -> Credentials:
        """Perform browser-based authentication.
        
        Returns:
            Credentials from successful authentication
        """
        import webbrowser
        
        # Start local server
        callback_queue = await self.start_local_server()
        
        try:
            # Get auth URL and open in browser
            auth_url = await self.get_auth_url()
            webbrowser.open(auth_url)
            
            # Wait for callback
            try:
                callback_data = await asyncio.wait_for(
                    callback_queue.get(),
                    timeout=self.timeout
                )
            except asyncio.TimeoutError:
                raise Exception(f"Authentication timeout after {self.timeout} seconds")
            
            if "error" in callback_data:
                raise Exception(f"Authentication error: {callback_data['error']}")
            
            # Handle the callback
            return await self.handle_callback(
                callback_data["code"],
                callback_data.get("state")
            )
            
        finally:
            # Always stop the server
            await self.stop_local_server()