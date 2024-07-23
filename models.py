from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    sales_per_day: int
    category: str
    product_title: str
    product_price: float
    product_image_url: str
    store_name: str
    store_id: int
    day_of_week: str

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
