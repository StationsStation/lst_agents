# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 eightballer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Test messages module for user_interaction protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import List

from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.user_interaction.custom_types import ErrorCode
from packages.eightballer.protocols.user_interaction.message import (
    UserInteractionMessage,
)


class TestMessageUserInteraction(BaseProtocolMessagesTestCase):
    """Test for the 'user_interaction' protocol message."""

    MESSAGE_CLASS = UserInteractionMessage

    def build_messages(self) -> List[UserInteractionMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            UserInteractionMessage(
                performative=UserInteractionMessage.Performative.NOTIFICATION,
                title="some str",
                body="some str",
                attach="some str",
            ),
            UserInteractionMessage(
                performative=UserInteractionMessage.Performative.USER_COMMAND,
                command="some str",
                data={"some str": b"some_bytes"},
            ),
            UserInteractionMessage(
                performative=UserInteractionMessage.Performative.REQUEST_CONFIRMATION,
                message="some str",
            ),
            UserInteractionMessage(
                performative=UserInteractionMessage.Performative.USER_CONFIRMATION,
                confirmed=True,
            ),
            UserInteractionMessage(
                performative=UserInteractionMessage.Performative.ERROR,
                error_code=ErrorCode.INVALID_DATA,  # check it please!
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
            UserInteractionMessage(
                performative=UserInteractionMessage.Performative.END,
            ),
        ]

    def build_inconsistent(self) -> List[UserInteractionMessage]:  # type: ignore[override]
        """Build inconsistent messages to be used for testing."""
        return [
            UserInteractionMessage(
                performative=UserInteractionMessage.Performative.NOTIFICATION,
                # skip content: title
                attach="some str",
            ),
            UserInteractionMessage(
                performative=UserInteractionMessage.Performative.USER_COMMAND,
                # skip content: command
                data={"some str": b"some_bytes"},
            ),
            UserInteractionMessage(
                performative=UserInteractionMessage.Performative.REQUEST_CONFIRMATION,
                # skip content: message
            ),
            UserInteractionMessage(
                performative=UserInteractionMessage.Performative.USER_CONFIRMATION,
                # skip content: confirmed
            ),
            UserInteractionMessage(
                performative=UserInteractionMessage.Performative.ERROR,
                # skip content: error_code
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]
