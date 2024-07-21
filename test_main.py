from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_recommended_products():
    response = client.get("/products/1", headers={"Authorization": "Bearer johndoe"})
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]["name"] == "Product 1"

def test_read_recommended_products_unauthorized():
    response = client.get("/products/1")
    assert response.status_code == 401
