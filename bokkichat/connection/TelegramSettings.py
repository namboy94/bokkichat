"""LICENSE
Copyright 2018 Hermann Krumrey <hermann@krumreyh.com>

This file is part of bokkichat.

bokkichat is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

bokkichat is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with bokkichat.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import json
from bokkichat.connection.Settings import Settings


class TelegramSettings(Settings):
    """
    Class that defines a Settings object for a Telegram connection
    """

    def __init__(
            self,
            api_id: str,
            api_hash: str,
            session_name: str = "bokkichat"
    ):
        """
        Initializes the Telegram Connection.
        :param api_id: The API ID
        :param api_hash: The API hash
        :param session_name: The name of the telethon session
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name

    # noinspection PyMethodMayBeStatic
    def serialize(self) -> str:
        """
        Serializes the settings to a string
        :return: The serialized Settings object
        """
        return json.dumps({
            "api_id": self.api_id,
            "api_hash": self.api_hash,
            "session_name": self.session_name
        })

    @classmethod
    def deserialize(cls, serialized: str):
        """
        Deserializes a string and generates a Settings object from it
        :param serialized: The serialized string
        :return: The deserialized Settings object
        """
        obj = json.loads(serialized)
        return cls(obj["api_id"], obj["api_hash"], obj["session_name"])
