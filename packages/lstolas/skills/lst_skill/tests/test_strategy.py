"""Test the metrics skill."""

from typing import cast
from pathlib import Path

from aea.test_tools.test_skill import BaseSkillTestCase

from packages.lstolas.skills.lst_skill import PUBLIC_ID
from packages.lstolas.skills.lst_skill.models import LstStrategy


ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent.parent


class TestLSTStrategy(BaseSkillTestCase):
    """Test HttpHandler of http_echo."""

    path_to_skill = Path(ROOT_DIR, "packages", PUBLIC_ID.author, "skills", PUBLIC_ID.name)

    @classmethod
    def setup_method(cls):  # pylint: disable=W0221
        """Setup the test class."""
        super().setup_class()
        cls.strategy = cast(LstStrategy, cls._skill.skill_context.lst_strategy)
        cls.logger = cls._skill.skill_context.logger

    @classmethod
    def teardown_method(cls):  # pylint: disable=W0221
        """Teardown the test class."""

    def test_initialization(self):
        """Test the initialization of the strategy."""
        assert self.strategy.layer_1_api is not None
        assert self.strategy.layer_2_api is not None
