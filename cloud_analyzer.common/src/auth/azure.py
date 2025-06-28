"""Azure authentication provider with browser support."""

import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from azure.identity import InteractiveBrowserCredential, ClientSecretCredential, AzureCliCredential
from azure.mgmt.resource import SubscriptionClient
from msal import PublicClientApplication

from constants import AUTH_CALLBACK_PORT, DEFAULT_AZURE_REGION
from models import CloudProvider
from auth.base import AzureCredentials, BrowserAuthProvider


class AzureBrowserAuthProvider(BrowserAuthProvider):
    """Azure browser-based authentication provider using MSAL."""
    
    # Azure management scope
    AZURE_MGMT_SCOPE = ["https://management.azure.com/.default"]
    
    def __init__(
        self,
        tenant_id: str = "common",
        port: int = AUTH_CALLBACK_PORT,
        timeout: int = 300
    ) -> None:
        """Initialize Azure browser auth provider.
        
        Args:
            tenant_id: Azure tenant ID or 'common' for multi-tenant
            port: Local port for OAuth callback
            timeout: Timeout in seconds
        """
        super().__init__(CloudProvider.AZURE, port, timeout)
        self.tenant_id = tenant_id
        self._state = None
        self._app = None
        self._subscriptions = []
    
    def _get_app(self) -> PublicClientApplication:
        """Get or create MSAL public client application."""
        if not self._app:
            # Using the Azure CLI client ID (publicly known)
            self._app = PublicClientApplication(
                "04b07795-8ddb-461a-bbee-02f9e1bf7b46",  # Azure CLI client ID
                authority=f"https://login.microsoftonline.com/{self.tenant_id}"
            )
        return self._app
    
    async def get_auth_url(self) -> str:
        """Get Azure authentication URL."""
        app = self._get_app()
        
        # Generate state for CSRF protection
        self._state = secrets.token_urlsafe(32)
        
        # Get auth code flow
        flow = app.initiate_auth_code_flow(
            scopes=self.AZURE_MGMT_SCOPE,
            redirect_uri=self.callback_url,
            state=self._state
        )
        
        if "auth_uri" not in flow:
            raise Exception("Failed to get Azure auth URL")
        
        # Store flow for later
        self._auth_flow = flow
        
        return flow["auth_uri"]
    
    async def handle_callback(self, code: str, state: Optional[str] = None) -> AzureCredentials:
        """Handle Azure OAuth callback."""
        # Verify state
        if state != self._state:
            raise Exception("Invalid state parameter - possible CSRF attack")
        
        if not hasattr(self, '_auth_flow'):
            raise Exception("No auth flow found")
        
        app = self._get_app()
        
        # Complete the flow
        result = app.acquire_token_by_auth_code_flow(
            self._auth_flow,
            {"code": code, "state": state}
        )
        
        if "error" in result:
            raise Exception(f"Azure authentication failed: {result.get('error_description', result['error'])}")
        
        # Get access token and account info
        access_token = result["access_token"]
        expires_in = result.get("expires_in", 3600)
        refresh_token = result.get("refresh_token")
        account = result.get("account", {})
        
        # Get subscription information
        subscription_id = await self._get_subscription_id(access_token)
        
        return AzureCredentials(
            provider=CloudProvider.AZURE,
            tenant_id=account.get("tenant_id", self.tenant_id),
            subscription_id=subscription_id,
            access_token=access_token,
            expires_at=datetime.utcnow() + timedelta(seconds=expires_in),
            refresh_token=refresh_token,
            metadata={
                "account": account,
                "username": account.get("username", ""),
                "name": account.get("name", "")
            }
        )
    
    async def _get_subscription_id(self, access_token: str) -> str:
        """Get the first available subscription ID."""
        # Use the access token to get subscriptions
        from azure.core.credentials import AccessToken
        
        class TokenCredential:
            def __init__(self, token):
                self.token = token
            
            def get_token(self, *scopes, **kwargs):
                return AccessToken(self.token, int(datetime.utcnow().timestamp()) + 3600)
        
        credential = TokenCredential(access_token)
        sub_client = SubscriptionClient(credential)
        
        subscriptions = list(sub_client.subscriptions.list())
        if not subscriptions:
            raise Exception("No Azure subscriptions found")
        
        # Store all subscriptions for future use
        self._subscriptions = [
            {
                "id": sub.subscription_id,
                "name": sub.display_name,
                "state": sub.state
            }
            for sub in subscriptions
        ]
        
        # Return the first active subscription
        for sub in subscriptions:
            if sub.state == "Enabled":
                return sub.subscription_id
        
        # If no enabled subscriptions, return the first one
        return subscriptions[0].subscription_id
    
    async def refresh(self, credentials: AzureCredentials) -> AzureCredentials:
        """Refresh Azure credentials using refresh token."""
        if not credentials.refresh_token:
            # No refresh token, need to re-authenticate
            return await self.authenticate()
        
        app = self._get_app()
        
        # Get accounts in cache
        accounts = app.get_accounts(username=credentials.metadata.get("username"))
        if not accounts:
            # No cached account, need to re-authenticate
            return await self.authenticate()
        
        # Try to acquire token silently
        result = app.acquire_token_silent(
            scopes=self.AZURE_MGMT_SCOPE,
            account=accounts[0]
        )
        
        if not result:
            # Silent acquisition failed, try with refresh token
            result = app.acquire_token_by_refresh_token(
                credentials.refresh_token,
                scopes=self.AZURE_MGMT_SCOPE
            )
        
        if "error" in result:
            # Refresh failed, need to re-authenticate
            return await self.authenticate()
        
        # Update credentials
        credentials.access_token = result["access_token"]
        credentials.expires_at = datetime.utcnow() + timedelta(seconds=result.get("expires_in", 3600))
        credentials.refresh_token = result.get("refresh_token", credentials.refresh_token)
        
        return credentials
    
    async def validate(self, credentials: AzureCredentials) -> bool:
        """Validate Azure credentials."""
        if credentials.is_expired:
            return False
        
        try:
            # Try to use the token to list subscriptions
            from azure.core.credentials import AccessToken
            
            class TokenCredential:
                def __init__(self, token):
                    self.token = token
                
                def get_token(self, *scopes, **kwargs):
                    return AccessToken(self.token, int(datetime.utcnow().timestamp()) + 3600)
            
            credential = TokenCredential(credentials.access_token)
            sub_client = SubscriptionClient(credential)
            
            # Try to get at least one subscription
            next(sub_client.subscriptions.list())
            return True
            
        except Exception:
            return False


