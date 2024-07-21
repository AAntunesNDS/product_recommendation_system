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


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}

class User(BaseModel):
    username: str
    email: str
    full_name: str = None
    disabled: bool = None

class UserInDB(User):
    hashed_password: str

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)