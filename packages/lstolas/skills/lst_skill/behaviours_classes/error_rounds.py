"""Error Rounds Behaviour Classes."""

from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


class UnHandledErrorRound(BaseState):
    """This class implements the behaviour of the state UnHandledErrorRound."""

    _state = LstabciappStates.UNHANDLEDERRORROUND

    def act(self) -> None:
        """Perform the act."""
        self.log.info("Handling unhandled error...")
        self._is_done = True
        self._event = LstabciappEvents.DONE


class HandledErrorRound(BaseState):
    """This class implements the behaviour of the state HandledErrorRound."""

    _state = LstabciappStates.HANDLEDERRORROUND

    def act(self) -> None:
        """Perform the act."""
        self.log.info("Handling error...")
        self._is_done = True
        self._event = LstabciappEvents.DONE
