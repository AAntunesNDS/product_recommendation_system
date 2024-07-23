from fastapi.testclient import TestClient
import pytest
from main import app  # Certifique-se de importar o app da maneira correta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from models import Product
from recomender import ProductRecommender
import crud, schemas, auth

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def test_client():
    return client

def test_create_user(test_client):
    response = test_client.post("/users/", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_create_user_duplicate(test_client):
    test_client.post("/users/", json={"email": "test@example.com", "password": "testpassword"})
    response = test_client.post("/users/", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_for_access_token(test_client):
    test_client.post("/users/", json={"email": "test@example.com", "password": "testpassword"})
    response = test_client.post("/token", data={"username": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_for_access_token_invalid(test_client):
    response = test_client.post("/token", data={"username": "test@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_read_recommended_products_v0(test_client):
    # Mock do ProductRecommender para evitar leitura de arquivo real
    def mock_recommend_products(self, id_usuario, version):
        return [{
            "id": 1,
            "name": "Product 1",
            "sales_per_day": 100,
            "category": "Category A",
            "product_title": "Title A",
            "product_price": 10.0,
            "product_image_url": "http://example.com/image1.jpg",
            "store_name": "Store A",
            "store_id": 101,
            "day_of_week": "Monday"
        }]
    
    # Substituir o método recommend_products do ProductRecommender
    ProductRecommender.recommend_products = mock_recommend_products
    response = test_client.get("/v0/products/1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Product 1"

def test_read_recommended_products_v1(test_client):
    # Mock do ProductRecommender para evitar leitura de arquivo real
    def mock_recommend_products(self, id_usuario, version):
        return [{
            "id": 1,
            "name": "Product 1",
            "sales_per_day": 100,
            "category": "Category A",
            "product_title": "Title A",
            "product_price": 10.0,
            "product_image_url": "http://example.com/image1.jpg",
            "store_name": "Store A",
            "store_id": 101,
            "day_of_week": "Monday"
        }]
    
    # Substituir o método recommend_products do ProductRecommender
    ProductRecommender.recommend_products = mock_recommend_products
    response = test_client.get("/v1/products/1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Product 1"