class AzureServicePrincipalAuthProvider(BrowserAuthProvider):
    """Azure authentication using service principal (client credentials)."""
    
    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        client_secret: str,
        subscription_id: str
    ) -> None:
        """Initialize Azure service principal auth provider.
        
        Args:
            tenant_id: Azure tenant ID
            client_id: Service principal client ID
            client_secret: Service principal client secret
            subscription_id: Azure subscription ID
        """
        super().__init__(CloudProvider.AZURE)
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.subscription_id = subscription_id
    
    async def get_auth_url(self) -> str:
        """Not used for service principal auth."""
        raise NotImplementedError("Service principal auth doesn't use browser flow")
    
    async def handle_callback(self, code: str, state: Optional[str] = None) -> AzureCredentials:
        """Not used for service principal auth."""
        raise NotImplementedError("Service principal auth doesn't use browser flow")
    
    async def authenticate(self, **kwargs) -> AzureCredentials:
        """Authenticate using service principal."""
        try:
            # Create credential object
            credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            
            # Get access token
            token = credential.get_token("https://management.azure.com/.default")
            
            return AzureCredentials(
                provider=CloudProvider.AZURE,
                tenant_id=self.tenant_id,
                subscription_id=self.subscription_id,
                access_token=token.token,
                client_id=self.client_id,
                client_secret=self.client_secret,
                expires_at=datetime.fromtimestamp(token.expires_on),
                metadata={
                    "auth_type": "service_principal"
                }
            )
            
        except Exception as e:
            raise Exception(f"Service principal authentication failed: {e}")
    
    async def refresh(self, credentials: AzureCredentials) -> AzureCredentials:
        """Refresh service principal credentials."""
        # Service principal credentials are refreshed by getting a new token
        return await self.authenticate()
    
    async def validate(self, credentials: AzureCredentials) -> bool:
        """Validate Azure credentials."""
        if credentials.is_expired:
            return False
        
        try:
            from azure.core.credentials import AccessToken
            
            class TokenCredential:
                def __init__(self, token):
                    self.token = token
                
                def get_token(self, *scopes, **kwargs):
                    return AccessToken(self.token, int(datetime.utcnow().timestamp()) + 3600)
            
            credential = TokenCredential(credentials.access_token)
            sub_client = SubscriptionClient(credential)
            
            # Try to get the subscription
            sub = sub_client.subscriptions.get(credentials.subscription_id)
            return sub is not None
            
        except Exception:
            return False


