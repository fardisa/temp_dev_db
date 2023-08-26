import hashlib, uuid, time
from .database import Json, Path, Any, Union, Database, save_t


class User:
    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        self.api_key = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
        self.databases: Json[str, Database] = Json()

    def __eq__(self, user: "User"):
        if isinstance(user, User):
            return self.api_key == user.api_key and self.identifier == user.identifier
        return False

    @property
    def details(self) -> Json:
        json = Json(
            identifier=self.identifier,
            api_key=self.api_key,
            database_details={
                database.name: database.details for database in self.databases.values()
            },
        )
        return json

    def create_database(
        self,
        name: str,
        description: str = "",
    ) -> Json:
        response = Json(
            message=f"given name for database: `{name}` already exists",
            code="database_already_exists",
            error=True,
        )

        if name not in self.databases:
            database = Database(name, description)
            self.databases[name] = database

            save_t()

            response.update(
                message=f"database `{name}` created successfully",
                code="database_created",
                error=False,
                **database.details,
            )

        return response

    def delete_database(self, name: str) -> Json:
        response = Json(
            message=f"given name for database: `{name}` doesn't exists",
            code="database_non_exist",
            error=True,
        )

        if name in self.databases:
            del self.databases[name]

            save_t()

            response.update(
                message=f"database: `{name}` deleted successfully",
                code="database_deleted",
                error=False,
                name=name,
            )

        return response

    def get_data(self, path: str) -> Json:
        response = Json(
            error=True,
            message=f"provided path: `{path}` does not exist in a database",
            code="invalid_path",
        )

        path = Path.get_path(path)

        if path != None:
            database: Union[Database, None] = self.databases.get(path.root)

            if isinstance(database, Database):
                if not path.child:
                    response.update(
                        path=path.raw_path,
                        data=database.data,
                        remaining_timestamp=database.remaining_timestamp,
                        error=False,
                        code="path_found",
                        message="path is found and returned",
                    )
                else:
                    response = database.get_data(path.child)
            else:
                response.update(
                    message=f"database: `{path.root}` does not exists",
                    code="database_non_exist",
                )

        return response

    def set_data(self, path: str, data: Any) -> Json:
        response = Json(
            error=True,
            message=f"provided path: `{path}` does not exist in database",
            code="invalid_path",
        )

        path = Path.get_path(path)

        if isinstance(path, Path):
            database: Union[Database, None] = self.databases.get(path.root)

            if isinstance(database, Database):
                if not path.child:
                    database.data = data

                    save_t()

                    response.update(
                        path=path.raw_path,
                        message="data set successfully",
                        code="set_made",
                        remaining_timestamp=database.remaining_timestamp,
                        error=False,
                    )
                else:
                    response = database.set_data(path.child, data)

            else:
                response.update(
                    message=f"database: `{path.root}` does not exists",
                    code="database_non_exist",
                )

        return response

    def delete_data(self, path: str) -> Json:
        response = Json(
            error=True,
            message=f"provided path: `{path}` does not exist in database",
            code="invalid_path",
        )

        path = Path.get_path(path)

        if isinstance(path, Path):
            database: Union[Database, None] = self.databases.get(path.root)

            if isinstance(database, Database):
                if not path.child:
                    del self.databases[path.root]

                    save_t()

                    response.update(
                        path=path.raw_path,
                        message="data deleted successfully",
                        code="delete_made",
                        error=False,
                    )
                else:
                    response = database.delete_data(path.child)

            else:
                response.update(
                    message=f"database: `{path.root}` does not exists",
                    code="database_non_exist",
                )

        return response


class Users:
    users_by_identifier: Json[str, User] = Json()
    users_by_api_key: Json[str, User] = Json()
    watching = True

    @classmethod
    def watch(cls):
        while cls.watching:
            for user in cls.users_by_identifier.values():
                user: User
                databases: dict[str, Database] = user.databases.copy()

                for name, database in databases.items():
                    if not database.valid:
                        del user.databases[name]

                        print(f"Database: `{user.identifier}::{name}` deleted")
                        save_t()

    @classmethod
    def unwatch(cls):
        cls.watching = False
        save_t()

    @classmethod
    def is_user(cls, user: Union[User, None]) -> bool:
        return isinstance(user, User)

    @classmethod
    def create_user(cls, identifier: str):
        response = Json(error=True)
        identifier = identifier.strip()

        if identifier in cls.users_by_identifier:
            response.message = f"given identifier: `{identifier}` already exists"
            response.code = "identifier_exists"

        elif len(identifier) > 20:
            response.message = f"given identifier: `{identifier}` is too long, valid length for an identifier is 20"
            response.code = "identifier_too_long"
        else:
            user = User(identifier)

            cls.users_by_identifier[identifier] = user
            cls.users_by_api_key[user.api_key] = user

            save_t()

            response.update(
                message="User created successfully",
                identifier=user.identifier,
                api_key=user.api_key,
                code="created_user",
                error=False,
            )

        return response

    @classmethod
    def __get_user(cls, identifier: str, api_key: str) -> Union[User, None]:
        identifier = identifier.strip()

        user_by_api_key: Union[User, None] = cls.users_by_api_key.get(api_key)
        user_by_identifier: Union[User, None] = cls.users_by_identifier.get(identifier)

        # hack
        # user_by_api_key: User = user_by_identifier

        if (
            cls.is_user(user_by_api_key)
            and cls.is_user(user_by_identifier)
            and (user_by_api_key == user_by_identifier)
        ):
            return user_by_api_key

    @classmethod
    def get_user(cls, identifier: str, api_key: str):
        response = Json(error=True)
        user: Union[User, None] = cls.__get_user(identifier, api_key)

        if cls.is_user(user):
            response.update(
                error=False,
                message="user is found",
                code="user_found",
                **user.details,
            )

        else:
            response.update(
                message=f"provided identifier: `{identifier}` or api_key in path is invalid",
                code="invalid_identifier_or_api_key",
            )

        return response

    @classmethod
    def create_database(
        cls,
        identifier: str,
        api_key: str,
        name: str,
        description: str = "",
    ):
        response = cls.get_user(identifier, api_key)

        if not response.error:
            user: Union[User, None] = cls.__get_user(identifier, api_key)

            if cls.is_user(user):
                response = user.create_database(name, description)

        return response

    @classmethod
    def delete_database(
        cls,
        identifier: str,
        api_key: str,
        name: str,
    ):
        response = cls.get_user(identifier, api_key)

        if not response.error:
            user: Union[User, None] = cls.__get_user(identifier, api_key)

            if cls.is_user(user):
                response = user.delete_database(name)

        return response

    @classmethod
    def get_data(cls, identifier: str, api_key: str, path: str):
        response = cls.get_user(identifier, api_key)

        if not response.error:
            user: Union[User, None] = cls.__get_user(identifier, api_key)

            if cls.is_user(user):
                response = user.get_data(path)
                response.path = path

        return response

    @classmethod
    def set_data(
        cls,
        identifier: str,
        api_key: str,
        path: str,
        data: Any,
    ):
        response = cls.get_user(identifier, api_key)

        if not response.error:
            user: Union[User, None] = cls.__get_user(identifier, api_key)

            if cls.is_user(user):
                response = user.set_data(path, data)
                response.path = path

        return response

    @classmethod
    def delete_data(
        cls,
        identifier: str,
        api_key: str,
        path: str,
    ):
        response = cls.get_user(identifier, api_key)

        if not response.error:
            user: Union[User, None] = cls.__get_user(identifier, api_key)

            if cls.is_user(user):
                response = user.delete_data(path)
                response.path = path

        return response
