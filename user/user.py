# Standard
from dataclasses import dataclass
from typing import Self


@dataclass
class User:

    id: int
    name: str
    last_login: int

    def json(self) -> dict:

        return {
            "id": self.id,
            "name": self.name,
            "last_login": self.last_login
        }

    @classmethod
    def from_json(cls, data: dict) -> Self:

        fields = {"id": int, "name": str, "last_login": int}

        for f_name, f_type in fields.items():
            if f_name not in data:
                return None
            if not isinstance(data[f_name], f_type):
                return None

        return cls(data["id"], data["name"], data["last_login"])
