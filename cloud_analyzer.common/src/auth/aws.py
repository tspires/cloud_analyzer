"""AWS authentication provider with SSO support."""

import json
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import boto3
from botocore.exceptions import ClientError

from constants import DEFAULT_AWS_REGION
from models import CloudProvider
from auth.base import AWSCredentials, BrowserAuthProvider


class AWSSSOAuthProvider(BrowserAuthProvider):
    """AWS SSO browser-based authentication provider."""
    
    def __init__(
        self,
        start_url: str,
        region: str = DEFAULT_AWS_REGION,
        port: int = 8080,
        timeout: int = 300
    ) -> None:
        """Initialize AWS SSO auth provider.
        
        Args:
            start_url: AWS SSO start URL
            region: AWS region for SSO
            port: Local port for OAuth callback
            timeout: Timeout in seconds
        """
        super().__init__(CloudProvider.AWS, port, timeout)
        self.start_url = start_url
        self.region = region
        self.sso_oidc_client = boto3.client('sso-oidc', region_name=region)
        self.sso_client = boto3.client('sso', region_name=region)
        self._client_creds = None
        self._device_auth = None
    
    async def get_auth_url(self) -> str:
        """Register client and start device authorization flow."""
        # Register client if not already done
        if not self._client_creds:
            try:
                register_response = self.sso_oidc_client.register_client(
                    clientName='CloudAnalyzer',
                    clientType='public'
                )
                self._client_creds = {
                    'clientId': register_response['clientId'],
                    'clientSecret': register_response['clientSecret']
                }
            except ClientError as e:
                raise Exception(f"Failed to register SSO client: {e}")
        
        # Start device authorization
        try:
            device_auth = self.sso_oidc_client.start_device_authorization(
                clientId=self._client_creds['clientId'],
                clientSecret=self._client_creds['clientSecret'],
                startUrl=self.start_url
            )
            self._device_auth = device_auth
            
            # Return the verification URI
            return device_auth['verificationUriComplete']
            
        except ClientError as e:
            raise Exception(f"Failed to start device authorization: {e}")
    
    async def handle_callback(self, code: str, state: Optional[str] = None) -> AWSCredentials:
        """Handle AWS SSO callback - in this case, poll for device auth completion."""
        if not self._device_auth or not self._client_creds:
            raise Exception("Device authorization not started")
        
        # Poll for token
        import asyncio
        interval = self._device_auth.get('interval', 5)
        
        while True:
            try:
                token_response = self.sso_oidc_client.create_token(
                    clientId=self._client_creds['clientId'],
                    clientSecret=self._client_creds['clientSecret'],
                    grantType='urn:ietf:params:oauth:grant-type:device_code',
                    deviceCode=self._device_auth['deviceCode']
                )
                
                # Success! Get account and role information
                access_token = token_response['accessToken']
                expires_in = token_response.get('expiresIn', 3600)
                
                # List accounts
                accounts = self.sso_client.list_accounts(
                    accessToken=access_token
                )['accountList']
                
                if not accounts:
                    raise Exception("No AWS accounts found for this SSO session")
                
                # For now, use the first account
                # In a real implementation, you might want to let the user choose
                account = accounts[0]
                
                # List roles for the account
                roles = self.sso_client.list_account_roles(
                    accessToken=access_token,
                    accountId=account['accountId']
                )['roleList']
                
                if not roles:
                    raise Exception(f"No roles found for account {account['accountId']}")
                
                # Use the first role (or could let user choose)
                role = roles[0]
                
                # Get role credentials
                role_creds = self.sso_client.get_role_credentials(
                    accessToken=access_token,
                    accountId=account['accountId'],
                    roleName=role['roleName']
                )['roleCredentials']
                
                return AWSCredentials(
                    provider=CloudProvider.AWS,
                    access_key_id=role_creds['accessKeyId'],
                    secret_access_key=role_creds['secretAccessKey'],
                    session_token=role_creds['sessionToken'],
                    region=self.region,
                    expires_at=datetime.fromtimestamp(role_creds['expiration'] / 1000),
                    refresh_token=access_token,
                    metadata={
                        'account_id': account['accountId'],
                        'account_name': account.get('accountName', ''),
                        'role_name': role['roleName'],
                        'sso_session': {
                            'start_url': self.start_url,
                            'region': self.region,
                            'access_token': access_token
                        }
                    }
                )
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'AuthorizationPendingException':
                    # Still waiting for user to authorize
                    await asyncio.sleep(interval)
                    continue
                elif error_code == 'ExpiredTokenException':
                    raise Exception("Device code expired. Please try again.")
                else:
                    raise Exception(f"Token creation failed: {e}")
    
    async def refresh(self, credentials: AWSCredentials) -> AWSCredentials:
        """Refresh AWS SSO credentials."""
        if not credentials.sso_session:
            raise Exception("No SSO session found in credentials")
        
        # In AWS SSO, we need to use the refresh token to get new role credentials
        sso_session = credentials.metadata.get('sso_session', {})
        access_token = sso_session.get('access_token')
        
        if not access_token:
            # Need to re-authenticate
            return await self.authenticate()
        
        try:
            # Get new role credentials
            role_creds = self.sso_client.get_role_credentials(
                accessToken=access_token,
                accountId=credentials.metadata['account_id'],
                roleName=credentials.metadata['role_name']
            )['roleCredentials']
            
            # Update credentials
            credentials.access_key_id = role_creds['accessKeyId']
            credentials.secret_access_key = role_creds['secretAccessKey']
            credentials.session_token = role_creds['sessionToken']
            credentials.expires_at = datetime.fromtimestamp(role_creds['expiration'] / 1000)
            
            return credentials
            
        except ClientError:
            # Access token might be expired, need to re-authenticate
            return await self.authenticate()
    
    async def validate(self, credentials: AWSCredentials) -> bool:
        """Validate AWS credentials."""
        try:
            # Create STS client with credentials
            sts = boto3.client(
                'sts',
                aws_access_key_id=credentials.access_key_id,
                aws_secret_access_key=credentials.secret_access_key,
                aws_session_token=credentials.session_token,
                region_name=credentials.region
            )
            
            # Try to get caller identity
            sts.get_caller_identity()
            return True
            
        except ClientError:
            return False


