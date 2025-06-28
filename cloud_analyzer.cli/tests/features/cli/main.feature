Feature: Cloud Analyzer CLI Main Interface
  As a cloud administrator
  I want to use the cloud analyzer CLI
  So that I can analyze and optimize my cloud costs

  Background:
    Given the CLI application is installed

  Scenario: Display help information
    When I run "cloud-analyzer --help"
    Then the output should contain "Cloud Analyzer - Multi-cloud cost optimization tool"
    And the output should contain "analyze"
    And the output should contain "configure"
    And the output should contain "list-checks"
    And the output should contain "report"

  Scenario: Display version information
    When I run "cloud-analyzer --version"
    Then the output should contain "cloud-analyzer, version 0.1.0"

  Scenario: Run invalid command
    When I run "cloud-analyzer invalid-command"
    Then the command should fail
    And the output should contain "No such command" or "Invalid"

  Scenario: Handle keyboard interrupt gracefully
    When I run the CLI and press Ctrl+C
    Then the output should contain "Operation cancelled by user"
    And the exit code should be 1

  Scenario: Handle unexpected errors
    When the CLI encounters an unexpected error
    Then the error should be logged
    And the output should contain "Unexpected error"
    And the output should contain "Run with --debug for more information"
    And the exit code should be 1