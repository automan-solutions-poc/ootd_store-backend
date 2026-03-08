import pytest
from app.core import security

def test_password_hashing():
    password = "testpassword"
    hashed = security.get_password_hash(password)
    assert hashed != password
    assert security.verify_password(password, hashed)
    assert not security.verify_password("wrongpassword", hashed)

def test_create_access_token():
    subject = "user123"
    token = security.create_access_token(subject)
    assert isinstance(token, str)
    assert len(token) > 0
