from enum import Enum
from typing import Any
from .core import Json, Base


class ResponseCode(Enum):
    identifier_exists = "identifier_exists"
    identifier_too_long = "identifier_too_long"
    invalid_identifier_or_api_key = "invalid_identifier_or_api_key"
    invalid_path = "invalid_path"
    path_found = "path_found"
    user_found = "user_found"
    database_already_exists = "database_already_exists"
    created_user = "created_user"
    database_deleted = "database_deleted"
    database_created = "database_created"
    database_non_exist = "database_non_exist"
    set_made = "set_made"
    delete_made = "delete_made"


class Response(Base):
    def __init__(self, json: Json):
        self.message = json.message
        self.error = json.error
        self.code = ResponseCode[json.code]


class Database:
    def __init__(self, json: Json):
        self.name: str = json.name
        self.description: str = json.description
        self.created_timestamp: int = json.created_timestamp
        self.expiration_timestamp: int = json.expiration_timestamp
        self.remaining_timestamp: int = json.remaining_timestamp


class UserResponse(Response):
    def __init__(self, json: Json):
        super().__init__(json)

        self.identifier = json.identifier
        self.api_key = json.api_key


class GetUserResponse(UserResponse):
    def __init__(self, json: Json):
        super().__init__(json)

        database_details = json.database_details or Json()
        self.database_details: Json = {
            k: Database(v) for k, v in database_details.items()
        }


class CreateDatabaseResponse(Response, Database):
    def __init__(self, json: Json):
        Response.__init__(self, json)
        Database.__init__(self, json)


class DeleteDatabaseResponse(Response):
    def __init__(self, json: Json):
        super().__init__(json)

        self.name = json.name


class SetDataResponse(Response):
    def __init__(self, json: Json):
        super().__init__(json)

        self.path: str = json.path
        self.remaining_timestamp: int = json.remaining_timestamp


class DeleteDataResponse(SetDataResponse):
    ...


class GetDataResponse(SetDataResponse):
    def __init__(self, json: Json):
        super().__init__(json)

        self.data: Any = json.data
