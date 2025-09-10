"""Claim reward tokens round behaviour."""

from typing import Any

from web3.exceptions import ContractLogicError, ContractCustomError
from aea_ledger_ethereum import Address

from packages.lstolas.skills.lst_skill.events_processing import EventsPayload
from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


class ClaimRewardTokensRound(BaseState):
    """This class implements the behaviour of the state ClaimRewardTokensRound."""

    _state = LstabciappStates.CLAIMREWARDTOKENSROUND
    current_activity_module: Address | None = None

    def act(self) -> None:
        """Perform the act."""
        self.log.info("Claiming reward tokens...")
        self._is_done = True
        self._event = LstabciappEvents.DONE

    def is_triggered(self) -> bool:
        """Check whether the behaviour is triggered."""
        self.current_activity_module = None
        raw_events = self.strategy.lst_staking_manager_contract.get_staked_events(
            self.strategy.layer_2_api,
            self.strategy.lst_staking_manager_address,
            from_block=17497117,
        )

        all_events = EventsPayload(dictionary=raw_events)
        unique_staking_proxies = set()
        service_id_to_activity_module = {}

        for event in all_events.events:
            unique_staking_proxies.add(event.args.stakingProxy)
            service_id_to_activity_module[event.args.serviceId] = event.args.activityModule
        for service_id, activity_module in service_id_to_activity_module.items():
            self.log.info(
                f"Checking claimable rewards for service ID {service_id} and activity module {activity_module}..."
            )
            function: Any = self.strategy.lst_activity_module_contract.claim(
                ledger_api=self.strategy.layer_2_api,
                contract_address=activity_module,
            )
            try:
                function.call()
                self.log.info(f"Successfully called claim rewards for service ID {service_id}.")
                self.current_activity_module = activity_module
                return True
            except (ContractLogicError, ContractCustomError):
                self.log.info(f"No claimable rewards for service ID {service_id}.")
        return False
