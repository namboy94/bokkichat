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

import os
import random
from base64 import b64decode
from unittest import TestCase
from bokkichat.message import TextMessage
from bokkichat.connection.TelegramConnection import TelegramConnection
from bokkichat.connection.TelegramSettings import TelegramSettings
from bokkichat.connection.TelegramBotConnection import TelegramBotConnection
from bokkichat.connection.TelegramBotSettings import TelegramBotSettings


class TestTelegram(TestCase):
    """
    Class that tests telegram connections, both the telethon and
    python-telegram-bot implementations. By using both, they can test each
    other.
    """

    def setUp(self):
        """
        Initializes the connections
        :return: None
        """

        api_id = os.environ["TELEGRAM_API_ID"]
        api_hash = os.environ["TELEGRAM_API_HASH"]
        bot_api_key = os.environ["TELEGRAM_BOT_API_KEY"]

        if not os.path.isfile("bokkichat.session"):
            with open("bokkichat.session", "w") as f:
                content = bytes(os.environ["TELEGRAM_SESSION"], "utf-8")
                f.write(b64decode(content).decode("utf-8"))

        self.telegram = TelegramConnection(TelegramSettings(
            api_id, api_hash, "bokkichat"
        ))
        self.telegram_bot = TelegramBotConnection(TelegramBotSettings(
            bot_api_key
        ))

    def tearDown(self):
        """
        Closes the connections
        :return: None
        """

        self.telegram.close()
        self.telegram_bot.close()

    def test_sending_text_messages(self):
        """
        Tests sending text messages from one connection to another
        :return: None
        """
        # First, test telethon -> python-telegram-bot

        text_one = "Test1 {}".format(random.randint(0, 10000))
        message_one = TextMessage(
            self.telegram.address, self.telegram_bot.address, text_one
        )
        self.telegram.send(message_one)
        received_one = self.telegram_bot.receive()[-1]  # type: TextMessage

        self.assertEqual(text_one, received_one.body)
        self.assertEqual(message_one.body, received_one.body)

        # Next, test python-telegram-bot -> telethon

        text_two = "Test2 {}".format(random.randint(0, 10000))
        message_two = TextMessage(
            self.telegram_bot.address, received_one.sender, text_two
        )
        self.telegram_bot.send(message_two)

        found = False
        for received in self.telegram.receive():  # type: TextMessage
            if received.body == text_two:
                self.assertEqual(text_two, received.body)
                self.assertEqual(message_two.body, received.body)
                found = True

        self.assertTrue(found)
