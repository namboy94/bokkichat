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

import time
# noinspection PyPackageRequirements
import telegram
import requests
from typing import Callable, List
from bokkichat.address.Address import Address
from bokkichat.message.Message import Message
from bokkichat.message.TextMessage import TextMessage
from bokkichat.message.MediaType import MediaType
from bokkichat.message.MediaMessage import MediaMessage
from bokkichat.connection.Connection import Connection
from bokkichat.connection.TelegramSettings import TelegramSettings


class TelegramConnection(Connection):
    """
    Class that implements a Telegram connection
    """

    def __init__(self, settings: TelegramSettings):
        """
        Initializes the connection, with credentials provided by a
        Settings object.
        :param settings: The settings for the connection
        """
        super().__init__(settings)
        self.bot = telegram.Bot(settings.api_key)

        try:
            self.update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            self.update_id = 0

    @property
    def address(self) -> Address:
        """
        A connection must be able to specify its own address
        :return: The address of the connection
        """
        return Address(str(self.bot.id))

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
                self.bot.send_message(
                    chat_id=message.receiver.address,
                    text=message.body
                )
            elif isinstance(message, MediaMessage):

                with open("/tmp/bokkichat-telegram-temp", "wb") as f:
                    f.write(message.data)
                tempfile = open("/tmp/bokkichat-telegram-temp", "rb")

                if message.media_type == MediaType.IMAGE:
                    self.bot.send_photo(
                        chat_id=message.receiver.address,
                        photo=tempfile,
                        caption=message.caption
                    )
                elif message.media_type == MediaType.AUDIO:
                    self.bot.send_audio(
                        chat_id=message.receiver.address,
                        audio=tempfile,
                        caption=message.caption
                    )
                else:
                    self.bot.send_video(
                        chat_id=message.receiver.address,
                        video=tempfile,
                        caption=message.caption
                    )

                tempfile.close()

        except (telegram.error.Unauthorized, telegram.error.BadRequest):
            self.logger.info(
                "Failed to send message to {}".format(message.receiver)
            )

    def receive(self) -> List[Message]:
        """
        Receives all pending messages.
        :return: A list of pending Message objects
        """
        messages = []

        try:
            for update in self.bot.get_updates(
                    offset=self.update_id, timeout=10
            ):
                self.update_id = update.update_id + 1

                telegram_message = update.message.to_dict()
                address = Address(str(telegram_message['chat']['id']))

                self.logger.info("Received message from {}".format(address))

                if "text" in telegram_message:
                    body = telegram_message['text']
                    self.logger.debug("Message Body: {}".format(body))
                    messages.append(TextMessage(address, self.address, body))

                for media_key, media_type in {
                    "photo": MediaType.IMAGE,
                    "audio": MediaType.AUDIO,
                    "video": MediaType.VIDEO,
                    "voice": MediaType.AUDIO
                }.items():
                    if media_key in telegram_message:

                        self.logger.debug("Media Type: {}".format(media_key))

                        media_info = telegram_message[media_key]

                        if isinstance(media_info, list):

                            if len(media_info) == 0:
                                continue

                            largest = media_info[len(media_info) - 1]
                            file_id = largest["file_id"]

                        elif isinstance(media_info, dict):

                            file_id = media_info["file_id"]

                        else:
                            continue

                        file_info = self.bot.get_file(file_id)
                        resp = requests.get(file_info["file_path"])
                        data = resp.content

                        messages.append(MediaMessage(
                            address,
                            self.address,
                            media_type,
                            data,
                            telegram_message.get("caption", "")
                        ))

                        break

        except telegram.error.Unauthorized:
            # The self.bot.get_update method may cause an
            # Unauthorized Error if the bot is blocked by the user
            self.update_id += 1

        except telegram.error.TimedOut:
            pass

        return messages

    def loop(self, callback: Callable):
        """
        Starts a loop that periodically checks for new messages, calling
        a provided callback function in the process.
        :param callback: The callback function to call for each
                         received message.
                         The callback should have the following format:
                             lambda connection, message: do_stuff()
        :return: None
        """
        while True:
            for message in self.receive():
                callback(self, message)
            time.sleep(1)
