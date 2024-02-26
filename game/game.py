# Standard
from dataclasses import dataclass
from typing import Self, Any
from logging import Logger


@dataclass(slots=True)
class Game:

    id: int
    name: str
    type: str
    short_description: str
    short_description_split: int
    description: str
    author: str
    owners: list[int]
    image_name: str
    data: dict[str, Any]

    def json(self) -> dict:

        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "short_description": self.short_description,
            "short_description_split": self.short_description_split,
            "description": self.description,
            "author": self.author,
            "owners": self.owners,
            "image_name": self.image_name
        } | self.data

    @classmethod
    def from_json(cls, json: dict, logger: Logger) -> Self:

        # Name: Required, Type
        fields = {
            "id": ((), int),
            "name": ((), str),
            "type": ((), str),
            "short_description": ((), str),
            "short_description_split": ((), int),
            "description": ((), str),
            "author": ((), str),
            "owners": ((), list),
            "image_name": ((), str),
            "url": (("web", "makecode", "scratch"), str)
        }

        # Additional data
        data = {}

        # Type checking and fill missing fields
        game_type = ""
        for f_name, f_data in fields.items():

            # Required field
            if [t for t in f_data[0] if t == game_type] or not f_data[0]:

                # Field not available
                if f_name not in json:

                    # Log warning and fail
                    logger.warning(f"Missing field '{f_name}' on loading a game! Data: {json}")
                    return None

                # Set the type
                if f_name == "type":
                    game_type = json["type"]

                # Check for type
                if not isinstance(json[f_name], f_data[1]):
                    logger.warning(f"Invalid field type of '{f_name}' on loading a game! Data: {json}")
                    return None

                # Check for additional field
                if [t for t in f_data[0] if t == game_type]:
                    data[f_name] = json[f_name]

        return cls(json["id"], json["name"], json["type"], json["short_description"], json["short_description_split"],
                   json["description"], json["author"], json["owners"], json["image_name"], data)
