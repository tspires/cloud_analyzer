"""Constants for the CLI application."""

from typing import List, Dict

# Version
VERSION = "0.1.0"

# Provider choices for CLI commands
PROVIDER_CHOICES = ["azure"]
PROVIDER_CHOICES_WITH_ALL = ["azure"]

# Output format choices
OUTPUT_FORMAT_CHOICES = ["table", "json", "csv"]

# Severity choices
SEVERITY_CHOICES = ["critical", "high", "medium", "low", "all"]

# Authentication type choices
AUTH_TYPE_CHOICES = ["browser", "credentials", "profile", "cli"]

# Default values
DEFAULT_PROVIDER = "all"
DEFAULT_OUTPUT_FORMAT = "table"
DEFAULT_SEVERITY = "all"

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_KEYBOARD_INTERRUPT = 130

# Error messages
ERROR_NO_CONFIG = "No configuration found. Please run 'cloud-analyzer configure' first."
ERROR_NO_PROVIDER_CONFIG = "No configuration found for provider '{}'. Please run 'cloud-analyzer configure' first."
ERROR_INVALID_CHECK_TYPE = "Invalid check type '{}'"
ERROR_NO_CHECKS_FOUND = "No checks found matching the criteria"
ERROR_UNEXPECTED = "Unexpected error: {}"

# Success messages
SUCCESS_CONFIG_SAVED = "Configuration saved successfully"
SUCCESS_CONFIG_CLEARED = "Configuration cleared for {}"

# Info messages
INFO_OPERATION_CANCELLED = "Operation cancelled by user"
INFO_RUN_WITH_DEBUG = "Run with --debug for more information"

# File permissions
FILE_PERMISSION_OWNER_RW = 0o600

