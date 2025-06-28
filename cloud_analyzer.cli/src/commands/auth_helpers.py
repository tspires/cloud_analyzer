"""Helper functions for auth status command."""

from typing import Optional, Tuple

from auth import AuthManager
from auth.aws import AWSProfileAuthProvider, AWSSSOAuthProvider
from auth.azure import AzureBrowserAuthProvider, AzureServicePrincipalAuthProvider
from auth.gcp import GCPBrowserAuthProvider, GCPServiceAccountAuthProvider
from auth.base import AuthProvider, Credentials
from models import CloudProvider


def create_aws_provider(creds: Credentials) -> Optional[AuthProvider]:
    """Create AWS auth provider from credentials."""
    if creds.profile:
        return AWSProfileAuthProvider(
            profile=creds.profile,
            region=creds.region
        )
    elif creds.metadata.get("sso_session"):
        sso_data = creds.metadata["sso_session"]
        return AWSSSOAuthProvider(
            start_url=sso_data["start_url"],
            region=sso_data["region"]
        )
    return None


def create_azure_provider(creds: Credentials) -> Optional[AuthProvider]:
    """Create Azure auth provider from credentials."""
    if creds.client_id and creds.client_secret:
        return AzureServicePrincipalAuthProvider(
            tenant_id=creds.tenant_id,
            client_id=creds.client_id,
            client_secret=creds.client_secret,
            subscription_id=creds.subscription_id
        )
    else:
        return AzureBrowserAuthProvider(
            tenant_id=creds.tenant_id
        )


def create_gcp_provider(creds: Credentials) -> Optional[AuthProvider]:
    """Create GCP auth provider from credentials."""
    if creds.service_account_key:
        # Service account auth would require temp file handling
        return None
    else:
        return GCPBrowserAuthProvider(
            project_id=creds.project_id
        )


def get_or_create_provider(
    provider: CloudProvider,
    auth_manager: AuthManager,
    creds: Credentials
) -> Optional[AuthProvider]:
    """Get existing provider or create new one from credentials."""
    auth_provider = auth_manager.get_provider(provider)
    
    if not auth_provider:
        # Create provider based on type
        if provider == CloudProvider.AWS:
            auth_provider = create_aws_provider(creds)
        elif provider == CloudProvider.AZURE:
            auth_provider = create_azure_provider(creds)
        elif provider == CloudProvider.GCP:
            auth_provider = create_gcp_provider(creds)
        
        if auth_provider:
            auth_manager.register_provider(auth_provider)
    
    return auth_provider


def format_status_details(creds: Credentials) -> Tuple[str, str]:
    """Format status and details from credentials."""
    details_parts = []
    
    # Add provider-specific details
    if creds.provider == CloudProvider.AWS:
        if creds.region:
            details_parts.append(f"Region: {creds.region}")
        if creds.profile:
            details_parts.append(f"Profile: {creds.profile}")
        elif creds.metadata.get("account_id"):
            details_parts.append(f"Account: {creds.metadata['account_id']}")
        if creds.metadata.get("role_name"):
            details_parts.append(f"Role: {creds.metadata['role_name']}")
            
    elif creds.provider == CloudProvider.AZURE:
        details_parts.append(f"Tenant: {creds.tenant_id}")
        if creds.subscription_id:
            details_parts.append(f"Subscription: {creds.subscription_id}")
        if creds.metadata.get("username"):
            details_parts.append(f"User: {creds.metadata['username']}")
            
    elif creds.provider == CloudProvider.GCP:
        details_parts.append(f"Project: {creds.project_id}")
        if creds.metadata.get("email"):
            details_parts.append(f"Email: {creds.metadata['email']}")
        elif creds.metadata.get("service_account_email"):
            details_parts.append(f"Service Account: {creds.metadata['service_account_email']}")
    
    # Check expiration and set status
    if creds.expires_at:
        if creds.is_expired:
            status = "[red]Expired[/red]"
            details_parts.append("[red]Credentials expired[/red]")
        else:
            status = "[green]Configured[/green]"
            if creds.expires_in_minutes is not None:
                if creds.expires_in_minutes < 60:
                    details_parts.append(f"[yellow]Expires in {creds.expires_in_minutes} min[/yellow]")
                else:
                    hours = creds.expires_in_minutes // 60
                    details_parts.append(f"Expires in {hours}h")
    else:
        status = "[green]Configured[/green]"
    
    details = ", ".join(details_parts) if details_parts else "Configured"
    return status, details


async def validate_provider(
    auth_provider: Optional[AuthProvider],
    creds: Credentials
) -> str:
    """Validate authentication provider."""
    if not auth_provider:
        return "[dim]N/A[/dim]"
    
    try:
        is_valid = await auth_provider.validate(creds)
        return "[green]Valid[/green]" if is_valid else "[red]Invalid[/red]"
    except Exception:
        return "[red]Error[/red]"