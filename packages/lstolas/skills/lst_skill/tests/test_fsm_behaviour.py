"""Test the metrics skill."""

from typing import cast
from pathlib import Path

from aea.test_tools.test_skill import BaseSkillTestCase

from packages.lstolas.skills.lst_skill import PUBLIC_ID
from packages.lstolas.skills.lst_skill.behaviours import (
    LstabciappFsmBehaviour,
)


ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent.parent


class TestFsmBehaviour(BaseSkillTestCase):
    """Test HttpHandler of http_echo."""

    path_to_skill = Path(ROOT_DIR, "packages", PUBLIC_ID.author, "skills", PUBLIC_ID.name)

    @classmethod
    def setup_method(cls):  # pylint: disable=W0221
        """Setup the test class."""
        super().setup_class()
        cls.behaviour = cast(LstabciappFsmBehaviour, cls._skill.skill_context.behaviours.main)
        cls.logger = cls._skill.skill_context.logger

    def test_setup(self):
        """Test the initialization of the strategy."""
        assert self.behaviour is not None
        assert self.behaviour.context is not None
        self.behaviour.setup()

    @classmethod
    def teardown_method(cls):  # pylint: disable=W0221
        """Teardown the test class."""
