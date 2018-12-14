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

# noinspection PyPackageRequirements
from typing import List
# noinspection PyUnresolvedReferences
from telethon import TelegramClient, sync
from bokkichat.address.Address import Address
from bokkichat.message.Message import Message
from bokkichat.message.TextMessage import TextMessage
from bokkichat.message.MediaMessage import MediaMessage
from bokkichat.connection.Connection import Connection
from bokkichat.connection.TelegramSettings import TelegramSettings


class TelegramConnection(Connection):
    """
    Class that implements a Telegram connection using telethon
    """

    def __init__(self, settings: TelegramSettings):
        """
        Initializes the connection, with credentials provided by a
        Settings object.
        :param settings: The settings for the connection
        """
        super().__init__(settings)
        self.client = TelegramClient(
            settings.session_name, settings.api_id, settings.api_hash
        )
        self.client.start()

    @property
    def address(self) -> Address:
        """
        A connection must be able to specify its own address
        :return: The address of the connection
        """
        # noinspection PyUnresolvedReferences
        return Address(self.client.get_me().username)

    def send(self, message: Message):
        """
        Sends a message. A message may be either a TextMessage
        or a MediaMessage.
        :param message: The message to send
        :return: None
        """
        self.logger.info("Sending message to {}".format(message.receiver))

        try:
            if isinstance(message, TextMessage):
                self.client.send_message(
                    message.receiver.address,
                    message.body
                )
            elif isinstance(message, MediaMessage):

                # Write to file TODO: Check if this can be done with bytes
                tempfile = "/tmp/bokkichat-telegram-temp"
                with open(tempfile, "wb") as f:
                    f.write(message.data)

                self.client.send_file(
                    message.receiver.address,
                    tempfile,
                    caption=message.caption
                )

        except ValueError:
            self.logger.info(
                "Failed to send message to {}".format(message.receiver)
            )

    def receive(self) -> List[Message]:
        """
        Receives all pending messages.
        :return: A list of pending Message objects
        """
        messages = []

        # noinspection PyTypeChecker
        for dialog in self.client.get_dialogs():

            # noinspection PyTypeChecker
            for message in self.client.iter_messages(dialog.entity):

                # TODO figure out how to filter out read messages
                if not message.out:

                    address = Address(dialog.name)
                    body = message.message

                    generated = TextMessage(address, self.address, body)
                    messages.append(generated)

                    # TODO ACK

        return messages

    def close(self):
        """
        Disconnects the Connection.
        :return: None
        """
        self.client.disconnect()
