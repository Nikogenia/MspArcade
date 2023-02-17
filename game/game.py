# Standard
from dataclasses import dataclass
from typing import Self, Any


@dataclass
class Game:

    name: str
    type: str
    short_description: str
    description: str
    author: str
    image_name: str
    data: dict[str, Any]

    def json(self) -> dict:

        return {
            "name": self.name,
            "type": self.type,
            "short_description": self.short_description,
            "description": self.description,
            "author": self.author,
            "image_name": self.image_name
        } | self.data

    @classmethod
    def from_json(cls, data: dict) -> Self:

        fields = {"name": str, "type": str, "short_description": str, "description": str, "author": str, "image_name": str}
        optional_fields = {"url": str}

        for f_name, f_type in fields.items():
            if f_name not in data:
                return None
            if not isinstance(data[f_name], f_type):
                return None
        for f_name, f_type in optional_fields.items():
            if f_name in data and not isinstance(data[f_name], f_type):
                return None

        optional = {}
        for f_name, f_value in data.items():
            if f_name not in fields:
                optional[f_name] = f_value

        return cls(data["name"], data["type"], data["short_description"], data["description"], data["author"], data["image_name"], optional)