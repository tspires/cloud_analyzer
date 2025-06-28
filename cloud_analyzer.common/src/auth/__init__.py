"""Authentication module for cloud providers."""

from auth.aws import AWSSSOAuthProvider, AWSProfileAuthProvider
from auth.azure import AzureBrowserAuthProvider, AzureServicePrincipalAuthProvider
from auth.base import (
    AuthProvider,
    AWSCredentials,
    AzureCredentials,
    BrowserAuthProvider,
    Credentials,
    GCPCredentials,
)
from auth.gcp import GCPBrowserAuthProvider, GCPServiceAccountAuthProvider
from auth.manager import AuthManager

__all__ = [
    "AuthProvider",
    "BrowserAuthProvider",
    "Credentials",
    "AWSCredentials",
    "AzureCredentials",
    "GCPCredentials",
    "AuthManager",
    "AWSSSOAuthProvider",
    "AWSProfileAuthProvider",
    "AzureBrowserAuthProvider",
    "AzureServicePrincipalAuthProvider",
    "GCPBrowserAuthProvider",
    "GCPServiceAccountAuthProvider",
]