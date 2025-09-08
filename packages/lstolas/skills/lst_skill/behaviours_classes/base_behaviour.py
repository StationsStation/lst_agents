"""Base behaviour module."""

import json
from abc import ABC
from enum import Enum
from typing import Any

from aea.contracts.base import Contract
from aea.skills.behaviours import State

from packages.lstolas.skills.lst_skill.models import LstStrategy


class LstabciappEvents(Enum):
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

    _state: LstabciappStates = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._event = None
        self._is_done = False  # Initially, the state is not done

    def is_done(self) -> bool:
        """Is done."""
        return self._is_done

    @property
    def event(self) -> str | None:
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

    def load_abi(self, contract: Contract) -> list:
        """Load the ABI of a contract."""
        abi_path = contract.configuration.directory / contract.configuration.contract_interface_paths["ethereum"]
        with open(abi_path, encoding="utf-8") as json_file:
            abi = json.load(json_file)
        return abi.get("abi", [])
