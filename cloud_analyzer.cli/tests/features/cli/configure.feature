Feature: Configure Cloud Provider Credentials
  As a cloud administrator
  I want to configure my cloud provider credentials
  So that I can authenticate and analyze my cloud resources

  Background:
    Given the CLI application is installed
    And I have a clean configuration directory

  Scenario: Show empty configuration
    Given no providers are configured
    When I run "cloud-analyzer configure --show"
    Then the output should contain "No providers configured"

  Scenario: Show existing configuration
    Given I have configured AWS and Azure providers
    When I run "cloud-analyzer configure --show"
    Then the output should contain "AWS"
    And the output should contain "AZURE"
    And the output should contain "GCP"
    And credentials should be masked with "****"

  Scenario: Clear configuration without specifying provider
    When I run "cloud-analyzer configure --clear"
    Then the output should contain "Error"
    And the output should contain "--provider is required"

  Scenario: Clear AWS configuration
    Given AWS is configured
    When I run "cloud-analyzer configure --clear --provider aws"
    And I confirm with "y"
    Then the output should contain "Configuration cleared for AWS"
    And AWS configuration should be removed

  Scenario: Clear non-existent provider configuration
    Given no providers are configured
    When I run "cloud-analyzer configure --clear --provider aws"
    Then the output should contain "No configuration found for AWS"

  Scenario: Configure AWS with profile
    When I run "cloud-analyzer configure --provider aws"
    And I choose AWS profile authentication
    And I enter profile name "my-profile"
    Then the output should contain "Configuration saved for AWS"
    And AWS should be configured with profile "my-profile"

  Scenario: Configure AWS with access keys
    When I run "cloud-analyzer configure --provider aws"
    And I choose AWS credentials authentication
    And I enter access key "AKIAIOSFODNN7EXAMPLE"
    And I enter secret key "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    And I enter region "us-west-2"
    Then the output should contain "Configuration saved for AWS"
    And AWS should be configured with the provided credentials

  Scenario: Configure Azure with service principal
    When I run "cloud-analyzer configure --provider azure"
    And I enter subscription ID "sub-123"
    And I enter tenant ID "tenant-123"
    And I enter client ID "client-123"
    And I enter client secret "secret-123"
    Then the output should contain "Configuration saved for AZURE"
    And Azure should be configured with the provided credentials

  Scenario: Configure GCP with existing service account file
    Given a service account file exists at "/tmp/service-account.json"
    When I run "cloud-analyzer configure --provider gcp"
    And I enter project ID "project-123"
    And I enter credentials path "/tmp/service-account.json"
    Then the output should contain "Configuration saved for GCP"
    And GCP should be configured with the provided credentials

  Scenario: Configure GCP with missing service account file
    When I run "cloud-analyzer configure --provider gcp"
    And I enter project ID "project-123"
    And I enter credentials path "/nonexistent/file.json"
    And I see warning "File not found"
    And I confirm with "y"
    Then the output should contain "Configuration saved for GCP"

  Scenario: Interactive provider selection
    When I run "cloud-analyzer configure"
    And I select "aws" when prompted for provider
    And I configure AWS with default settings
    Then the output should contain "Configuration saved for AWS"