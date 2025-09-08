"""Trigger the bridge from L2 to L1 if there are pending transfers."""

from enum import Enum
from typing import cast

from pydantic import BaseModel
from aea_ledger_ethereum import Address

from packages.lstolas.skills.lst_skill.transactions import signed_tx_to_dict, try_send_signed_transaction
from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


TX_MINING_TIMEOUT = 300  # seconds


class TriggerOperations(Enum):
    """Enum for the different operations that can trigger the bridge."""

    REWARD = "0x0b9821ae606ebc7c79bf3390bdd3dc93e1b4a7cda27aad60646e7b88ff55b001"
    UNSTAKE = "0x8ca9a95e41b5eece253c93f5b31eed1253aed6b145d8a6e14d913fdf8e732293"
    UNSTAKE_RETIRED = "0x9065ad15d9673159e4597c86084aff8052550cec93c5a6e44b3f1dba4c8731b3"


class BalanceResponse(BaseModel):
    """Response model for the balance of an operation."""

    balance: int
    receiver: Address


class TriggerL2ToL1BridgeRound(BaseState):
    """This class implements the behaviour of the state TriggerL2ToL1BridgeRound."""

    _state = LstabciappStates.TRIGGERL2TOL1BRIDGEROUND
    current_operation: TriggerOperations | None = None
    current_balance: BalanceResponse | None = None

    def act(self) -> None:
        """Perform the act."""
        if self.current_operation is None or self.current_balance is None:
            self.log.error("Current operation or balance is not set.")
            self._event = LstabciappEvents.FATAL_ERROR
            self._is_done = True
            return
        self.log.info("Triggering L2 to L1 bridge...")

        # we here try to call the l2 relay operation.
        # bridge payload.
        function = self.strategy.lst_collector_contract.relay_tokens(
            self.strategy.layer_2_api,
            self.strategy.lst_collector_address,
            self.current_operation.value,  # type: ignore
            "0x",
        )
        raw_tx = self.strategy.build_transaction(
            self.strategy.layer_2_api,
            function,
        )
        signed_tx = signed_tx_to_dict(self.strategy.crypto.entity.sign_transaction(raw_tx))
        tx_hash = try_send_signed_transaction(self.strategy.layer_2_api, signed_tx)
        if tx_hash is None:
            self.log.error("Transaction failed to be sent...")
            self._event = LstabciappEvents.FATAL_ERROR
            self._is_done = True
            return
        self.context.logger.info(f"Transaction hash: {tx_hash}")
        tx_receipt = self.strategy.layer_2_api.api.eth.wait_for_transaction_receipt(tx_hash, timeout=TX_MINING_TIMEOUT)
        if tx_receipt is None or tx_receipt.get("status") != 1:
            self._event = LstabciappEvents.FATAL_ERROR
        else:
            self._event = LstabciappEvents.DONE
        self._is_done = True

    def is_triggered(self) -> bool:
        """Check if the state is triggered."""
        # Implement the condition to trigger this state
        min_olas_balance = self.get_min_olas_balance()
        if not min_olas_balance:
            self.log.warning("No minimal OLAS balance set, skipping bridge trigger.")
            return False

        for operation in TriggerOperations:
            operation_balance = self.get_operation_balance(operation)
            if operation_balance.balance >= min_olas_balance:
                self.log.info(f"Operation {operation} triggered with balance of {operation_balance.balance}.")
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
        return BalanceResponse(balance=cast(int, data.get("balance")), receiver=cast(Address, data.get("receiver")))
