"""Tests for loki.parser — NLCommandParser."""

import pytest

from loki.models import ActionType
from loki.parser import NLCommandParser


@pytest.fixture
def parser():
    return NLCommandParser()


# ------------------------------------------------------------------ #
# Single-command parsing
# ------------------------------------------------------------------ #


class TestNavigate:
    def test_go_to(self, parser):
        actions = parser.parse("go to example.com")
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.NAVIGATE
        assert actions[0].value == "example.com"

    def test_open(self, parser):
        actions = parser.parse("open https://google.com")
        assert actions[0].action_type == ActionType.NAVIGATE
        assert actions[0].value == "https://google.com"

    def test_visit(self, parser):
        actions = parser.parse("visit github.com")
        assert actions[0].value == "github.com"


class TestClick:
    def test_click_button(self, parser):
        actions = parser.parse("click the login button")
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.CLICK
        assert "login" in actions[0].selector

    def test_click_on_link(self, parser):
        actions = parser.parse("click on about link")
        assert actions[0].action_type == ActionType.CLICK


class TestType:
    def test_type_into_field(self, parser):
        actions = parser.parse("type hello in the search box")
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.TYPE
        assert actions[0].value == "hello"
        assert "search box" in actions[0].selector

    def test_enter_text(self, parser):
        actions = parser.parse("enter admin into the username field")
        assert actions[0].action_type == ActionType.TYPE
        assert actions[0].value == "admin"

    def test_type_bare(self, parser):
        actions = parser.parse("type some text")
        assert actions[0].action_type == ActionType.TYPE
        assert actions[0].value == "some text"


class TestScroll:
    def test_scroll_down(self, parser):
        actions = parser.parse("scroll down")
        assert actions[0].action_type == ActionType.SCROLL
        assert actions[0].value == "down"

    def test_scroll_up(self, parser):
        actions = parser.parse("scroll up")
        assert actions[0].value == "up"


class TestExtract:
    def test_extract_text(self, parser):
        actions = parser.parse("extract the text from the heading")
        assert actions[0].action_type == ActionType.EXTRACT


class TestWait:
    def test_wait_seconds(self, parser):
        actions = parser.parse("wait for 5 seconds")
        assert actions[0].action_type == ActionType.WAIT
        assert actions[0].value == "5"


class TestScreenshot:
    def test_take_screenshot(self, parser):
        actions = parser.parse("take a screenshot")
        assert actions[0].action_type == ActionType.SCREENSHOT


class TestBackForward:
    def test_go_back(self, parser):
        actions = parser.parse("go back")
        assert actions[0].action_type == ActionType.BACK

    def test_go_forward(self, parser):
        actions = parser.parse("go forward")
        assert actions[0].action_type == ActionType.FORWARD


class TestRefresh:
    def test_refresh(self, parser):
        actions = parser.parse("refresh")
        assert actions[0].action_type == ActionType.REFRESH

    def test_reload(self, parser):
        actions = parser.parse("reload")
        assert actions[0].action_type == ActionType.REFRESH


# ------------------------------------------------------------------ #
# Compound commands
# ------------------------------------------------------------------ #


class TestCompound:
    def test_and_split(self, parser):
        actions = parser.parse("go to example.com and click the login button")
        assert len(actions) == 2
        assert actions[0].action_type == ActionType.NAVIGATE
        assert actions[1].action_type == ActionType.CLICK

    def test_then_split(self, parser):
        actions = parser.parse("open google.com then search for AI")
        assert len(actions) == 2
        assert actions[0].action_type == ActionType.NAVIGATE
        assert actions[1].action_type == ActionType.TYPE

    def test_and_then_split(self, parser):
        actions = parser.parse(
            "go to github.com and then click the sign in button"
        )
        assert len(actions) == 2


# ------------------------------------------------------------------ #
# Edge cases
# ------------------------------------------------------------------ #


class TestEdgeCases:
    def test_empty_string(self, parser):
        assert parser.parse("") == []

    def test_whitespace_only(self, parser):
        assert parser.parse("   ") == []

    def test_unrecognised_returns_empty(self, parser):
        actions = parser.parse("fly me to the moon")
        assert actions == []

    def test_search_for(self, parser):
        actions = parser.parse("search for machine learning")
        assert len(actions) == 1
        assert actions[0].action_type == ActionType.TYPE
        assert actions[0].value == "machine learning"
        assert actions[0].selector == "search box"
