"""Checkpoint Round behaviour class."""

from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


class CheckpointRound(BaseState):
    """This class implements the behaviour of the state CheckpointRound."""

    _state = LstabciappStates.CHECKPOINTROUND

    def act(self) -> None:
        """Perform the act."""
        self.log.info("Creating checkpoint...")
        self._is_done = True
        self._event = LstabciappEvents.DONE
