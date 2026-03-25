"""Tests for loki.core — BrowserAgent and ActionExecutor."""

import pytest

from loki.models import Action, ActionType
from loki.core import ActionExecutor, BrowserAgent
from loki.session import BrowserSession


# ------------------------------------------------------------------ #
# Action dataclass
# ------------------------------------------------------------------ #


class TestAction:
    def test_to_dict_minimal(self):
        a = Action(action_type=ActionType.CLICK)
        d = a.to_dict()
        assert d == {"type": "click"}

    def test_to_dict_full(self):
        a = Action(
            action_type=ActionType.TYPE,
            selector="input#email",
            value="user@example.com",
            metadata={"delay": 50},
        )
        d = a.to_dict()
        assert d["type"] == "type"
        assert d["selector"] == "input#email"
        assert d["value"] == "user@example.com"
        assert d["metadata"]["delay"] == 50

    def test_str_representation(self):
        a = Action(ActionType.NAVIGATE, value="https://example.com")
        assert "navigate" in str(a)
        assert "example.com" in str(a)


# ------------------------------------------------------------------ #
# ActionExecutor
# ------------------------------------------------------------------ #


class TestActionExecutor:
    def test_execute_navigate(self):
        session = BrowserSession()
        exe = ActionExecutor(session)
        result = exe.execute(Action(ActionType.NAVIGATE, value="example.com"))
        assert result["status"] == "ok"
        assert result["url"] == "https://example.com"
        assert session.current_url == "https://example.com"

    def test_execute_click(self):
        exe = ActionExecutor()
        result = exe.execute(Action(ActionType.CLICK, selector="button.submit"))
        assert result["status"] == "ok"
        assert result["clicked"] == "button.submit"

    def test_execute_type(self):
        exe = ActionExecutor()
        result = exe.execute(
            Action(ActionType.TYPE, selector="input#q", value="hello")
        )
        assert result["typed"] == "hello"
        assert result["target"] == "input#q"

    def test_execute_extract_stores_data(self):
        session = BrowserSession()
        exe = ActionExecutor(session)
        exe.execute(Action(ActionType.EXTRACT, selector="h1.title"))
        assert "h1.title" in session.extracted_data

    def test_execute_wait(self):
        exe = ActionExecutor()
        result = exe.execute(Action(ActionType.WAIT, value="3"))
        assert result["waited_seconds"] == 3.0

    def test_execute_scroll(self):
        exe = ActionExecutor()
        result = exe.execute(Action(ActionType.SCROLL, value="up"))
        assert result["direction"] == "up"

    def test_execution_count_increments(self):
        exe = ActionExecutor()
        assert exe.execution_count == 0
        exe.execute(Action(ActionType.CLICK, selector="a"))
        exe.execute(Action(ActionType.CLICK, selector="b"))
        assert exe.execution_count == 2

    def test_reset_clears_log(self):
        exe = ActionExecutor()
        exe.execute(Action(ActionType.CLICK, selector="x"))
        exe.reset()
        assert exe.execution_count == 0
        assert exe.action_log == []


# ------------------------------------------------------------------ #
# BrowserAgent
# ------------------------------------------------------------------ #


class TestBrowserAgent:
    def test_run_navigate(self):
        agent = BrowserAgent()
        results = agent.run("go to example.com")
        assert len(results) == 1
        assert results[0]["status"] == "ok"
        assert agent.get_current_url() == "https://example.com"

    def test_run_empty_string(self):
        agent = BrowserAgent()
        assert agent.run("") == []
        assert agent.run("   ") == []

    def test_run_script(self):
        agent = BrowserAgent()
        script = """
        # Navigate first
        go to example.com
        click the login button

        type admin in the username field
        """
        results = agent.run_script(script)
        assert len(results) == 3

    def test_history_populated(self):
        agent = BrowserAgent()
        agent.run("go to example.com")
        agent.run("click submit")
        assert len(agent.history) == 2

    def test_reset_clears_everything(self):
        agent = BrowserAgent()
        agent.run("go to example.com")
        agent.reset()
        assert agent.get_current_url() is None
        assert agent.history == []
