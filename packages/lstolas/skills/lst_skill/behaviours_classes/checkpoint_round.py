"""Checkpoint Round behaviour class."""

from typing import cast

from aea_ledger_ethereum import Address

from packages.lstolas.skills.lst_skill.events_processing import EventsPayload
from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


class CheckpointRound(BaseState):
    """This class implements the behaviour of the state CheckpointRound."""

    _state = LstabciappStates.CHECKPOINTROUND
    current_staking_proxy: Address | None = None

    def act(self) -> None:
        """Perform the act."""
        self.log.info("Creating checkpoint...")
        self._is_done = True
        self._event = LstabciappEvents.DONE

    def is_triggered(self) -> bool:
        """Check whether the behaviour is triggered."""
        self.current_staking_proxy = None
        current_block_ts = int(self.strategy.layer_2_api.api.eth.get_block("latest").timestamp)  # type: ignore
        raw_events = self.strategy.lst_staking_manager_contract.get_staked_events(
            self.strategy.layer_2_api,
            self.strategy.lst_staking_manager_address,
            from_block=17497117,
        )

        all_events = EventsPayload(dictionary=raw_events)

        unique_staking_proxies = {event.args.stakingProxy for event in all_events.events}

        for staking_proxy in unique_staking_proxies:
            last_checkpoint = cast(
                int,
                self.strategy.lst_staking_token_locked.ts_checkpoint(
                    self.strategy.layer_2_api,
                    staking_proxy,
                ).get("int"),
            )
            livliness_period = cast(
                int,
                self.strategy.lst_staking_token_locked.liveness_period(
                    self.strategy.layer_2_api,
                    staking_proxy,
                ).get("int"),
            )

            if current_block_ts - last_checkpoint > livliness_period:
                self.log.info(f"Checkpoint needed for staking proxy {staking_proxy}.")
                self.current_staking_proxy = staking_proxy
                return True
        return False
