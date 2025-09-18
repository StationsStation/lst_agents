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

"""Serialization module for user_interaction protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import cast

from aea.mail.base_pb2 import DialogueMessage
from aea.mail.base_pb2 import Message as ProtobufMessage
from aea.protocols.base import Message, Serializer

from packages.eightballer.protocols.user_interaction import user_interaction_pb2
from packages.eightballer.protocols.user_interaction.custom_types import ErrorCode
from packages.eightballer.protocols.user_interaction.message import (
    UserInteractionMessage,
)


class UserInteractionSerializer(Serializer):
    """Serialization for the 'user_interaction' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'UserInteraction' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(UserInteractionMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        user_interaction_msg = user_interaction_pb2.UserInteractionMessage()

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == UserInteractionMessage.Performative.NOTIFICATION:
            performative = user_interaction_pb2.UserInteractionMessage.Notification_Performative()  # type: ignore
            body = msg.body
            performative.body = body
            if msg.is_set("title"):
                performative.title_is_set = True
                title = msg.title
                performative.title = title
            if msg.is_set("attach"):
                performative.attach_is_set = True
                attach = msg.attach
                performative.attach = attach
            user_interaction_msg.notification.CopyFrom(performative)
        elif performative_id == UserInteractionMessage.Performative.USER_COMMAND:
            performative = user_interaction_pb2.UserInteractionMessage.User_Command_Performative()  # type: ignore
            command = msg.command
            performative.command = command
            if msg.is_set("data"):
                performative.data_is_set = True
                data = msg.data
                performative.data.update(data)
            user_interaction_msg.user_command.CopyFrom(performative)
        elif (
            performative_id == UserInteractionMessage.Performative.REQUEST_CONFIRMATION
        ):
            performative = user_interaction_pb2.UserInteractionMessage.Request_Confirmation_Performative()  # type: ignore
            message = msg.message
            performative.message = message
            user_interaction_msg.request_confirmation.CopyFrom(performative)
        elif performative_id == UserInteractionMessage.Performative.USER_CONFIRMATION:
            performative = user_interaction_pb2.UserInteractionMessage.User_Confirmation_Performative()  # type: ignore
            confirmed = msg.confirmed
            performative.confirmed = confirmed
            user_interaction_msg.user_confirmation.CopyFrom(performative)
        elif performative_id == UserInteractionMessage.Performative.ERROR:
            performative = user_interaction_pb2.UserInteractionMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            if msg.is_set("error_data"):
                performative.error_data_is_set = True
                error_data = msg.error_data
                performative.error_data.update(error_data)
            user_interaction_msg.error.CopyFrom(performative)
        elif performative_id == UserInteractionMessage.Performative.END:
            performative = user_interaction_pb2.UserInteractionMessage.End_Performative()  # type: ignore
            user_interaction_msg.end.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = user_interaction_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'UserInteraction' message.

        :param obj: the bytes object.
        :return: the 'UserInteraction' message.
        """
        message_pb = ProtobufMessage()
        user_interaction_pb = user_interaction_pb2.UserInteractionMessage()
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        user_interaction_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = user_interaction_pb.WhichOneof("performative")
        performative_id = UserInteractionMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == UserInteractionMessage.Performative.NOTIFICATION:
            body = user_interaction_pb.notification.body
            performative_content["body"] = body
            if user_interaction_pb.notification.title_is_set:
                title = user_interaction_pb.notification.title
                performative_content["title"] = title
            if user_interaction_pb.notification.attach_is_set:
                attach = user_interaction_pb.notification.attach
                performative_content["attach"] = attach
        elif performative_id == UserInteractionMessage.Performative.USER_COMMAND:
            command = user_interaction_pb.user_command.command
            performative_content["command"] = command
            if user_interaction_pb.user_command.data_is_set:
                data = user_interaction_pb.user_command.data
                data_dict = dict(data)
                performative_content["data"] = data_dict
        elif (
            performative_id == UserInteractionMessage.Performative.REQUEST_CONFIRMATION
        ):
            message = user_interaction_pb.request_confirmation.message
            performative_content["message"] = message
        elif performative_id == UserInteractionMessage.Performative.USER_CONFIRMATION:
            confirmed = user_interaction_pb.user_confirmation.confirmed
            performative_content["confirmed"] = confirmed
        elif performative_id == UserInteractionMessage.Performative.ERROR:
            pb2_error_code = user_interaction_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            error_msg = user_interaction_pb.error.error_msg
            performative_content["error_msg"] = error_msg
            if user_interaction_pb.error.error_data_is_set:
                error_data = user_interaction_pb.error.error_data
                error_data_dict = dict(error_data)
                performative_content["error_data"] = error_data_dict
        elif performative_id == UserInteractionMessage.Performative.END:
            pass
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return UserInteractionMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content
        )
