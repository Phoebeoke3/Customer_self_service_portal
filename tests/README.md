# Test Suite for SwissAxa Customer Self-Service Portal

This directory contains the comprehensive unit test suite for the SwissAxa Portal application.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Pytest fixtures and configuration
├── test_models.py           # Database model tests
├── test_auth.py             # Authentication route tests
├── test_policies.py         # Policy-related route tests
├── test_claims.py           # Claims management tests
├── test_documents.py        # Document upload/download tests
├── test_services.py         # Services (contact, scheduling, etc.) tests
├── test_information.py     # User information management tests
└── test_bank.py             # Bank account management tests
```

## Running Tests

### Install Dependencies

First, make sure all testing dependencies are installed:

```bash
pip install -r requirements.txt
```

### Run All Tests

**Windows (PowerShell):**
```powershell
.\run_tests.ps1
```

**Windows (Command Prompt):**
```cmd
run_tests.bat
```

**Linux/Mac:**
```bash
python run_tests.py
```

**Direct pytest:**
```bash
pytest tests/ -v
```

### Run Specific Test Files

```bash
# Run only model tests
pytest tests/test_models.py -v

# Run only authentication tests
pytest tests/test_auth.py -v

# Run only policy tests
pytest tests/test_policies.py -v
```

### Run Specific Tests

```bash
# Run a specific test class
pytest tests/test_models.py::TestUserModel -v

# Run a specific test function
pytest tests/test_auth.py::TestLogin::test_login_success -v
```

### Run with Coverage

The test runner automatically generates coverage reports:

```bash
python run_tests.py
```

Coverage reports are generated in:
- Terminal output (summary)
- `htmlcov/` directory (HTML report)
- `coverage.xml` (XML report for CI/CD)

### Run Tests in Verbose Mode

```bash
pytest tests/ -v -s
```

The `-s` flag shows print statements and other output.

## Test Coverage

The test suite covers:

### ✅ Database Models
- User model (creation, password hashing, relationships)
- Agent model
- SwissAxaPolicy model
- ExternalPolicy model
- Claim and ClaimMedia models
- Document model
- BankAccount model
- Appointment model
- PolicyChangeRequest model

### ✅ Authentication Routes
- Login (success, failure, validation)
- Registration (success, duplicate email, validation)
- Logout
- Protected route access control

### ✅ Policy Routes
- Policy listing
- External policy upload
- Policy comparison API
- Expiration warnings

### ✅ Claims Management
- Filing claims
- Uploading claim media (photos/videos)
- Claim listing
- Geolocation handling

### ✅ Document Management
- Document upload
- Document download
- Document type organization
- Access control (users can't access other users' documents)

### ✅ Services
- Policy management requests
- Contact (email to service desk/agents)
- Appointment scheduling
- Policy change requests

### ✅ User Information
- Viewing user information
- Updating user information
- Partial updates

### ✅ Bank Management
- Connecting bank accounts
- Bank transactions
- Account listing

## Test Fixtures

The `conftest.py` file provides reusable fixtures:

- `test_app`: Flask application with test database
- `client`: Test client for making requests
- `authenticated_client`: Authenticated test client
- `test_user`: Sample user for testing
- `test_agent`: Sample agent for testing
- `test_policy`: Sample SwissAxa policy
- `test_external_policy`: Sample external policy
- `test_claim`: Sample claim
- `test_document`: Sample document
- `test_bank_account`: Sample bank account
- `test_appointment`: Sample appointment

## Writing New Tests

When adding new tests:

1. **Follow naming conventions:**
   - Test files: `test_*.py`
   - Test classes: `Test*`
   - Test functions: `test_*`

2. **Use fixtures:**
   ```python
   def test_my_feature(authenticated_client, test_user):
       # Your test code
   ```

3. **Clean up:**
   - Tests automatically clean up database and files
   - Use temporary files for file uploads

4. **Assertions:**
   - Use descriptive assertion messages
   - Test both success and failure cases
   - Test edge cases and validation

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ --cov=app --cov-report=xml
```

## Troubleshooting

### Tests fail with database errors
- Make sure you're using the test database (handled by fixtures)
- Check that test database is properly cleaned up

### Import errors
- Ensure you're running tests from the project root
- Check that `app.py` is in the Python path

### Authentication issues
- Use the `authenticated_client` fixture for authenticated requests
- Check that test user password matches fixture password

### File upload tests fail
- Ensure temporary files are properly created and cleaned up
- Check file paths and permissions

## Test Statistics

Run tests with coverage to see:
- Total number of tests
- Pass/fail statistics
- Code coverage percentage
- Lines not covered

## Best Practices

1. **Isolation**: Each test should be independent
2. **Speed**: Tests should run quickly (use test database)
3. **Clarity**: Test names should describe what they test
4. **Coverage**: Aim for high code coverage (>80%)
5. **Maintainability**: Keep tests simple and readable

