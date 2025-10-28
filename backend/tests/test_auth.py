import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User
from app.auth.security import hash_password
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

# Test database configuration
TEST_MONGODB_URL = "mongodb://localhost:27017"
TEST_DATABASE_NAME = "test_auth_db"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def setup_database():
    """Setup test database"""
    client = AsyncIOMotorClient(TEST_MONGODB_URL)
    await init_beanie(
        database=client[TEST_DATABASE_NAME],
        document_models=[User]
    )
    yield
    # Cleanup
    await client.drop_database(TEST_DATABASE_NAME)
    client.close()

@pytest.fixture(autouse=True)
async def cleanup_database():
    """Clean up database after each test"""
    yield
    await User.delete_all()

# Create test client
client = TestClient(app)

@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "Test1234!"
    }

@pytest.fixture
async def registered_user(test_user_data):
    """Create a registered user in the database"""
    user = User(
        email=test_user_data["email"],
        username=test_user_data["username"],
        hashed_password=hash_password(test_user_data["password"])
    )
    await user.insert()
    return test_user_data

class TestRegistration:
    """Test user registration"""
    
    @pytest.mark.asyncio
    async def test_register_user_success(self, test_user_data, setup_database):
        """Test successful user registration"""
        response = client.post("/auth/register", json=test_user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["username"] == test_user_data["username"]
        assert "id" in data
        assert data["is_active"] is True

    @pytest.mark.asyncio 
    async def test_register_duplicate_email(self, registered_user, setup_database):
        """Test registration with duplicate email"""
        user_data = {
            "email": registered_user["email"],
            "username": "newusername",
            "password": "Test1234!"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

class TestLogin:
    """Test user login"""
    
    @pytest.mark.asyncio
    async def test_login_success(self, registered_user, setup_database):
        """Test successful login"""
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, registered_user, setup_database):
        """Test login with wrong password"""
        login_data = {
            "email": registered_user["email"],
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]


# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.main import app
# from app.database import Base, get_db
# from app.models import User
# from app.auth.security import hash_password

# # Create test database
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def override_get_db():
#     """Override database dependency for testing"""
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db

# # Create test client
# client = TestClient(app)


# @pytest.fixture(autouse=True)
# def setup_database():
#     """Setup and teardown test database"""
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)


# @pytest.fixture
# def test_user_data():
#     """Sample user data for testing"""
#     return {
#         "email": "test@example.com",
#         "username": "testuser",
#         "password": "Test1234!"
#     }


# @pytest.fixture
# def registered_user(test_user_data):
#     """Create a registered user in the database"""
#     db = TestingSessionLocal()
#     user = User(
#         email=test_user_data["email"],
#         username=test_user_data["username"],
#         hashed_password=hash_password(test_user_data["password"])
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     db.close()
#     return test_user_data


# class TestRegistration:
#     """Test user registration"""
    
#     def test_register_success(self, test_user_data):
#         """Test successful user registration"""
#         response = client.post("/auth/register", json=test_user_data)
#         assert response.status_code == 201
#         data = response.json()
#         assert data["email"] == test_user_data["email"]
#         assert data["username"] == test_user_data["username"]
#         assert "id" in data
#         assert "hashed_password" not in data
    
#     def test_register_duplicate_email(self, registered_user):
#         """Test registration with duplicate email"""
#         response = client.post("/auth/register", json=registered_user)
#         assert response.status_code == 400
#         assert "Email already registered" in response.json()["detail"]
    
#     def test_register_weak_password(self):
#         """Test registration with weak password"""
#         weak_password_data = {
#             "email": "weak@example.com",
#             "username": "weakuser",
#             "password": "weak"
#         }
#         response = client.post("/auth/register", json=weak_password_data)
#         assert response.status_code == 422
    
#     def test_register_invalid_email(self):
#         """Test registration with invalid email"""
#         invalid_email_data = {
#             "email": "notanemail",
#             "username": "testuser",
#             "password": "Test1234!"
#         }
#         response = client.post("/auth/register", json=invalid_email_data)
#         assert response.status_code == 422


# class TestLogin:
#     """Test user login"""
    
#     def test_login_success(self, registered_user):
#         """Test successful login"""
#         response = client.post("/auth/login", json={
#             "email": registered_user["email"],
#             "password": registered_user["password"]
#         })
#         assert response.status_code == 200
#         data = response.json()
#         assert "access_token" in data
#         assert data["token_type"] == "bearer"
    
#     def test_login_wrong_password(self, registered_user):
#         """Test login with wrong password"""
#         response = client.post("/auth/login", json={
#             "email": registered_user["email"],
#             "password": "WrongPassword123!"
#         })
#         assert response.status_code == 401
#         assert "Incorrect email or password" in response.json()["detail"]
    
#     def test_login_nonexistent_user(self):
#         """Test login with non-existent user"""
#         response = client.post("/auth/login", json={
#             "email": "nonexistent@example.com",
#             "password": "Test1234!"
#         })
#         assert response.status_code == 401


# class TestProtectedRoutes:
#     """Test protected endpoints"""
    
#     def test_get_current_user_with_valid_token(self, registered_user):
#         """Test accessing protected route with valid token"""
#         # Login to get token
#         login_response = client.post("/auth/login", json={
#             "email": registered_user["email"],
#             "password": registered_user["password"]
#         })
#         token = login_response.json()["access_token"]
        
#         # Access protected route
#         response = client.get(
#             "/users/me",
#             headers={"Authorization": f"Bearer {token}"}
#         )
#         assert response.status_code == 200
#         data = response.json()
#         assert data["email"] == registered_user["email"]
#         assert data["username"] == registered_user["username"]
    
#     def test_get_current_user_without_token(self):
#         """Test accessing protected route without token"""
#         response = client.get("/users/me")
#         assert response.status_code == 403
    
#     def test_get_current_user_with_invalid_token(self):
#         """Test accessing protected route with invalid token"""
#         response = client.get(
#             "/users/me",
#             headers={"Authorization": "Bearer invalid_token_here"}
#         )
#         assert response.status_code == 401
    
#     def test_get_current_user_with_expired_token(self):
#         """Test accessing protected route with malformed token"""
#         response = client.get(
#             "/users/me",
#             headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"}
#         )
#         assert response.status_code == 401