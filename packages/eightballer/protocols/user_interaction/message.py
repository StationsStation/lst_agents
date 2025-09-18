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

"""This module contains user_interaction's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Dict, Optional, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message

from packages.eightballer.protocols.user_interaction.custom_types import (
    ErrorCode as CustomErrorCode,
)

_default_logger = logging.getLogger(
    "aea.packages.eightballer.protocols.user_interaction.message"
)

DEFAULT_BODY_SIZE = 4


class UserInteractionMessage(Message):
    """A protocol for handling interactive user-agent communications within applications, facilitating notifications, commands, confirmations, and error handling."""

    protocol_id = PublicId.from_str("eightballer/user_interaction:0.1.0")
    protocol_specification_id = PublicId.from_str("eightballer/user_interaction:0.1.0")

    ErrorCode = CustomErrorCode

    class Performative(Message.Performative):
        """Performatives for the user_interaction protocol."""

        END = "end"
        ERROR = "error"
        NOTIFICATION = "notification"
        REQUEST_CONFIRMATION = "request_confirmation"
        USER_COMMAND = "user_command"
        USER_CONFIRMATION = "user_confirmation"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {
        "end",
        "error",
        "notification",
        "request_confirmation",
        "user_command",
        "user_confirmation",
    }
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "attach",
            "body",
            "command",
            "confirmed",
            "data",
            "dialogue_reference",
            "error_code",
            "error_data",
            "error_msg",
            "message",
            "message_id",
            "performative",
            "target",
            "title",
        )

    def __init__(
        self,
        performative: Performative,
        dialogue_reference: Tuple[str, str] = ("", ""),
        message_id: int = 1,
        target: int = 0,
        **kwargs: Any,
    ):
        """
        Initialise an instance of UserInteractionMessage.

        :param message_id: the message id.
        :param dialogue_reference: the dialogue reference.
        :param target: the message target.
        :param performative: the message performative.
        :param **kwargs: extra options.
        """
        super().__init__(
            dialogue_reference=dialogue_reference,
            message_id=message_id,
            target=target,
            performative=UserInteractionMessage.Performative(performative),
            **kwargs,
        )

    @property
    def valid_performatives(self) -> Set[str]:
        """Get valid performatives."""
        return self._performatives

    @property
    def dialogue_reference(self) -> Tuple[str, str]:
        """Get the dialogue_reference of the message."""
        enforce(self.is_set("dialogue_reference"), "dialogue_reference is not set.")
        return cast(Tuple[str, str], self.get("dialogue_reference"))

    @property
    def message_id(self) -> int:
        """Get the message_id of the message."""
        enforce(self.is_set("message_id"), "message_id is not set.")
        return cast(int, self.get("message_id"))

    @property
    def performative(self) -> Performative:  # type: ignore # noqa: F821
        """Get the performative of the message."""
        enforce(self.is_set("performative"), "performative is not set.")
        return cast(UserInteractionMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def attach(self) -> Optional[str]:
        """Get the 'attach' content from the message."""
        return cast(Optional[str], self.get("attach"))

    @property
    def body(self) -> str:
        """Get the 'body' content from the message."""
        enforce(self.is_set("body"), "'body' content is not set.")
        return cast(str, self.get("body"))

    @property
    def command(self) -> str:
        """Get the 'command' content from the message."""
        enforce(self.is_set("command"), "'command' content is not set.")
        return cast(str, self.get("command"))

    @property
    def confirmed(self) -> bool:
        """Get the 'confirmed' content from the message."""
        enforce(self.is_set("confirmed"), "'confirmed' content is not set.")
        return cast(bool, self.get("confirmed"))

    @property
    def data(self) -> Optional[Dict[str, bytes]]:
        """Get the 'data' content from the message."""
        return cast(Optional[Dict[str, bytes]], self.get("data"))

    @property
    def error_code(self) -> CustomErrorCode:
        """Get the 'error_code' content from the message."""
        enforce(self.is_set("error_code"), "'error_code' content is not set.")
        return cast(CustomErrorCode, self.get("error_code"))

    @property
    def error_data(self) -> Optional[Dict[str, bytes]]:
        """Get the 'error_data' content from the message."""
        return cast(Optional[Dict[str, bytes]], self.get("error_data"))

    @property
    def error_msg(self) -> str:
        """Get the 'error_msg' content from the message."""
        enforce(self.is_set("error_msg"), "'error_msg' content is not set.")
        return cast(str, self.get("error_msg"))

    @property
    def message(self) -> str:
        """Get the 'message' content from the message."""
        enforce(self.is_set("message"), "'message' content is not set.")
        return cast(str, self.get("message"))

    @property
    def title(self) -> Optional[str]:
        """Get the 'title' content from the message."""
        return cast(Optional[str], self.get("title"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the user_interaction protocol."""
        try:
            enforce(
                isinstance(self.dialogue_reference, tuple),
                "Invalid type for 'dialogue_reference'. Expected 'tuple'. Found '{}'.".format(
                    type(self.dialogue_reference)
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[0], str),
                "Invalid type for 'dialogue_reference[0]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[0])
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[1], str),
                "Invalid type for 'dialogue_reference[1]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[1])
                ),
            )
            enforce(
                type(self.message_id) is int,
                "Invalid type for 'message_id'. Expected 'int'. Found '{}'.".format(
                    type(self.message_id)
                ),
            )
            enforce(
                type(self.target) is int,
                "Invalid type for 'target'. Expected 'int'. Found '{}'.".format(
                    type(self.target)
                ),
            )

            # Light Protocol Rule 2
            # Check correct performative
            enforce(
                isinstance(self.performative, UserInteractionMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == UserInteractionMessage.Performative.NOTIFICATION:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.body, str),
                    "Invalid type for content 'body'. Expected 'str'. Found '{}'.".format(
                        type(self.body)
                    ),
                )
                if self.is_set("title"):
                    expected_nb_of_contents += 1
                    title = cast(str, self.title)
                    enforce(
                        isinstance(title, str),
                        "Invalid type for content 'title'. Expected 'str'. Found '{}'.".format(
                            type(title)
                        ),
                    )
                if self.is_set("attach"):
                    expected_nb_of_contents += 1
                    attach = cast(str, self.attach)
                    enforce(
                        isinstance(attach, str),
                        "Invalid type for content 'attach'. Expected 'str'. Found '{}'.".format(
                            type(attach)
                        ),
                    )
            elif self.performative == UserInteractionMessage.Performative.USER_COMMAND:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.command, str),
                    "Invalid type for content 'command'. Expected 'str'. Found '{}'.".format(
                        type(self.command)
                    ),
                )
                if self.is_set("data"):
                    expected_nb_of_contents += 1
                    data = cast(Dict[str, bytes], self.data)
                    enforce(
                        isinstance(data, dict),
                        "Invalid type for content 'data'. Expected 'dict'. Found '{}'.".format(
                            type(data)
                        ),
                    )
                    for key_of_data, value_of_data in data.items():
                        enforce(
                            isinstance(key_of_data, str),
                            "Invalid type for dictionary keys in content 'data'. Expected 'str'. Found '{}'.".format(
                                type(key_of_data)
                            ),
                        )
                        enforce(
                            isinstance(value_of_data, bytes),
                            "Invalid type for dictionary values in content 'data'. Expected 'bytes'. Found '{}'.".format(
                                type(value_of_data)
                            ),
                        )
            elif (
                self.performative
                == UserInteractionMessage.Performative.REQUEST_CONFIRMATION
            ):
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.message, str),
                    "Invalid type for content 'message'. Expected 'str'. Found '{}'.".format(
                        type(self.message)
                    ),
                )
            elif (
                self.performative
                == UserInteractionMessage.Performative.USER_CONFIRMATION
            ):
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.confirmed, bool),
                    "Invalid type for content 'confirmed'. Expected 'bool'. Found '{}'.".format(
                        type(self.confirmed)
                    ),
                )
            elif self.performative == UserInteractionMessage.Performative.ERROR:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.error_code, CustomErrorCode),
                    "Invalid type for content 'error_code'. Expected 'ErrorCode'. Found '{}'.".format(
                        type(self.error_code)
                    ),
                )
                enforce(
                    isinstance(self.error_msg, str),
                    "Invalid type for content 'error_msg'. Expected 'str'. Found '{}'.".format(
                        type(self.error_msg)
                    ),
                )
                if self.is_set("error_data"):
                    expected_nb_of_contents += 1
                    error_data = cast(Dict[str, bytes], self.error_data)
                    enforce(
                        isinstance(error_data, dict),
                        "Invalid type for content 'error_data'. Expected 'dict'. Found '{}'.".format(
                            type(error_data)
                        ),
                    )
                    for key_of_error_data, value_of_error_data in error_data.items():
                        enforce(
                            isinstance(key_of_error_data, str),
                            "Invalid type for dictionary keys in content 'error_data'. Expected 'str'. Found '{}'.".format(
                                type(key_of_error_data)
                            ),
                        )
                        enforce(
                            isinstance(value_of_error_data, bytes),
                            "Invalid type for dictionary values in content 'error_data'. Expected 'bytes'. Found '{}'.".format(
                                type(value_of_error_data)
                            ),
                        )
            elif self.performative == UserInteractionMessage.Performative.END:
                expected_nb_of_contents = 0

            # Check correct content count
            enforce(
                expected_nb_of_contents == actual_nb_of_contents,
                "Incorrect number of contents. Expected {}. Found {}".format(
                    expected_nb_of_contents, actual_nb_of_contents
                ),
            )

            # Light Protocol Rule 3
            if self.message_id == 1:
                enforce(
                    self.target == 0,
                    "Invalid 'target'. Expected 0 (because 'message_id' is 1). Found {}.".format(
                        self.target
                    ),
                )
        except (AEAEnforceError, ValueError, KeyError) as e:
            _default_logger.error(str(e))
            return False

        return True
