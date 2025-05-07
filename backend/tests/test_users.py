import pytest
from fastapi.testclient import TestClient
from database import Base, engine, get_db
from backend.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from models import Users, Items
from fastapi import status

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_up():
    """Clean up users and items tables before each test"""
    db = TestingSessionLocal()
    db.execute(text("DELETE FROM users"))
    db.execute(text("DELETE FROM items"))
    db.commit()
    db.close()

def test_login_success():
    # Setup: Create a test user
    db = TestingSessionLocal()
    test_user = Users(
        username="testuser",
        password="testpass",
        admin=False
    )
    db.add(test_user)
    db.commit()
    db.close()

    response = client.post(
        "/users/login",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert response.json().get("message") == "Login successful"

def test_login_invalid_credentials():
    response = client.post(
        "/users/login",
        json={"username": "nonexistent", "password": "wrong"}
    )
    assert response.status_code == 500
    assert "detail" in response.json()

def test_purchase_item_success():
    db = TestingSessionLocal()
    
    test_item = Items(
        title="Test Item",
        brand="Test Brand",
        price=10.0,
        quantity=20
    )
    db.add(test_item)
    db.commit()
    item_id = test_item.id
    
    test_user = Users(
        username="buyer",
        password="pass",
        admin=False
    )
    db.add(test_user)
    db.commit()
    db.close()

    response = client.put(
        f"/users/purchase/user",
        params={"admin": False},
        json={"id": item_id, "quantity": 5}
    )
    assert response.status_code == 200
    assert "has been purchased" in response.json().get("message", "")

def test_purchase_item_admin_blocked():
    db = TestingSessionLocal()
    test_item = Items(
        title="Admin Item",
        brand="Admin Brand",
        price=15.0,
        quantity=10
    )
    db.add(test_item)
    db.commit()
    item_id = test_item.id
    db.close()

    response = client.put(
        f"/users/purchase/admin",
        params={"admin": True},
        json={"id": item_id, "quantity": 2}
    )
    assert response.status_code == 500
    assert "detail" in response.json()

def test_purchase_item_not_found():
    response = client.put(
        "/users/purchase/user",
        params={"admin": False},
        json={"id": 9999, "quantity": 1}
    )
    assert response.status_code == 500
    assert "detail" in response.json()

def test_total_revenue_admin_success():
    db = TestingSessionLocal()
    test_item = Items(
        title="Revenue Item",
        brand="RevenueBrand",
        price=12.5,
        quantity=5
    )
    db.add(test_item)
    db.commit()
    db.close()

    response = client.get(
        "/users/total-revenue/RevenueBrand",
        params={"admin": True}
    )
    assert response.status_code == 200
    assert "total revenue" in response.json().get("message", "")

def test_total_revenue_non_admin_blocked():
    response = client.get(
        "/users/total-revenue/AnyBrand",
        params={"admin": False}
    )

    assert response.status_code == 500
    assert "detail" in response.json()

def test_total_revenue_brand_not_found():
    response = client.get(
        "/users/total-revenue/NonExistentBrand",
        params={"admin": True}
    )

    assert response.status_code == 500
    assert "detail" in response.json()