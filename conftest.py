import pytest


def pytest_configure(config: pytest.Config):
    config.addinivalue_line("markers", "success_rate: mark test as a success rate test")
    config.addinivalue_line("markers", "performance: mark test as a performance test")
