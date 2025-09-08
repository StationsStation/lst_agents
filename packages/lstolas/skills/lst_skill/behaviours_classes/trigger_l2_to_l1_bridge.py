"""Trigger the bridge from L2 to L1 if there are pending transfers."""

from enum import Enum
from typing import NamedTuple, cast

from pydantic import BaseModel

from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


class TriggerOperations(Enum):
    """Enum for the different operations that can trigger the bridge."""

    REWARD = "0x0b9821ae606ebc7c79bf3390bdd3dc93e1b4a7cda27aad60646e7b88ff55b001"
    UNSTAKE = "0x8ca9a95e41b5eece253c93f5b31eed1253aed6b145d8a6e14d913fdf8e732293"
    UNSTAKE_RETIRED = "0x9065ad15d9673159e4597c86084aff8052550cec93c5a6e44b3f1dba4c8731b3"


class AmountTuple(NamedTuple):
    """Tuple for amount and address."""

    amount: int
    address: str


class BalanceResponse(BaseModel):
    """Response model for the balance of an operation."""

    balance: AmountTuple
    receiver: AmountTuple

    @classmethod
    def from_response(cls, data: dict) -> "BalanceResponse":
        """Create a BalanceResponse from a response dictionary."""
        return cls(balance=AmountTuple(*data["balance"]), receiver=AmountTuple(*data["receiver"]))


class TriggerL2ToL1BridgeRound(BaseState):
    """This class implements the behaviour of the state TriggerL2ToL1BridgeRound."""

    _state = LstabciappStates.TRIGGERL2TOL1BRIDGEROUND
    current_operation: TriggerOperations | None = None
    current_balance: BalanceResponse | None = None

    def act(self) -> None:
        """Perform the act."""
        self.log.info("Triggering L2 to L1 bridge...")
        self._is_done = True
        self._event = LstabciappEvents.DONE

    def is_triggered(self) -> bool:
        """Check if the state is triggered."""
        # Implement the condition to trigger this state
        min_olas_balance = self.get_min_olas_balance()
        if not min_olas_balance:
            self.log.warning("No minimal OLAS balance set, skipping bridge trigger.")
            return False

        for operation in TriggerOperations:
            operation_balance = self.get_operation_balance(operation)
            if operation_balance.balance.amount >= min_olas_balance:
                self.log.info(f"Operation {operation} triggered with balance of {operation_balance.balance.amount}.")
                self.current_operation = operation
                self.current_balance = operation_balance
                return True
            self.log.info(f"Operation {operation} has insufficient balance {operation_balance}.")
        return False

    def get_min_olas_balance(self) -> int:
        """Get the minimal balance to trigger the bridge."""
        return cast(
            int,
            self.strategy.lst_collector_contract.min_olas_balance(
                self.strategy.layer_2_api, self.strategy.lst_collector_address
            ).get("int"),
        )

    def get_operation_balance(self, operation: TriggerOperations) -> BalanceResponse:
        """Get the balance for a specific operation."""
        data = self.strategy.lst_collector_contract.map_operation_receiver_balances(
            self.strategy.layer_2_api, self.strategy.lst_collector_address, operation.value
        )
        return BalanceResponse.from_response(data)
