#!/usr/bin/env python3
"""
Test runner script for Punjabi Language Learning Tool

This script runs pytest with appropriate configuration.
"""
import sys
import os

# Ensure we have pytest
try:
    import pytest
except ImportError:
    print("❌ Error: pytest not installed")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

# Check for .env file (tests need it too)
if not os.path.exists(".env"):
    print("⚠️  Warning: .env file not found")
    print("Some tests may fail without proper configuration")
    print()

print("🧪 Running Punjabi Language Learning Tool Tests")
print("=" * 50)
print()

# Run pytest with configuration from pytest.ini
exit_code = pytest.main([
    "-v",  # Verbose
    "--tb=short",  # Short traceback
    "tests/",  # Test directory
    "-m", "not api",  # Skip API tests by default to avoid costs
])

print()
print("=" * 50)

if exit_code == 0:
    print("✅ All tests passed!")
else:
    print(f"❌ Tests failed with exit code {exit_code}")

print()
print("To run ALL tests including API calls (costs money):")
print("  pytest tests/")
print()
print("To run specific test file:")
print("  pytest tests/test_models.py")

sys.exit(exit_code)

