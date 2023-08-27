import time
from enum import Enum
from typing import Any, Union


DATABASE_TIMEOUT = 5 * 60 * 60
# DATABASE_TIMEOUT = 300


def NOW():
    return int(time.time())


class ErrorCode(Enum):
    identifier_exists = "identifier_exists"
    identifier_too_long = "identifier_too_long"


class Json(dict):
    message: str
    code: str
    error: bool
    data: Any

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, kwargs):
        self.__dict__.update(**kwargs)


class Path:
    def __init__(self, path: str):
        self.raw_path = path
        self.root, children = path.split("/", 1)
        self.child: Union[Path, None] = Path(children) if children else None

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(raw_path={self.raw_path})"

    @classmethod
    def get_path(cls, path: str) -> Union["Path", None]:
        path = path.strip().rstrip()
        if path:
            return cls(path + "/")