class AWSProfileAuthProvider(BrowserAuthProvider):
    """AWS authentication using existing AWS CLI profiles."""
    
    def __init__(self, profile: str = "default", region: str = DEFAULT_AWS_REGION) -> None:
        """Initialize AWS profile auth provider.
        
        Args:
            profile: AWS CLI profile name
            region: AWS region
        """
        super().__init__(CloudProvider.AWS)
        self.profile = profile
        self.region = region
    
    async def get_auth_url(self) -> str:
        """Not used for profile auth."""
        raise NotImplementedError("Profile auth doesn't use browser flow")
    
    async def handle_callback(self, code: str, state: Optional[str] = None) -> AWSCredentials:
        """Not used for profile auth."""
        raise NotImplementedError("Profile auth doesn't use browser flow")
    
    async def authenticate(self, **kwargs) -> AWSCredentials:
        """Authenticate using AWS profile."""
        try:
            # Create session with profile
            session = boto3.Session(profile_name=self.profile)
            
            # Get credentials
            creds = session.get_credentials()
            if not creds:
                raise Exception(f"No credentials found for profile '{self.profile}'")
            
            # Get frozen credentials
            frozen_creds = creds.get_frozen_credentials()
            
            return AWSCredentials(
                provider=CloudProvider.AWS,
                access_key_id=frozen_creds.access_key,
                secret_access_key=frozen_creds.secret_key,
                session_token=frozen_creds.token,
                region=self.region or session.region_name or DEFAULT_AWS_REGION,
                profile=self.profile,
                expires_at=None,  # Profile creds don't typically expire
                metadata={
                    'profile': self.profile
                }
            )
            
        except Exception as e:
            raise Exception(f"Failed to load AWS profile '{self.profile}': {e}")
    
    async def refresh(self, credentials: AWSCredentials) -> AWSCredentials:
        """Refresh profile credentials."""
        # Profile credentials are automatically refreshed by boto3
        return await self.authenticate()
    
    async def validate(self, credentials: AWSCredentials) -> bool:
        """Validate AWS credentials."""
        try:
            sts = boto3.client(
                'sts',
                aws_access_key_id=credentials.access_key_id,
                aws_secret_access_key=credentials.secret_access_key,
                aws_session_token=credentials.session_token,
                region_name=credentials.region
            )
            sts.get_caller_identity()
            return True
        except ClientError:
            return False