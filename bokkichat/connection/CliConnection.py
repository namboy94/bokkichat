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

from typing import List
from bokkichat.address.Address import Address
from bokkichat.message.Message import Message
from bokkichat.message.TextMessage import TextMessage
from bokkichat.connection.Connection import Connection


class CliConnection(Connection):
    """
    Class that implements a CLI connection which can be used in testing
    """

    @property
    def address(self) -> Address:
        """
        A CLI connection has no real address, so a dummy address is generated.
        :return: The address of the connection
        """
        return Address("CLI")

    # noinspection PyMethodMayBeStatic
    def send(self, message: Message):
        """
        Prints a "sent" message
        :param message: The message to "send"
        :return: None
        """
        print(message)

    def receive(self) -> List[Message]:
        """
        A CLI Connection receives messages by listening to the input
        :return: A list of pending Message objects
        """
        return [TextMessage(self.address, self.address, input())]

    def close(self):
        """
        Disconnects the Connection.
        :return: None
        """
        pass