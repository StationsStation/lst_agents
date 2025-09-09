"""Starting round behaviour class."""

from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


class StartRound(BaseState):
    """This class implements the behaviour of the state StartRound."""

    _state = LstabciappStates.STARTROUND

    def act(self) -> None:
        """Perform the act."""
        self.log.info("Starting the round...")
        self._is_done = True
        self._event = LstabciappEvents.DONE
