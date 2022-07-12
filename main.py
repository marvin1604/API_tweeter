# Python
from typing import Optional
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import List


# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status

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

# Path Operations 

## Users

### Register a User
@app.post(
    path="/signup",
    response_model = User,
    status_code = status.HTTP_201_CREATED,
    summary = "Register a User",
    tags = ["Users"]

    )

def signup():
    pass

### Login a User
@app.post(
    path="/login",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Login a User",
    tags = ["Users"]

    )

def loginup():
    pass

### Show all Users
@app.get(
    path="/users",
    response_model = List[User],
    status_code = status.HTTP_200_OK,
    summary = "Show all Users",
    tags = ["Users"]

    )

def show_all_users():
    pass

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Show a User",
    tags = ["Users"]

    )

def show_a_user():
    pass

### Delete a User
@app.delete(
    path="/users/{user-id}/delete",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Delete a User",
    tags = ["Users"]

    )

def delete_a_user():
    pass

### Update a User
@app.put(
    path="/users/{user-id}/update",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Update a User",
    tags = ["Users"]

    )

def update_a_user():
    pass

## Tweets

### Show all Tweets
@app.get(
    path = "/",
    response_model = List[Tweet],
    status_code = status.HTTP_200_OK,
    summary = "Show all Tweet",
    tags = ["Tweets"]
    )
def home():
    return {"Twitter API" : "Working"}

### Post a Tweet
@app.post(
    path="/post",
    response_model = Tweet,
    status_code = status.HTTP_201_CREATED,
    summary = "Post a tweet",
    tags = ["Tweets"]

    )

def post():
    pass

### Show a Tweet
@app.get(
    path="/tweet/{tweet_id}",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Show a tweet",
    tags = ["Tweets"]

    )

def show_a_tweet():
    pass

### Delete a Tweet
@app.delete(
    path="/tweet/{tweet_id}/delete",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Delete a tweet",
    tags = ["Tweets"]

    )

def delete_a_tweet():
    pass

### Update a Tweet
@app.put(
    path="/tweet/{tweet_id}/update",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Update a tweet",
    tags = ["Tweets"]

    )

def update_a_tweet():
    pass