"""Claim reward tokens round behaviour."""

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
