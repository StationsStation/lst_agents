"""Test the metrics skill."""

from typing import cast
from pathlib import Path

from aea.test_tools.test_skill import BaseSkillTestCase

from packages.lstolas.skills.lst_skill import PUBLIC_ID
from packages.lstolas.skills.lst_skill.behaviours import (
    FinalizeBridgedTokensRound,
)
from packages.lstolas.skills.lst_skill.behaviours_classes.redeem_round import RedeemRound
from packages.lstolas.skills.lst_skill.behaviours_classes.base_behaviour import BaseState, LstabciappStates
from packages.lstolas.skills.lst_skill.behaviours_classes.checkpoint_round import CheckpointRound
from packages.lstolas.skills.lst_skill.behaviours_classes.trigger_l2_to_l1_bridge import TriggerL2ToL1BridgeRound
from packages.lstolas.skills.lst_skill.behaviours_classes.claim_reward_tokens_round import ClaimRewardTokensRound
from packages.lstolas.skills.lst_skill.behaviours_classes.claim_bridged_tokens_round import (
    ClaimBridgedTokensRound,
)


ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent.parent


class BaseTestConditionalBehaviour(BaseSkillTestCase):
    """Test the conditional behaviour of the skill."""

    path_to_skill = Path(ROOT_DIR, "packages", PUBLIC_ID.author, "skills", PUBLIC_ID.name)
    behaviour: BaseState

    @classmethod
    def teardown_method(cls):  # pylint: disable=W0221
        """Teardown the test class."""

    def test_setup(self):
        """Test the initialization of the strategy."""
        assert self.behaviour is not None
        assert self.behaviour.context is not None
        self.behaviour.setup()

    def test_trigger(self):
        """Test the initialization of the strategy."""
        self.behaviour.is_triggered()


class TestClaimBridgedTokens(BaseTestConditionalBehaviour):
    """Test HttpHandler of http_echo."""

    @classmethod
    def setup_method(cls):  # pylint: disable=W0221
        """Setup the test class."""
        super().setup_class()
        behaviour_to_test = LstabciappStates.CLAIMBRIDGEDTOKENSROUND
        cls.behaviour = cast(
            ClaimBridgedTokensRound, cls._skill.skill_context.behaviours.main.get_state(behaviour_to_test.value)
        )
        cls.logger = cls._skill.skill_context.logger


class TestTriggerL2ToL1Bridge(BaseTestConditionalBehaviour):
    """Test HttpHandler of http_echo."""

    @classmethod
    def setup_method(cls):  # pylint: disable=W0221
        """Setup the test class."""
        super().setup_class()
        behaviour_to_test = LstabciappStates.TRIGGERL2TOL1BRIDGEROUND
        cls.behaviour = cast(
            TriggerL2ToL1BridgeRound, cls._skill.skill_context.behaviours.main.get_state(behaviour_to_test.value)
        )
        cls.logger = cls._skill.skill_context.logger

    def test_act(self):
        """Test the initialization of the strategy."""
        self.behaviour.is_triggered()
        self.behaviour.act()


class TestFinalizeBridgedTokens(BaseTestConditionalBehaviour):
    """Test HttpHandler of http_echo."""

    @classmethod
    def setup_method(cls):  # pylint: disable=W0221
        """Setup the test class."""
        super().setup_class()
        behaviour_to_test = LstabciappStates.FINALIZEBRIDGEDTOKENSROUND
        cls.behaviour = cast(
            FinalizeBridgedTokensRound, cls._skill.skill_context.behaviours.main.get_state(behaviour_to_test.value)
        )
        cls.logger = cls._skill.skill_context.logger


class TestClaimRewardTokensRound(BaseTestConditionalBehaviour):
    """Test HttpHandler of http_echo."""

    @classmethod
    def setup_method(cls):  # pylint: disable=W0221
        """Setup the test class."""
        super().setup_class()
        behaviour_to_test = LstabciappStates.CLAIMREWARDTOKENSROUND
        cls.behaviour = cast(
            ClaimRewardTokensRound, cls._skill.skill_context.behaviours.main.get_state(behaviour_to_test.value)
        )
        cls.logger = cls._skill.skill_context.logger


class TestCheckpointRound(BaseTestConditionalBehaviour):
    """Test HttpHandler of http_echo."""

    @classmethod
    def setup_method(cls):  # pylint: disable=W0221
        """Setup the test class."""
        super().setup_class()
        behaviour_to_test = LstabciappStates.CHECKPOINTROUND
        cls.behaviour = cast(
            CheckpointRound, cls._skill.skill_context.behaviours.main.get_state(behaviour_to_test.value)
        )
        cls.logger = cls._skill.skill_context.logger


class TestRedeemRound(BaseTestConditionalBehaviour):
    """Test HttpHandler of http_echo."""

    @classmethod
    def setup_method(cls):  # pylint: disable=W0221
        """Setup the test class."""
        super().setup_class()
        behaviour_to_test = LstabciappStates.REDEEMROUND
        cls.behaviour = cast(RedeemRound, cls._skill.skill_context.behaviours.main.get_state(behaviour_to_test.value))
        cls.logger = cls._skill.skill_context.logger
