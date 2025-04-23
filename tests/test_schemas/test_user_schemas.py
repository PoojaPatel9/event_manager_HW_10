from builtins import str
import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest

# Tests for UserBase
def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]

# Tests for UserCreate
def test_user_create_valid(user_create_data):
    user = UserCreate(**user_create_data)
    assert user.nickname == user_create_data["nickname"]
    assert user.password == user_create_data["password"]

# Tests for UserUpdate
def test_user_update_valid(user_update_data):
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == user_update_data["email"]
    assert user_update.first_name == user_update_data["first_name"]

# Tests for UserResponse
def test_user_response_valid(user_response_data):
    user = UserResponse(**user_response_data)
    assert str(user.id) == user_response_data["id"]
    # assert user.last_login_at == user_response_data["last_login_at"]

# Tests for LoginRequest
def test_login_request_valid(login_request_data):
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]

# Parametrized tests for nickname and email validation
@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["test user", "test?user", "", "us"])
def test_user_base_nickname_invalid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Parametrized tests for URL validation
@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Tests for UserBase
def test_user_base_invalid_email(user_base_data_invalid):
    with pytest.raises(ValidationError) as exc_info:
        user = UserBase(**user_base_data_invalid)
    
    assert "value is not a valid email address" in str(exc_info.value)
    assert "john.doe.example.com" in str(exc_info.value)

def test_user_update_valid_single_field():
    update = UserUpdate(first_name="Jane")
    assert update.first_name == "Jane"

def test_user_update_valid_multiple_fields():
    update = UserUpdate(
        bio="New bio",
        profile_picture_url="https://example.com/pic.jpg"
    )
    assert update.bio == "New bio"

def test_user_update_invalid_empty():
    with pytest.raises(ValidationError) as exc_info:
        UserUpdate()
    assert "At least one field must be provided for update" in str(exc_info.value)

@pytest.mark.parametrize("nickname", [
    "john_doe",     # valid
    "user123",      # valid
    "user-name",    # valid
])
def test_nickname_valid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", [
    "a",            # too short
    "thisnicknameiswaytoolongtobevalidbecauseitexceeds30chars",  # too long
    "invalid*name", # special char not allowed
    "space name",   # space not allowed
])
def test_nickname_invalid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

@pytest.mark.parametrize("password", [
    "Short1!",       # too short
    "alllowercase1!",# no uppercase
    "NoNumber!",     # no number
    "NoSpecial123",  # no special char
])
def test_user_create_invalid_password(password, user_base_data):
    user_base_data["password"] = password
    with pytest.raises(ValidationError):
        UserCreate(**user_base_data)

def test_user_create_valid_password(user_base_data):
    user_base_data["password"] = "StrongPass1!"
    user = UserCreate(**user_base_data)
    assert user.password == "StrongPass1!"
