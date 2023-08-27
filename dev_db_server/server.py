from typing import Union
from fastapi import FastAPI
from .users import *
from .persist import *
from .api_models import *


dev_db_app = FastAPI(
    on_startup=[load_t],
    on_shutdown=[Users.unwatch],
)


@dev_db_app.get("/create_user", status_code=200)
def create_user(identifier: str) -> Union[CreateUserResponse, Response]:
    return Users.create_user(identifier)


@dev_db_app.post("/delete_user", status_code=200)
def delete_user(user_request: UserRequest) -> Response:
    return Users.delete_user(
        user_request.identifier,
        user_request.api_key,
    )


@dev_db_app.post("/get_user", status_code=200)
def get_user(user_request: UserRequest) -> Union[GetUserResponse, Response]:
    return Users.get_user(
        user_request.identifier,
        user_request.api_key,
    )


@dev_db_app.get("/get_users", status_code=200)
def get_users(identifier: str) -> Union[GetUsersResponse, Response]:
    return Users.get_users(identifier)


@dev_db_app.post("/create_database", status_code=200)
def create_database(
    create_database_request: CreateDatabaseRequest,
) -> Union[CreateDatabaseResponse, Response]:
    return Users.create_database(
        create_database_request.identifier,
        create_database_request.api_key,
        create_database_request.name,
        create_database_request.description,
    )


@dev_db_app.post("/delete_database", status_code=200)
def delete_database(
    delete_database_request: DeleteDatabaseRequest,
) -> Union[DeleteDatabaseResponse, Response]:
    return Users.delete_database(
        delete_database_request.identifier,
        delete_database_request.api_key,
        delete_database_request.name,
    )


@dev_db_app.post("/get_data", status_code=200)
def get_data(
    data_request: DataRequest,
) -> Union[GetDataResponse, Response]:
    return Users.get_data(
        data_request.identifier,
        data_request.api_key,
        data_request.path,
    )


@dev_db_app.post("/set_data", status_code=200)
def set_data(set_data_request: SetDataRequest):
    return Users.set_data(
        set_data_request.identifier,
        set_data_request.api_key,
        set_data_request.path,
        set_data_request.data,
    )


@dev_db_app.post("/delete_data", status_code=200)
def delete_data(
    data_request: DataRequest,
):
    return Users.delete_data(
        data_request.identifier,
        data_request.api_key,
        data_request.path,
    )
