from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_all_items():
    response = client.get("/items/all-items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_item():
    payload = {
        "title": "Water Bottle",
        "brand": "BrandX",
        "price": 1.5,
        "quantity": 20
    }
    response = client.post("/items/add-item", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["title"] == payload["title"]

def test_get_item_by_id():
    payload = {
        "title": "Chips",
        "brand": "SnackBrand",
        "price": 2.0,
        "quantity": 10 
    }
    create_response = client.post("/items/add-item", json=payload)
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]
    
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id

def test_get_item_not_found():
    response = client.get("/items/9999")
    assert response.status_code in [404, 500]
    assert "detail" in response.json()

def test_update_item():
    payload = {
        "title": "Soda",
        "brand": "BeverageCo",
        "price": 1.0,
        "quantity": 10
    }
    create_response = client.post("/items/add-item", json=payload)
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]
    
    update_payload = {
        "title": "Soda Lite",
        "brand": "BeverageCo",
        "price": 1.2,
        "quantity": 15
    }
    response = client.put(f"/items/update-item/{item_id}", json=update_payload)
    assert response.status_code == 200
    updated_item = response.json()
    
    if isinstance(updated_item, dict) and "title" in updated_item:
        assert updated_item["title"] == "Soda Lite"
    else:
        get_response = client.get(f"/items/{item_id}")   
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "Soda Lite"

def test_delete_item():
    payload = {
        "title": "Juice",
        "brand": "FruitCo",
        "price": 1.8,
        "quantity": 15
    }
    create_response = client.post("/items/add-item", json=payload)
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]
    
    response = client.delete(f"/items/delete-item/{item_id}")
    assert response.status_code == 200
    
    response = client.get(f"/items/{item_id}")
    assert response.status_code in [404, 500]

def test_create_item_missing_field():
    payload = {
        "title": "Broken Item",
        "brand": "NoPriceBrand",
        "quantity": 10
    }
    response = client.post("/items/add-item", json=payload)
    assert response.status_code == 422


def test_create_item_invalid_price():
    payload = {
        "title": "Invalid Price Item",
        "brand": "BadBrand",
        "price": "not_a_number",
        "quantity": 5
    }
    response = client.post("/items/add-item", json=payload)
    assert response.status_code == 422


def test_update_nonexistent_item():
    update_payload = {
        "title": "Ghost Item",
        "brand": "NowhereBrand",
        "price": 9.9,
        "quantity": 1
    }
    response = client.put("/items/update-item/9999", json=update_payload)
    assert response.status_code in [404, 500]


def test_delete_nonexistent_item():
    response = client.delete("/items/delete-item/9999")
    assert response.status_code in [404, 500] 