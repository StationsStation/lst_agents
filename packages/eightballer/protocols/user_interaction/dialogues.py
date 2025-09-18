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

"""
This module contains the classes required for user_interaction dialogue management.

- UserInteractionDialogue: The dialogue class maintains state of a dialogue and manages it.
- UserInteractionDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import Callable, Dict, FrozenSet, Type, cast

from aea.common import Address
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, DialogueLabel, Dialogues
from aea.skills.base import Model

from packages.eightballer.protocols.user_interaction.message import (
    UserInteractionMessage,
)


class UserInteractionDialogue(Dialogue):
    """The user_interaction dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            UserInteractionMessage.Performative.NOTIFICATION,
            UserInteractionMessage.Performative.USER_COMMAND,
        }
    )
    TERMINAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            UserInteractionMessage.Performative.END,
            UserInteractionMessage.Performative.ERROR,
        }
    )
    VALID_REPLIES: Dict[Message.Performative, FrozenSet[Message.Performative]] = {
        UserInteractionMessage.Performative.END: frozenset(),
        UserInteractionMessage.Performative.ERROR: frozenset(),
        UserInteractionMessage.Performative.NOTIFICATION: frozenset(
            {
                UserInteractionMessage.Performative.USER_COMMAND,
                UserInteractionMessage.Performative.REQUEST_CONFIRMATION,
                UserInteractionMessage.Performative.ERROR,
                UserInteractionMessage.Performative.END,
            }
        ),
        UserInteractionMessage.Performative.REQUEST_CONFIRMATION: frozenset(
            {
                UserInteractionMessage.Performative.USER_CONFIRMATION,
                UserInteractionMessage.Performative.ERROR,
            }
        ),
        UserInteractionMessage.Performative.USER_COMMAND: frozenset(
            {
                UserInteractionMessage.Performative.NOTIFICATION,
                UserInteractionMessage.Performative.REQUEST_CONFIRMATION,
                UserInteractionMessage.Performative.ERROR,
            }
        ),
        UserInteractionMessage.Performative.USER_CONFIRMATION: frozenset(
            {
                UserInteractionMessage.Performative.END,
                UserInteractionMessage.Performative.ERROR,
            }
        ),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a user_interaction dialogue."""

        AGENT = "agent"
        USER = "user"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a user_interaction dialogue."""

        END = 0
        ERROR = 1

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: Type[UserInteractionMessage] = UserInteractionMessage,
    ) -> None:
        """
        Initialize a dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param self_address: the address of the entity for whom this dialogue is maintained
        :param role: the role of the agent this dialogue is maintained for
        :param message_class: the message class used
        """
        Dialogue.__init__(
            self,
            dialogue_label=dialogue_label,
            message_class=message_class,
            self_address=self_address,
            role=role,
        )


class BaseUserInteractionDialogues(Dialogues, ABC):
    """This class keeps track of all user_interaction dialogues."""

    END_STATES = frozenset(
        {UserInteractionDialogue.EndState.END, UserInteractionDialogue.EndState.ERROR}
    )

    _keep_terminal_state_dialogues = True

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role],
        dialogue_class: Type[UserInteractionDialogue] = UserInteractionDialogue,
    ) -> None:
        """
        Initialize dialogues.

        :param self_address: the address of the entity for whom dialogues are maintained
        :param dialogue_class: the dialogue class used
        :param role_from_first_message: the callable determining role from first message
        """
        Dialogues.__init__(
            self,
            self_address=self_address,
            end_states=cast(FrozenSet[Dialogue.EndState], self.END_STATES),
            message_class=UserInteractionMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )


class UserInteractionDialogues(Model, BaseUserInteractionDialogues):
    """The dialogues class keeps track of all user_interaction dialogues."""

    def __init__(self, **kwargs: Dict):
        """Initialize dialogues."""
        Model.__init__(self, **kwargs)

        def role_from_first_message(
            message: Message, receiver_address: Address
        ) -> Dialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message

            :param message: an incoming/outgoing first message
            :param receiver_address: the address of the receiving agent
            :return: The role of the agent in this dialogue
            """
            if (
                message.performative == UserInteractionMessage.Performative.NOTIFICATION
                and message.sender != receiver_address
            ) or (
                message.performative == UserInteractionMessage.Performative.USER_COMMAND
                and message.sender == receiver_address
            ):
                return UserInteractionDialogue.Role.AGENT

            return UserInteractionDialogue.Role.USER

        BaseUserInteractionDialogues.__init__(
            self,
            self_address=str(self.skill_id),
            role_from_first_message=role_from_first_message,
        )
