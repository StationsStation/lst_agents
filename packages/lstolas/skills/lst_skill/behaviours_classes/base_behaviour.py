"""Base behaviour module."""

import json
from abc import ABC
from enum import Enum, StrEnum
from typing import Any, cast

from aea.contracts.base import Contract
from aea.skills.behaviours import State

from packages.lstolas.skills.lst_skill.models import LstStrategy, TransactionSettler
from packages.eightballer.protocols.user_interaction.message import UserInteractionMessage
from packages.eightballer.protocols.user_interaction.dialogues import UserInteractionDialogues
from packages.eightballer.connections.apprise_wrapper.connection import CONNECTION_ID as APPRISE_PUBLIC_ID


class LstabciappEvents(StrEnum):
    """Events for the fsm."""

    TRIGGER_L2_TO_L1 = "TRIGGER_L2_TO_L1"
    CLAIM_REWARDS = "CLAIM_REWARDS"
    FATAL_ERROR = "FATAL_ERROR"
    FINALIZE_BRIDGED_TOKEN = "FINALIZE_BRIDGED_TOKEN"
    DONE = "DONE"
    CALL_REDEEM = "CALL_REDEEM"
    CALL_CHECKPOINTS = "CALL_CHECKPOINTS"
    CLAIM_BRIDGED_TOKEN = "CLAIM_BRIDGED_TOKEN"
    NO_WORK = "NO_WORK"
    ERROR = "ERROR"


class LstabciappStates(Enum):
    """States for the fsm."""

    CHECKANYWORKROUND = "checkanyworkround"
    STARTROUND = "startround"
    UNHANDLEDERRORROUND = "unhandlederrorround"
    WAITINGROUND = "waitinground"
    FINALIZEBRIDGEDTOKENSROUND = "finalizebridgedtokensround"
    CLAIMBRIDGEDTOKENSROUND = "claimbridgedtokensround"
    HANDLEDERRORROUND = "handlederrorround"
    REDEEMROUND = "redeemround"
    TRIGGERL2TOL1BRIDGEROUND = "triggerl2tol1bridgeround"
    CHECKPOINTROUND = "checkpointround"
    CLAIMREWARDTOKENSROUND = "claimrewardtokensround"


class BaseState(State, ABC):
    """Base class for states."""

    _state: LstabciappStates
    _event: LstabciappEvents  # pyright: ignore

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._is_done = False  # Initially, the state is not done

    def is_done(self) -> bool:
        """Is done."""
        return self._is_done

    @property
    def event(self) -> LstabciappEvents:
        """Current event."""
        return self._event

    @property
    def log(self):
        """Get the logger from the context."""
        return self.context.logger

    def is_triggered(self) -> bool:
        """Check if the state is triggered."""
        msg = "This method should be implemented by subclasses."
        raise NotImplementedError(msg)

    @property
    def strategy(self) -> LstStrategy:
        """Get the strategy from the context."""
        return self.context.lst_strategy

    @property
    def tx_settler(self) -> TransactionSettler:
        """Get the tx settler from the context."""
        return self.context.tx_settler

    def load_abi(self, contract: Contract) -> list:
        """Load the ABI of a contract."""
        abi_path = contract.configuration.directory / contract.configuration.contract_interface_paths["ethereum"]  # pyright: ignore
        with open(abi_path, encoding="utf-8") as json_file:
            abi = json.load(json_file)
        return abi.get("abi", [])

    def send_notification_to_user(self, msg: str, attach: str | None = None, title: str | None = None) -> None:
        """Send notification to user."""
        dialogues = cast(UserInteractionDialogues, self.context.user_interaction_dialogues)
        msg, _ = dialogues.create(  # type: ignore
            counterparty=str(APPRISE_PUBLIC_ID),
            performative=UserInteractionMessage.Performative.NOTIFICATION,
            title=title,
            body=msg,
            attach=attach,
        )
        self.context.outbox.put_message(message=msg)  # type: ignore
