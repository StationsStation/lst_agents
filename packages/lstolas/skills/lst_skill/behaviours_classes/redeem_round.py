"""Behaviour class for the state RedeemRound of the LstAbciApp."""

from packages.lstolas.skills.lst_skill.events_processing import EventsPayload
from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


class RedeemRound(BaseState):
    """This class implements the behaviour of the state RedeemRound."""

    _state = LstabciappStates.REDEEMROUND

    def act(self) -> None:
        """Perform the act."""
        self.log.info("Redeeming tokens...")
        self._is_done = True
        self._event = LstabciappEvents.FATAL_ERROR

    def is_triggered(self) -> bool:
        """Check if the condition is met to trigger this behaviour."""
        # we check if there are tokens to be redeemed here;
        queued_requests = EventsPayload(
            dictionary=self.strategy.lst_staking_processor_l2_contract.get_request_queued_events(
                self.strategy.layer_2_api,
                self.strategy.lst_staking_processor_l2_address,
                from_block=17590111,
            )
        )
        if queued_requests.events:
            self.log.info(f"Found {len(queued_requests.events)} queued requests to be processed.")
            return True
        return False
