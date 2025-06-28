Feature: List Available Optimization Checks
  As a cloud administrator
  I want to list available optimization checks
  So that I can understand what optimizations are available

  Background:
    Given the CLI application is installed
    And the check registry contains sample checks

  Scenario: List all available checks
    When I run "cloud-analyzer list-checks"
    Then the output should contain "Available Optimization Checks"
    And the output should contain "idle-ec2-instances"
    And the output should contain "oversized-instances"
    And the output should contain "idle-vm-instances"
    And the output should contain "Total checks: 3"

  Scenario: Filter checks by provider
    When I run "cloud-analyzer list-checks --provider aws"
    Then the output should contain "idle-ec2-instances"
    And the output should contain "oversized-instances"
    But the output should not contain "idle-vm-instances"

  Scenario: Filter checks by type
    When I run "cloud-analyzer list-checks --type idle_resource"
    Then the output should contain "idle-ec2-instances"
    And the output should contain "idle-vm-instances"
    But the output should not contain "oversized-instances"

  Scenario: Filter with invalid check type
    When I run "cloud-analyzer list-checks --type invalid_type"
    Then the output should contain "Error"
    And the output should contain "Invalid check type"
    And the output should contain "Valid check types:"

  Scenario: Combine provider and type filters
    When I run "cloud-analyzer list-checks --provider aws --type idle_resource"
    Then the output should contain "idle-ec2-instances"
    But the output should not contain "oversized-instances"
    And the output should not contain "idle-vm-instances"

  Scenario: No matching checks found
    When I run "cloud-analyzer list-checks --provider gcp --type idle_resource"
    Then the output should contain "No checks found matching the criteria"

  Scenario: Display check summary statistics
    When I run "cloud-analyzer list-checks"
    Then the output should contain "Total checks: 3"
    And the output should contain "Check types: 2"
    And the output should contain "idle_resource: 2 checks"
    And the output should contain "right_sizing: 1 checks"

  Scenario: Empty check registry
    Given the check registry is empty
    When I run "cloud-analyzer list-checks"
    Then the output should contain "No checks found matching the criteria"

  Scenario: Verify table format
    When I run "cloud-analyzer list-checks"
    Then the output should display a table with columns:
      | Column      |
      | Check Name  |
      | Type        |
      | Providers   |
      | Description |

  Scenario: Verify provider formatting
    When I run "cloud-analyzer list-checks"
    Then providers should be displayed in uppercase
    And multi-provider checks should show "AWS, AZURE, GCP"