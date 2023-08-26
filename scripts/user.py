from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI()

# Mock database to store users and their API keys
users_db = {}
api_keys_db = {}


class User(BaseModel):
    username: str
    password: str


class APIKey(BaseModel):
    key: str


class DataItem(BaseModel):
    id: str
    content: str


# Function to create a new user
def create_user(user: User):
    user_id = str(uuid.uuid4())
    users_db[user_id] = user
    return user_id


# Function to generate a new API key for a user
def generate_api_key(user_id: str):
    api_key = str(uuid.uuid4())
    api_keys_db[api_key] = user_id
    return api_key


# Function to get user ID from API key
def get_user_id_from_api_key(api_key: str):
    return api_keys_db.get(api_key)


# Mock data storage in memory
data_storage = {}


# Function to store data
def store_data(user_id: str, data: DataItem):
    if user_id not in data_storage:
        data_storage[user_id] = []
    data_storage[user_id].append(data)


# Route to create a new user
@app.post("/users/")
def create_new_user(user: User):
    user_id = create_user(user)
    api_key = generate_api_key(user_id)
    return {"user_id": user_id, "api_key": api_key}


# Route to store data using API key authentication
@app.post("/store/")
def store_data_with_auth(data: DataItem, api_key: str = Header(...)):
    user_id = get_user_id_from_api_key(api_key)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid API key")
    store_data(user_id, data)
    return {"message": "Data stored successfully"}


# Route to retrieve stored data for a user
@app.get("/data/")
def get_stored_data(user_id: str):
    user_data = data_storage.get(user_id, [])
    return user_data


# Testing route to retrieve all stored data (for demonstration purposes)
@app.get("/all_data/")
def get_all_stored_data():
    return data_storage
