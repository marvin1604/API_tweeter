# Python
from typing import Optional
from uuid import UUID
from datetime import date
from datetime import datetime

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI

app = FastAPI()

# Models

class Userbase(BaseModel):
    user_id    : UUID     = Field(...)
    email      : EmailStr = Field(...)

class UserLoggin(Userbase):
    password   : str      = Field(
        ...,
        min_length=8
    )

class User(Userbase):
    first_name : str      = Field(
        ...,
        min_length=1,
        max_length=50
    ) 
    last_name  : str      = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date : Optional[date] = Field(default=None)
    

class Tweet(BaseModel):
    tweet_id  : UUID  = Field(...)
    content   : str   = Field(
        ...,
        min_length=1,
        max_length=256
    )
    create_at : datetime = Field(default=datetime.now())
    update_at : Optional[datetime] = Field(default=None)
    by        : User = Field(...)



@app.get(path = "/")
def home():
    return {"Twitter API" : "Working"}
