# BDD Tests with Gherkin

This directory contains Behavior-Driven Development (BDD) tests written using Gherkin syntax with pytest-bdd.

## Structure

```
tests/
├── features/           # Gherkin feature files
│   └── cli/
│       ├── main.feature
│       ├── configure.feature
│       ├── analyze.feature
│       ├── list_checks.feature
│       ├── report.feature
│       └── helpers.feature
└── cli/               # Step definitions
    ├── test_main_bdd.py
    ├── test_configure_bdd.py
    ├── test_analyze_bdd.py
    ├── test_list_checks_bdd.py
    ├── test_report_bdd.py
    └── test_helpers_bdd.py
```

## Running the Tests

### Run all BDD tests:
```bash
pytest tests/cli/test_*_bdd.py -v
```

### Run specific feature tests:
```bash
# Test main CLI functionality
pytest tests/cli/test_main_bdd.py -v

# Test configure command
pytest tests/cli/test_configure_bdd.py -v

# Test analyze command
pytest tests/cli/test_analyze_bdd.py -v

# Test list-checks command
pytest tests/cli/test_list_checks_bdd.py -v

# Test report command
pytest tests/cli/test_report_bdd.py -v

# Test helper functions
pytest tests/cli/test_helpers_bdd.py -v
```

### Generate test report:
```bash
pytest tests/cli/test_*_bdd.py --html=report.html --self-contained-html
```

### Run with coverage:
```bash
pytest tests/cli/test_*_bdd.py --cov=cli --cov-report=html
```

## Writing New Tests

1. **Create a feature file** in `tests/features/cli/`:
```gherkin
Feature: New Feature
  As a user
  I want to do something
  So that I achieve a goal

  Scenario: Basic scenario
    Given some precondition
    When I perform an action
    Then I expect a result
```

2. **Create step definitions** in `tests/cli/test_<feature>_bdd.py`:
```python
from pytest_bdd import scenarios, given, when, then

scenarios('../features/cli/new_feature.feature')

@given('some precondition')
def setup_precondition():
    # Setup code
    pass

@when('I perform an action')
def perform_action():
    # Action code
    pass

@then('I expect a result')
def check_result():
    # Assertion code
    assert True
```

## Gherkin Keywords

- **Feature**: High-level description of the feature being tested
- **Scenario**: A specific test case
- **Given**: Preconditions/setup
- **When**: The action being tested
- **Then**: Expected outcome/assertions
- **And**: Additional steps (can follow Given, When, or Then)
- **But**: Alternative to And for negative cases
- **Background**: Common setup for all scenarios in a feature
- **Scenario Outline**: Parameterized scenarios with Examples

## Best Practices

1. **Keep scenarios focused**: Each scenario should test one specific behavior
2. **Use descriptive names**: Scenario names should clearly indicate what's being tested
3. **Reuse step definitions**: Create generic step definitions that can be shared
4. **Avoid technical details**: Feature files should be readable by non-developers
5. **Use Background wisely**: Only include truly common setup steps

## Example Scenario

```gherkin
Feature: Cloud Provider Configuration
  As a cloud administrator
  I want to configure my cloud credentials
  So that I can analyze my cloud resources

  Background:
    Given the CLI application is installed

  Scenario: Configure AWS with SSO
    When I run "cloud-analyzer configure --provider aws"
    And I choose browser authentication
    And I enter SSO start URL "https://example.awsapps.com/start"
    Then the output should contain "Opening browser for authentication"
    And the output should contain "Configuration saved for AWS"
```

## Debugging Tests

### Run with verbose output:
```bash
pytest tests/cli/test_main_bdd.py -vv -s
```

### Run specific scenario:
```bash
pytest tests/cli/test_main_bdd.py -k "Display help information" -v
```

### Show available markers:
```bash
pytest --markers
```

## Common Issues

1. **Import errors**: Ensure the project is installed with `pip install -e .`
2. **Step not found**: Check that step definitions match exactly (including parameters)
3. **Fixture issues**: Ensure fixtures are properly scoped and imported