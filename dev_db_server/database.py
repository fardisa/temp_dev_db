from .core import Json, NOW, Path, DATABASE_TIMEOUT, Any, Union


def save_t():
    from .persist import save_t

    save_t()


class Database(Json):
    name: str
    description: str
    created_timestamp: int
    expiration_timestamp: int
    data: Json

    def __init__(self, name: str, description: str = "") -> None:
        super().__init__(
            name=name,
            description=description,
            created_timestamp=NOW(),
            data=Json(),
        )

    @property
    def expiration_timestamp(self) -> int:
        return self.created_timestamp + DATABASE_TIMEOUT

    @property
    def remaining_timestamp(self) -> int:
        return self.expiration_timestamp - NOW()

    @property
    def valid(self) -> bool:
        return NOW() <= self.expiration_timestamp

    @property
    def details(self) -> Json:
        copy = self.copy()
        del copy["data"]
        copy.update(
            expiration_timestamp=self.expiration_timestamp,
            remaining_timestamp=self.remaining_timestamp,
        )
        return copy

    def get_data(self, path: Path) -> bool:
        response = Json(
            error=True,
            message=f"provided path: `{path.raw_path}` does not exist in database: `{self.name}`",
            code="invalid_path",
        )

        seen_path: Union[Path, None] = path
        data: Any = self.data
        valid = False

        while True:
            if isinstance(data, Json):
                if seen_path.root in data:
                    data = data[seen_path.root]

                    if seen_path.child:
                        if isinstance(data, Json):
                            seen_path = seen_path.child
                        else:
                            break

                    else:
                        valid = True

                else:
                    break

            else:
                break

        if valid:
            response.update(
                data=data,
                remaining_timestamp=self.remaining_timestamp,
                code="path_found",
                message="path is found and returned",
                error=False,
            )

        return response

    def set_data(self, path: Path, data: Any) -> bool:
        response = Json(
            error=True,
            message=f"provided path: `{path.raw_path}` does not exist in database: `{self.name}`",
            code="invalid_path",
        )

        seen_path: Union[Path, None] = path
        set_data: Any = self.data

        while True:
            valid = False
            if seen_path.root in set_data:
                sub_data = set_data[seen_path.root]

                if seen_path.child:
                    if isinstance(sub_data, Json):
                        set_data = sub_data
                        seen_path = seen_path.child
                    else:
                        break

                else:
                    valid = True

            elif not seen_path.child:
                valid = True

            else:
                break

            if valid:
                set_data[seen_path.root] = data

                save_t()

                response.update(
                    message="data set successfully",
                    code="set_made",
                    remaining_timestamp=self.remaining_timestamp,
                    error=False,
                )
                break

        return response

    def delete_data(self, path: Path) -> bool:
        response = Json(
            error=True,
            message=f"provided path: `{path.raw_path}` does not exist in database: `{self.name}`",
            code="invalid_path",
        )

        seen_path: Union[Path, None] = path
        data: Any = self.data

        while True:
            valid = False
            if seen_path.root in data:
                sub_data = data[seen_path.root]

                if seen_path.child:
                    if isinstance(sub_data, Json):
                        data = sub_data
                        seen_path = seen_path.child
                    else:
                        break

                else:
                    del data[seen_path.root]
                    valid = True

            else:
                break

            if valid:
                response.update(
                    message="data deleted successfully",
                    code="delete_made",
                    error=False,
                ),
                break

        return response
