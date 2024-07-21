from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from models import Product, fake_decode_token, User
from dotenv import load_dotenv
from typing import List
from recomender import ProductRecommender

load_dotenv()

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/products/{id_usuario}", response_model=List[Product])
async def read_recommended_products(id_usuario: int):

    csv_file = 'db/xpto_sales_products_mar_may_2024.csv-Página4.csv'
    return ProductRecommender(csv_file).recommend_products(id_usuario)
