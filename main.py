# Python
from typing import Optional
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import List
import json


# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import Body, FastAPI, Path
from fastapi import status
from fastapi import Body, Form
from fastapi import HTTPException

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

class UserRegister(User):
    password   : str      = Field(
        ...,
        min_length=8
    )       

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

def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path parameter register a user i the app

    Parameters:
        - Request body parameter
            - user: UserRegister

    Returns a json with the basic user information:
        - user_id    : UUID
        - email      : Emailstr
        - first_name : str
        - last_name  : str
        - birth_date : str
   
    """
    with open("users.json", "r+", encoding="utf-8" ) as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

### Login a User
@app.post(
    path="/login",
    # response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Login a User",
    tags = ["Users"]

    )

def login(email: EmailStr= Form(...), password: str = Form(...)):
    """
    Login

    This path operation login a Person in the app

    Parameters:
        - Request body parameter
            - email      : EmailStr
            - password   : str 

    
    Returns a user model and message
   
    """
    with open("users.json", "r", encoding= "utf-8") as f:
        datos = json.loads(f.read())    
        for user in datos:
            if user["email"] == email and user["password"] == password:
                return "login successful",  user
        
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡email or password incorrect!"
              )

            
### Show all Users
@app.get(
    path="/users",
    response_model = List[User],
    status_code = status.HTTP_200_OK,
    summary = "Show all Users",
    tags = ["Users"]

    )

def show_all_users():
    """
    Show all Users

    This path operation shows all users in the app
    
    Parameters:
        -

    returns a json list with all users in the app, with the following keys
        - user_id    : UUID
        - email      : Emailstr
        - first_name : str
        - last_name  : str
        - birth_date : str
    """
    with open("users.json", "r", encoding= "utf-8") as f:
        results = json.loads(f.read())
        return results

### Show a user
@app.get(
    path="/users/{user_id}",
    # response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Show a User",
    tags = ["Users"]

    )

def show_a_user(user_id: UUID = Path(
    ...,
    title = "User ID",
    description = " this is the user ID",
    example= "3fa85f64-5717-4562-b3fc-2c963f66afa8"
    )
):
    """
    Show a User
    
    This path operation show if a user is in the app
    
    Parameters:
        - user_id : UUID

    returns a json list with the user in the app, with the following keys
        - user_id    : UUID
        - email      : Emailstr
        - first_name : str
        - last_name  : str
        - birth_date : str
    """
    with open("users.json", "r", encoding= "utf-8") as f:
        datos = json.loads(f.read())
        for user in datos:
            if user["user_id"] == str(user_id) :
                return "user exist!!",  user
        
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡user not exist!"
              )

### Delete a User
@app.delete(
    path="/users/{user_id}/delete",
    # response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Delete a User",
    tags = ["Users"]

    )

def delete_a_user(user_id: UUID = Path(
    ...,
    title = "User ID",
    description = " this is the user ID",
    example= "3fa85f64-5717-4562-b3fc-2c963f66afa8"
    )
):
    """
    Delete a User
    
    This path operation delete a user in the app
    
    Parameters:
        - user_id : UUID

    returns a json list with the user delete, with the following keys
        - user_id    : UUID
        - email      : Emailstr
        - first_name : str
        - last_name  : str
        - birth_date : str
    """
    with open("users.json", "r+", encoding= "utf-8") as f:
        datos = json.loads(f.read())
        for user in datos:
            if user["user_id"] == str(user_id):
                datos.remove(user)
                with open("users.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(datos))
                    return "user delete", user
                
                      
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡user not exist!"
              )

### Update a User
@app.put(
    path="/users/{user_id}/update",
    # response_model = UserRegister,
    status_code = status.HTTP_200_OK,
    summary = "Update a User",
    tags = ["Users"]

    )

def update_a_user(user_id: UUID = Path(
    ...,
    title = "User ID",
    description = " this is the user ID",
    example= "3fa85f64-5717-4562-b3fc-2c963f66afa8"
    ),
    user: UserRegister = Body(...)
):
    """
    Update a User
    
    This path operation update an user in the app
    
    Parameters:
        - user_id : UUID

    returns a json list with the user update, with the following keys
        - user_id    : UUID
        - email      : Emailstr
        - first_name : str
        - last_name  : str
        - birth_date : str
    """
    
    user_dict = user.dict()
    user_dict["user_id"]= str(user_dict["user_id"])
    user_dict["email"]= str(user_dict["email"])
    user_dict["first_name"]= str(user_dict["first_name"])
    user_dict["last_name"]= str(user_dict["last_name"])
    user_dict["birth_date"]= str(user_dict["birth_date"])
    user_dict["password"]= str(user_dict["password"])

    with open("users.json", "r+", encoding= "utf-8") as f:
        datos = json.loads(f.read())
        for user in datos:
            if user["user_id"] == str(user_id):
                datos[datos.index(user)] = user_dict
                with open("users.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(datos))
                    return "user update", user
                
                      
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡user not exist!"
              )


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
    """
    This path operation shows all tweets in the app
    
    Parameters:
        -

    returns a json list with all tweets in the app, with the following keys
        -tweet_id  : UUID
        -content   : str
        -create_at : datetime
        -update_at : Optional[datetime]
        -by        : User
    """
    with open("tweets.json", "r", encoding= "utf-8") as f:
        results = json.loads(f.read())
        return results
    

### Post a Tweet
@app.post(
    path="/post",
    response_model = Tweet,
    status_code = status.HTTP_201_CREATED,
    summary = "Post a tweet",
    tags = ["Tweets"]

    )

def post(tweet: Tweet = Body(...)):
    """
    Post a Tweet

    This path operation post a tweet in the app

    Parameters:
        - Request body parameter
            - tweet: Tweet

    Returns a json with the basic tweet information:
        -tweet_id  : UUID
        -content   : str
        -create_at : datetime
        -update_at : Optional[datetime]
        -by        : User
   
    """
    with open("tweets.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["create_at"] = str(tweet_dict["create_at"])
        tweet_dict["update_at"] = str(tweet_dict["update_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

        results.append(tweet_dict)
        with open("tweets.json", "w", encoding="utf-8") as f:
            f.seek(0)
            f.write(json.dumps(results))
            return tweet

### Show a Tweet
@app.get(
    path="/tweet/{tweet_id}",
    # response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Show a tweet",
    tags = ["Tweets"]

    )

def show_a_tweet(tweet_id: UUID = Path(
    ...,
    title = "Tweet ID",
    description = " this is the Tweet ID",
    example= "3fa85f64-5717-4562-b3fc-2c963f66afa8"
    )
):
    """
    Show a Tweet
    
    This path operation show if a Tweet is in the app
    
    Parameters:
        - Tweet_id : UUID

    returns a json list with the tweet in the app, with the following keys
        -tweet_id  : UUID
        -content   : str
        -create_at : datetime
        -update_at : Optional[datetime]
        -by        : User
    """
    with open("tweets.json", "r", encoding= "utf-8") as f:
        datos = json.loads(f.read())
        for tweet in datos:
            if tweet["tweet_id"] == str(tweet_id) :
                return "tweet exist!!",  tweet
        
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡tweet not exist!"
              )

### Delete a Tweet
@app.delete(
    path="/tweet/{tweet_id}/delete",
    # response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Delete a tweet",
    tags = ["Tweets"]

    )

def delete_a_tweet(tweet_id: UUID = Path(
    ...,
    title = "tweet ID",
    description = " this is the tweet ID",
    example= "3fa85f64-5717-4562-b3fc-2c963f66afa1"
    )
):
    """
    Delete a Tweet
    
    This path operation delete a tweet in the app
    
    Parameters:
        - tweet_id : UUID

    returns a json list with the tweet delete, with the following keys
        -tweet_id  : UUID
        -content   : str
        -create_at : datetime
        -update_at : Optional[datetime]
        -by        : User
    """
    with open("tweets.json", "r+", encoding= "utf-8") as f:
        datos = json.loads(f.read())
        for tweet in datos:
            if tweet["tweet_id"] == str(tweet_id):
                datos.remove(tweet)
                with open("tweets.json", "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(datos))
                    return "tweet delete", tweet
                
                      
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡tweet not exist!"
              )

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