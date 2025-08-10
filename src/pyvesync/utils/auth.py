"""Contains authentication-related functions and classes."""
from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class VeSyncAuth(DataClassORJSONMixin):
    """VeSync Authentication class.

    Args:
        username (str): The username or email of the user.
        password (str): The password of the user.
        account_id (str): The account ID of the user.
        token (str): The authentication token for the user.
        country_code (str): The country code for the user's region.

    Attributes:
        base_url (str): The base URL for the API, determined by the country code.

    Methods:
        from_json_file(file: str | Path) -> VeSyncAuth:
            Load authentication data from a JSON file.
        to_json_file(file: str | Path) -> None:
            Save authentication data to a JSON file.
        to_json() -> str:
            Convert the authentication data to a JSON string.
        from_json(json_str: str) -> VeSyncAuth:
            Create an instance of VeSyncAuth from a JSON string.

    Example:
        >>> auth = VeSyncAuth(
            username="mail@example.com"
            account_id="12345",
            token="abcde",
            country_code="US"
        )
        >>> auth.to_json_file("auth.json")
        >>> loaded_auth = VeSyncAuth.from_json_file("auth.json")
        >>> assert loaded_auth == auth
        >>> auth_dict = {
            "username": "mail@example.com",
            "password": "password123",
            "account_id": "12345",
            "token": "abcde",
            "country_code": "US"
        }
        >>> assert VeSyncAuth.from_dict(auth_dict) == auth

    """
    username: str
    password: str
    account_id: str
    token: str
    country_code: str

    @classmethod
    def from_json_file(cls, file: str | Path) -> VeSyncAuth:
        """Load authentication data from a file.

        Args:
            file (str | Path): The path to the JSON file containing authentication data.

        Returns:
            VeSyncAuth: An instance of VeSyncAuth initialized with the data from the file.
        """
        if isinstance(file, str):
            file = Path(file)
        if not file.exists():
            raise FileNotFoundError(f"Authentication file {file} does not exist.")
        return cls.from_json(file.read_text(encoding='utf-8'))

    def to_json_file(self, file: str | Path) -> None:
        """Save authentication data to a file."""
        if isinstance(file, str):
            file = Path(file)
        file.write_text(self.to_json(), encoding='utf-8')
        if not file.exists():
            raise FileNotFoundError(f"Failed to write authentication data to {file}.")
