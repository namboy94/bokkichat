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

from bokkichat.message.Message import Message
from bokkichat.address.Address import Address


class TextMessage(Message):
    """
    Class that defines an interface for text messages.
    Each text message has a title and a body.
    Some chat services don't allow titles for messages, in those cases,
    the title will be blank.
    """

    def __init__(
            self,
            sender: Address,
            receiver: Address,
            body: str,
            title: str = ""
    ):
        """
        Initializes the TextMessage object
        :param sender: The sender of the message
        :param receiver: The receiver of the message
        :param body: The message body
        :param title: The title of the message. Defaults to an empty string
        """
        super().__init__(sender, receiver)
        self.body = body
        self.title = title