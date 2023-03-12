# Standard
from dataclasses import dataclass
from typing import Self
from logging import Logger

# Local
from constants import DEFAULT_TIME


@dataclass
class Player:

    user_id: int

    id: int
    auth_id: str
    name: str
    created: int

    time: int

    ratings: dict[str, int]

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
    def from_json(cls, json: dict, logger: Logger) -> Self:

        # Name: Type, Default (None for error)
        fields = {
            "user_id": (int, None),
            "id": (int, None),
            "auth_id": (str, None),
            "name": (str, "Unknown Player"),
            "created": (int, 0),
            "time": (int, DEFAULT_TIME),
            "ratings": (dict, {})
        }

        # Type checking and fill missing fields
        for f_name, f_data in fields.items():

            # Field not available
            if f_name not in json:

                # Log warning
                logger.warning(f"Missing field '{f_name}' on loading a player! Data: {json}")

                # Fail on default value None
                if f_data[1] is None:
                    return None

                # Use default value
                json[f_name] = f_data[1]

            # Check for type
            if not isinstance(json[f_name], f_data[0]):

                # Log warning
                logger.warning(f"Invalid field type of '{f_name}' on loading a player! Data: {json}")

                # Fail on default value None
                if f_data[1] is None:
                    return None

                # Use default value
                json[f_name] = f_data[1]

        remove = []
        for game, value in json["ratings"].items():
            if not isinstance(value, int):
                logger.warning(f"Invalid field type of 'dict.{game}' on loading a player! Data: {json}")
                remove.append(game)
        for r in remove:
            json["ratings"].pop(r)

        return cls(json["user_id"], json["id"], json["auth_id"], json["name"],
                   json["created"], json["time"], json["ratings"])
