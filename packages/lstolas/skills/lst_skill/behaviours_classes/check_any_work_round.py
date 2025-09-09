"""Check any work round behaviour."""

from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import (
    BaseState,
    LstabciappEvents,
    LstabciappStates,
)


class CheckAnyWorkRound(BaseState):
    """This class implements the behaviour of the state CheckAnyWorkRound."""

    _state = LstabciappStates.CHECKANYWORKROUND

    conditional_behaviours_to_events: list[tuple[LstabciappStates, LstabciappEvents]] = []

    def setup(self) -> None:
        """Setup the conditional behaviours."""
        self.conditional_behaviours_to_events = [
            (LstabciappStates.CLAIMBRIDGEDTOKENSROUND, LstabciappEvents.CLAIM_BRIDGED_TOKEN),
            (LstabciappStates.TRIGGERL2TOL1BRIDGEROUND, LstabciappEvents.TRIGGER_L2_TO_L1),
            (LstabciappStates.FINALIZEBRIDGEDTOKENSROUND, LstabciappEvents.FINALIZE_BRIDGED_TOKEN),
        ]

    def act(self) -> None:
        """Perform the act."""
        self.log.info("Checking for any work to be done...")
        self._event = LstabciappEvents.NO_WORK
        for behaviour, event in self.conditional_behaviours_to_events:
            instance: BaseState = self.context.behaviours.main.get_state(behaviour.value)
            self.log.info(f"Checking condition for {behaviour}...")
            if instance.is_triggered():
                self._event = event
                self._is_done = True
                return
        self._is_done = True
