"""Behaviour class for the state RedeemRound of the LstAbciApp."""

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
        self._event = LstabciappEvents.DONE

    def is_triggered(self) -> bool:
        """Check if the condition is met to trigger this behaviour."""
        # we check if there are tokens to be redeemed here;
        return True
