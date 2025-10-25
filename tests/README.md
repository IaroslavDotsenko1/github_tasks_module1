# FastAPI Tests

This directory contains comprehensive tests for the Mergington High School Activities API.

## Test Structure

- `test_api.py` - Main test file containing all API endpoint tests
- `conftest.py` - Pytest configuration and shared fixtures
- `__init__.py` - Makes this directory a Python package

## Test Categories

### 1. Get Activities Tests (`TestGetActivities`)
- Test successful retrieval of all activities
- Verify response structure and expected activities

### 2. Signup Tests (`TestSignupForActivity`)
- Test successful signup for activities
- Test duplicate participant prevention
- Test non-existent activity handling
- Test URL encoding and special characters

### 3. Unregister Tests (`TestUnregisterFromActivity`)
- Test successful participant unregistration
- Test error cases (non-existent participant/activity)
- Test URL encoding

### 4. Root Endpoint Tests (`TestRootEndpoint`)
- Test redirect functionality

### 5. Integration Tests (`TestIntegrationScenarios`)
- Complete signup/unregister workflows
- Multiple participants scenarios
- Participant capacity tracking

### 6. Error Handling Tests (`TestErrorHandling`)
- Missing parameters
- Edge cases

## Running Tests

### Option 1: Using the test script
```bash
./run_tests.sh
```

### Option 2: Using pytest directly
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing

# Run specific test class
python -m pytest tests/test_api.py::TestSignupForActivity -v

# Run specific test method
python -m pytest tests/test_api.py::TestSignupForActivity::test_signup_success -v
```

## Test Coverage

The test suite achieves **100% code coverage** of the FastAPI application, ensuring all endpoints and code paths are thoroughly tested.

## Dependencies

The following packages are required for testing:
- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting
- `httpx` - HTTP client for FastAPI testing

## Fixtures

- `client` - FastAPI test client
- `backup_activities` - Preserves original test data and restores after each test