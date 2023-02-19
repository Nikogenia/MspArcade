# Standard
from dataclasses import dataclass
from typing import Self


@dataclass
class Player:

    user_id: int

    id: int
    auth_id: str
    name: str
    created: int

    time: int

    ratings: dict[int, int]

    def json(self) -> dict:

        return {
            "user_id": self.user_id,

            "id": self.id,
            "auth_id": self.auth_id,
            "name": self.name,
            "created": self.created,
            
            "time": self.time,

            "ratings": self.ratings
        }

    @classmethod
    def from_json(cls, data: dict) -> Self:

        fields = {"user_id": int, "id": int, "auth_id": str, "name": str, "created": int, "time": int, "ratings": dict}

        for f_name, f_type in fields.items():
            if f_name not in data:
                return None
            if not isinstance(data[f_name], f_type):
                return None

        return cls(data["user_id"], data["id"], data["auth_id"], data["name"], data["created"], data["time"], data["ratings"])
