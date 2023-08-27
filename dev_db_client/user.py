from typing import Any, Union
import requests
from .core import Base, Json
from .response import *


class User:
    dev_db_url = "http://127.0.0.1:8000"

    @classmethod
    def req(
        cls,
        path: str,
        response_class: Response,
        get: bool = True,
        **kwargs,
    ) -> Response:
        func = requests.get if get else requests.post

        response = func(
            f"{cls.dev_db_url}/{path}",
            **kwargs,
        )

        if response.status_code == 200:
            json = response.json(object_hook=Json)
            return response_class(json)
        else:
            raise Exception(response.reason)

    @classmethod
    def create_user(cls, identifier: str) -> Union["User", UserResponse]:
        response = cls.req(
            "create_user",
            UserResponse,
            params=Json(identifier=identifier),
        )
        if not response.error:
            return cls(response.identifier, response.api_key)
        else:
            return response

    @classmethod
    def get_users(cls, identifier: str) -> Json:
        return cls.req(
            "get_users",
            lambda json: json,
            params=Json(identifier=identifier),
        )

    def __init__(self, identifier: str, api_key: str) -> None:
        super().__init__()

        self.identifier = identifier
        self.api_key = api_key

    def __str__(self):
        return f"{self.__class__.__name__}(identifier={self.identifier}, api_key={self.api_key})"

    def post(
        self,
        path: str,
        response_class: Response,
        json: Json = None,
        **kwargs,
    ) -> Response:
        json = json or Json()

        return self.req(
            path,
            response_class,
            get=False,
            json=Json(
                identifier=self.identifier,
                api_key=self.api_key,
                **json,
            ),
            **kwargs,
        )

    def get_user(self) -> GetUserResponse:
        return self.post("get_user", GetUserResponse)

    def delete_user(self) -> GetUserResponse:
        return self.post("delete_user", Response)

    def create_database(
        self,
        name: str,
        description: str = "",
    ) -> CreateDatabaseResponse:
        return self.post(
            "create_database",
            CreateDatabaseResponse,
            json=Json(
                name=name,
                description=description,
            ),
        )

    def delete_database(self, name: str) -> DeleteDatabaseResponse:
        return self.post(
            "delete_database",
            DeleteDatabaseResponse,
            json=Json(name=name),
        )

    def get_data(self, path: str) -> GetDataResponse:
        return self.post(
            "get_data",
            GetDataResponse,
            json=Json(path=path),
        )

    def set_data(self, path: str, data: Any) -> SetDataResponse:
        return self.post(
            "set_data",
            SetDataResponse,
            json=Json(path=path, data=data),
        )

    def delete_data(self, path: str) -> DeleteDataResponse:
        return self.post(
            "delete_data",
            DeleteDataResponse,
            json=Json(path=path),
        )