class AzureCliAuthProvider(BrowserAuthProvider):
    """Azure authentication using Azure CLI."""
    
    def __init__(self, subscription_id: Optional[str] = None) -> None:
        """Initialize Azure CLI auth provider.
        
        Args:
            subscription_id: Optional Azure subscription ID to use
        """
        super().__init__(CloudProvider.AZURE)
        self.subscription_id = subscription_id
        self._credential = None
    
    async def get_auth_url(self) -> str:
        """Not used for Azure CLI auth."""
        raise NotImplementedError("Azure CLI auth doesn't use browser flow")
    
    async def handle_callback(self, code: str, state: Optional[str] = None) -> AzureCredentials:
        """Not used for Azure CLI auth."""
        raise NotImplementedError("Azure CLI auth doesn't use browser flow")
    
    async def authenticate(self, **kwargs) -> AzureCredentials:
        """Authenticate using Azure CLI."""
        try:
            # Create Azure CLI credential
            self._credential = AzureCliCredential()
            
            # Get access token
            token = self._credential.get_token("https://management.azure.com/.default")
            
            # Get subscription if not provided
            if not self.subscription_id:
                sub_client = SubscriptionClient(self._credential)
                subscriptions = list(sub_client.subscriptions.list())
                
                if not subscriptions:
                    raise Exception("No Azure subscriptions found")
                
                # Find the first enabled subscription
                for sub in subscriptions:
                    if sub.state == "Enabled":
                        self.subscription_id = sub.subscription_id
                        break
                
                if not self.subscription_id:
                    self.subscription_id = subscriptions[0].subscription_id
            
            # Get tenant ID from subscription
            sub_client = SubscriptionClient(self._credential)
            subscription = sub_client.subscriptions.get(self.subscription_id)
            tenant_id = subscription.tenant_id
            
            return AzureCredentials(
                provider=CloudProvider.AZURE,
                tenant_id=tenant_id,
                subscription_id=self.subscription_id,
                access_token=token.token,
                expires_at=datetime.fromtimestamp(token.expires_on),
                metadata={
                    "auth_type": "azure_cli",
                    "subscription_name": subscription.display_name
                }
            )
            
        except Exception as e:
            raise Exception(f"Azure CLI authentication failed: {e}. Make sure you have logged in with 'az login'")
    
    async def refresh(self, credentials: AzureCredentials) -> AzureCredentials:
        """Refresh Azure CLI credentials."""
        # Azure CLI handles token refresh automatically
        return await self.authenticate()
    
    async def validate(self, credentials: AzureCredentials) -> bool:
        """Validate Azure credentials."""
        if credentials.is_expired:
            return False
        
        try:
            # Try to use the token to list subscriptions
            from azure.core.credentials import AccessToken
            
            class TokenCredential:
                def __init__(self, token):
                    self.token = token
                
                def get_token(self, *scopes, **kwargs):
                    return AccessToken(self.token, int(datetime.utcnow().timestamp()) + 3600)
            
            credential = TokenCredential(credentials.access_token)
            sub_client = SubscriptionClient(credential)
            
            # Try to get the subscription
            sub = sub_client.subscriptions.get(credentials.subscription_id)
            return sub is not None
            
        except Exception:
            return False