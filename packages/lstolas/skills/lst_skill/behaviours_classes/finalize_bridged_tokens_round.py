"""Skill behaviour for finalizing bridged tokens round."""

from typing import cast

from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


class FinalizeBridgedTokensRound(BaseState):
    """This class implements the behaviour of the state ClaimRewardTokensRound."""

    _state = LstabciappStates.FINALIZEBRIDGEDTOKENSROUND
    balance_of_unstake_relayer: int
    balance_of_distributor: int

    def act(self) -> None:
        """Perform the act."""
        self.log.info("Distributing reward tokens...")
        results = []
        if self.balance_of_unstake_relayer:
            self.log.info("Finalizing bridged tokens for unstake relayer contract...")
            results.append(
                self.tx_settler.build_and_settle_transaction(
                    contract_address=self.strategy.lst_unstake_relayer_address,
                    function=self.strategy.lst_unstake_relayer_contract.relay,
                    ledger_api=self.strategy.layer_1_api,
                )
            )
        if self.balance_of_distributor:
            self.log.info("Finalizing bridged tokens for distributor contract...")
            results.append(
                self.tx_settler.build_and_settle_transaction(
                    contract_address=self.strategy.lst_distributor_address,
                    function=self.strategy.lst_distributor_contract.distribute,
                    ledger_api=self.strategy.layer_1_api,
                )
            )
        self._is_done = True
        self._event = LstabciappEvents.DONE if all(results) else LstabciappEvents.FATAL_ERROR

    def is_triggered(self) -> bool:
        """Check if the condition is met to trigger this behaviour."""
        self.log.debug("Checking if there are bridged tokens to finalize...")
        self.balance_of_unstake_relayer = self.get_token_balance(self.strategy.lst_unstake_relayer_address)
        self.balance_of_distributor = self.get_token_balance(self.strategy.lst_distributor_address)
        return any([self.balance_of_unstake_relayer, self.balance_of_distributor])

    def get_token_balance(self, contract_address) -> int:
        """Get the balance of the contract."""
        return cast(
            int,
            self.strategy.layer_1_olas_contract.balance_of(
                self.strategy.layer_1_api,
                self.strategy.layer_1_olas_token_address,
                contract_address,
            )["int"],
        )
