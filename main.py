from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from models import Product
from sqlalchemy import text
from dotenv import load_dotenv
from typing import List
from recomender import ProductRecommender
from sqlalchemy.orm import Session
from datetime import timedelta
import crud, schemas, database, auth

load_dotenv()

app = FastAPI()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)



@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/v0/products/{id_usuario}", response_model=List[Product])
def read_recommended_products(id_usuario: int):
    csv_file = 'db/xpto_sales_products_mar_may_2024.csv-Página4.csv'
    return ProductRecommender(csv_file).recommend_products(id_usuario, 'v0')

#TODO: Criar uma dependencia do do usuário estar logado e utilizar um Token de Acesso
@app.get("/v1/products/{id_usuario}", response_model=List[Product])
def read_recommended_products(id_usuario: int):
    csv_file = 'db/xpto_sales_products_mar_may_2024.csv-Página4.csv'
    return ProductRecommender(csv_file).recommend_products(id_usuario, 'v1')
