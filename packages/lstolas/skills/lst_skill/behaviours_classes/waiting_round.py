"""Waiting Round Behaviour Class."""

import time

from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


class WaitingRound(BaseState):
    """This class implements the behaviour of the state WaitingRound."""

    _state = LstabciappStates.WAITINGROUND

    def act(self) -> None:
        """Perform the act."""
        self.log.info("No work to be done. Waiting...")
        time.sleep(10)  # wait for 10 seconds before checking again
        self._is_done = True
        self._event = LstabciappEvents.DONE
