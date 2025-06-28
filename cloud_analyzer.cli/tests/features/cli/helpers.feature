
Feature: Helper Functions
  As a developer
  I want helper functions to work correctly
  So that the CLI commands function properly

  Scenario: Validate empty configuration
    Given no configuration exists
    When I validate configuration for "all" providers
    Then validation should fail
    And error message should mention "No configuration found"

  Scenario: Validate missing provider configuration
    Given only AWS is configured
    When I validate configuration for "azure" provider
    Then validation should fail
    And error message should mention "No configuration found for provider 'azure'"

  Scenario: Validate existing configuration
    Given all providers are configured
    When I validate configuration for "all" providers
    Then validation should succeed

  Scenario: Determine all providers
    Given configuration exists for AWS, Azure, and GCP
    When I determine providers for "all"
    Then I should get AWS, Azure, and GCP providers

  Scenario: Determine specific provider
    Given configuration exists for AWS
    When I determine providers for "aws"
    Then I should get only AWS provider

  Scenario: Filter results by severity
    Given I have results with different severities
    When I filter results by "high" severity
    Then I should only get high and critical severity results

  Scenario: Save results to JSON
    Given I have analysis results
    When I save results to JSON file "results.json"
    Then the file should contain valid JSON
    And success message should be displayed

  Scenario: Save results to CSV
    Given I have analysis results
    When I save results to CSV file "results.csv"
    Then the file should contain CSV data
    And success message should be displayed

  Scenario: Save empty results to CSV
    Given I have no analysis results
    When I save results to CSV file "results.csv"
    Then no file should be created
    And warning message should be displayed

  Scenario: Display analysis summary
    Given I have analysis results with savings
    When I display the summary
    Then output should show total findings
    And output should show monthly savings
    And output should show annual savings

  Scenario: Encrypt and decrypt configuration
    Given I have a configuration with sensitive data
    When I encrypt the configuration
    And I decrypt the encrypted configuration
    Then the decrypted config should match the original
