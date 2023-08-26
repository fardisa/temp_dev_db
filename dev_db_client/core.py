from pprint import pformat


class Base:
    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        text = f"{self.class_name}("

        for k, v in self.__dict__.items():
            text += f"{k}={v}, "

        text = text[:-2] + ")"

        return text

    def __str__(self) -> str:
        return f"{self.class_name}(\n {pformat(self.__dict__, indent=4)[1:-1]}\n)\n"

    def __repr__(self) -> str:
        return f"<{self}>"


class Json(dict):
    def __getattr__(self, item):
        return self.get(item)
