"""Tests for loki.session — BrowserSession."""

import pytest

from loki.session import BrowserSession


@pytest.fixture
def session():
    return BrowserSession()


class TestNavigation:
    def test_initial_url_is_none(self, session):
        assert session.current_url is None

    def test_navigate_sets_url(self, session):
        session.navigate("https://example.com")
        assert session.current_url == "https://example.com"

    def test_history_tracks_urls(self, session):
        session.navigate("https://a.com")
        session.navigate("https://b.com")
        assert session.history == ["https://a.com", "https://b.com"]

    def test_go_back(self, session):
        session.navigate("https://a.com")
        session.navigate("https://b.com")
        url = session.go_back()
        assert url == "https://a.com"
        assert session.current_url == "https://a.com"

    def test_go_forward(self, session):
        session.navigate("https://a.com")
        session.navigate("https://b.com")
        session.go_back()
        url = session.go_forward()
        assert url == "https://b.com"

    def test_navigate_truncates_forward_history(self, session):
        session.navigate("https://a.com")
        session.navigate("https://b.com")
        session.go_back()
        session.navigate("https://c.com")
        assert session.history == ["https://a.com", "https://c.com"]

    def test_go_back_at_start_stays(self, session):
        session.navigate("https://a.com")
        session.go_back()
        assert session.current_url == "https://a.com"


class TestCookies:
    def test_set_and_get(self, session):
        session.set_cookie("token", "abc123")
        assert session.get_cookie("token") == "abc123"

    def test_delete_cookie(self, session):
        session.set_cookie("token", "abc123")
        session.delete_cookie("token")
        assert session.get_cookie("token") is None

    def test_cookies_property_is_copy(self, session):
        session.set_cookie("a", "1")
        cookies = session.cookies
        cookies["b"] = "2"
        assert session.get_cookie("b") is None


class TestExtractedData:
    def test_add_and_retrieve(self, session):
        session.add_extracted_data("title", "Hello World")
        assert session.extracted_data["title"] == "Hello World"


class TestActionLog:
    def test_add_to_log(self, session):
        session.add_to_action_log({"type": "click", "selector": "a"})
        assert len(session.action_log) == 1

    def test_log_is_copy(self, session):
        session.add_to_action_log({"type": "click"})
        log = session.action_log
        log.append({"type": "fake"})
        assert len(session.action_log) == 1


class TestReset:
    def test_reset_clears_all(self, session):
        session.navigate("https://a.com")
        session.set_cookie("x", "1")
        session.add_extracted_data("k", "v")
        session.add_to_action_log({"type": "click"})
        session.reset()
        assert session.current_url is None
        assert session.history == []
        assert session.cookies == {}
        assert session.extracted_data == {}
        assert session.action_log == []
