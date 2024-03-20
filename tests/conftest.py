"""Pytest fixtures to be used by test suite"""

import pytest
from fastapi.testclient import TestClient

from app.server import fastapi_app


@pytest.fixture(scope="session")
def test_client():
    """fastapi test client"""
    client = TestClient(fastapi_app)
    yield client


@pytest.fixture(scope="session")
def sample_user_id():
    """randomly generated user id for testing"""
    return "test_u_2b5e3801a8624f2d854127ae019e0714"
