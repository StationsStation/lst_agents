"""Claim reward tokens round behaviour."""

from packages.lstolas.skills.lst_skill.events_processing import EventsPayload
from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


class ClaimRewardTokensRound(BaseState):
    """This class implements the behaviour of the state ClaimRewardTokensRound."""

    _state = LstabciappStates.CLAIMREWARDTOKENSROUND

    def act(self) -> None:
        """Perform the act."""
        self.log.info("Claiming reward tokens...")
        self._is_done = True
        self._event = LstabciappEvents.DONE

    def is_triggered(self) -> bool:
        """Check whether the behaviour is triggered."""
        raw_events = self.strategy.lst_staking_manager_contract.get_staked_events(
            self.strategy.layer_2_api,
            self.strategy.lst_staking_manager_address,
            from_block=17497117,
        )

        EventsPayload(dictionary=raw_events)

        return True
