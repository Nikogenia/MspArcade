# Standard
from dataclasses import dataclass
from typing import Self
from logging import Logger


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
    def from_json(cls, json: dict, logger: Logger) -> Self:

        # Name: Type, Default (None for error)
        fields = {
            "id": (int, None),
            "name": (str, "Unknown User"),
            "last_login": (int, 0)
        }

        # Type checking and fill missing fields
        for f_name, f_data in fields.items():

            # Field not available
            if f_name not in json:

                # Log warning
                logger.warning(f"Missing field '{f_name}' on loading a user! Data: {json}")

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

        return cls(json["id"], json["name"], json["last_login"])
