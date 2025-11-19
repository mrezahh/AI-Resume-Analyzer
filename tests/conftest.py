import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app
import models.user  # Ensure models are imported for metadata

# Create a new database for testing (SQLite in-memory database)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the testing database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db

# Create tables for testing
Base.metadata.create_all(bind=engine)


# ==================== Pytest Fixtures ====================
@pytest.fixture(autouse=True)
def reset_database():
    """Recreate the database tables before each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
        
@pytest.fixture
def test_user(client):
    """Create a test user."""
    user_data = {"email": "testuser@example.com", "full_name": "Test User", "password": "testpassword"}
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    
    # login to get the token
    login_response = client.post("/auth/login", 
                                 data={"username": user_data["email"], 
                                       "password": user_data["password"]
                                        })
    token = login_response.json()["access_token"]
    user_data["token"] = token
    return user_data
    
