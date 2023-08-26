from typing import Any
from pydantic import BaseModel


# Errors
class Response(BaseModel):
    message: str
    code: str
    error: bool


# Commons Models
class DatabaseDetail(BaseModel):
    name: str
    description: str
    created_timestamp: int
    expiration_timestamp: int
    remaining_timestamp: int


# Request Models
class UserRequest(BaseModel):
    identifier: str
    api_key: str


class DataRequest(UserRequest):
    path: str


class SetDataRequest(DataRequest):
    data: Any


class DeleteDatabaseRequest(UserRequest):
    name: str


class CreateDatabaseRequest(DeleteDatabaseRequest):
    description: str


# Response Models
class CreateUserResponse(Response):
    identifier: str
    api_key: str


class GetUserResponse(Response):
    database_details: dict[str, DatabaseDetail]


class SetDataResponse(Response):
    path: str
    remaining_timestamp: int


class GetDataResponse(SetDataResponse):
    data: Any


class CreateDatabaseResponse(Response):
    name: str
    description: str
    created_timestamp: int
    expiration_timestamp: int
    remaining_timestamp: int


class DeleteDatabaseResponse(SetDataResponse):
    name: str
    dscription: str
