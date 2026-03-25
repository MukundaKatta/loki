"""Natural language command parser for browser automation.

Converts free-form text commands into structured Action objects using
keyword-based pattern matching.  No ML model required.
"""

import re
from typing import List, Tuple

from loki.models import Action, ActionType


# ------------------------------------------------------------------
# Pattern definitions  (regex, action_type, group layout)
# ------------------------------------------------------------------

# Each pattern is (compiled_regex, ActionType, extractor_callable).
# The extractor receives the Match object and returns (selector, value).

def _extract_navigate(m: re.Match) -> Tuple[str, str]:
    url = (m.group("url") or "").strip()
    return (None, url)  # type: ignore[return-value]


def _extract_click(m: re.Match) -> Tuple[str, str]:
    target = (m.group("target") or "").strip().rstrip(".")
    return (target, None)  # type: ignore[return-value]


def _extract_type(m: re.Match) -> Tuple[str, str]:
    text = (m.group("text") or "").strip()
    target = (m.group("target") or "").strip().rstrip(".")
    return (target or None, text or None)  # type: ignore[return-value]


def _extract_scroll(m: re.Match) -> Tuple[str, str]:
    direction = (m.group("dir") or "down").strip().lower()
    return (None, direction)  # type: ignore[return-value]


def _extract_extract(m: re.Match) -> Tuple[str, str]:
    target = (m.group("target") or "").strip().rstrip(".")
    return (target or None, None)  # type: ignore[return-value]


def _extract_wait(m: re.Match) -> Tuple[str, str]:
    seconds = (m.group("secs") or "1").strip()
    return (None, seconds)  # type: ignore[return-value]


_PATTERNS: List[Tuple[re.Pattern, ActionType, callable]] = [
    # Navigate --------------------------------------------------------
    (
        re.compile(
            r"(?:go\s+to|navigate\s+to|open|visit|browse\s+to|load)\s+(?P<url>\S+)",
            re.IGNORECASE,
        ),
        ActionType.NAVIGATE,
        _extract_navigate,
    ),
    # Click -----------------------------------------------------------
    (
        re.compile(
            r"click\s+(?:on\s+)?(?:the\s+)?(?P<target>.+?)(?:\s+button|\s+link|\s+element)?$",
            re.IGNORECASE,
        ),
        ActionType.CLICK,
        _extract_click,
    ),
    # Type (with target) ---------------------------------------------
    (
        re.compile(
            r"(?:type|enter|input|fill(?:\s+in)?)\s+['\"]?(?P<text>[^'\"]+?)['\"]?\s+(?:in(?:to)?|on)\s+(?:the\s+)?(?P<target>.+?)$",
            re.IGNORECASE,
        ),
        ActionType.TYPE,
        _extract_type,
    ),
    # Type (without explicit target) ---------------------------------
    (
        re.compile(
            r"(?:type|enter|input)\s+['\"]?(?P<text>[^'\"]+?)['\"]?\s*$",
            re.IGNORECASE,
        ),
        ActionType.TYPE,
        lambda m: (None, (m.group("text") or "").strip()),
    ),
    # Search shorthand ("search for X") --------------------------------
    (
        re.compile(
            r"search\s+(?:for\s+)?['\"]?(?P<text>[^'\"]+?)['\"]?\s*$",
            re.IGNORECASE,
        ),
        ActionType.TYPE,
        lambda m: ("search box", (m.group("text") or "").strip()),
    ),
    # Scroll ----------------------------------------------------------
    (
        re.compile(
            r"scroll\s+(?P<dir>up|down|left|right)",
            re.IGNORECASE,
        ),
        ActionType.SCROLL,
        _extract_scroll,
    ),
    # Extract ---------------------------------------------------------
    (
        re.compile(
            r"(?:extract|scrape|get|read|grab)\s+(?:the\s+)?(?:text\s+(?:from|of)\s+)?(?:the\s+)?(?P<target>.+?)$",
            re.IGNORECASE,
        ),
        ActionType.EXTRACT,
        _extract_extract,
    ),
    # Wait ------------------------------------------------------------
    (
        re.compile(
            r"wait\s+(?:for\s+)?(?P<secs>\d+(?:\.\d+)?)\s*(?:s(?:ec(?:ond)?s?)?)?",
            re.IGNORECASE,
        ),
        ActionType.WAIT,
        _extract_wait,
    ),
    # Screenshot ------------------------------------------------------
    (
        re.compile(r"(?:take\s+a?\s*)?screenshot", re.IGNORECASE),
        ActionType.SCREENSHOT,
        lambda m: (None, None),
    ),
    # Back / Forward / Refresh ----------------------------------------
    (
        re.compile(r"go\s+back", re.IGNORECASE),
        ActionType.BACK,
        lambda m: (None, None),
    ),
    (
        re.compile(r"go\s+forward", re.IGNORECASE),
        ActionType.FORWARD,
        lambda m: (None, None),
    ),
    (
        re.compile(r"refresh|reload", re.IGNORECASE),
        ActionType.REFRESH,
        lambda m: (None, None),
    ),
]


class NLCommandParser:
    """Parse natural language browser commands into Action objects.

    Supports compound commands joined by "and" or "then".
    """

    COMPOUND_SPLIT = re.compile(r"\s+(?:and\s+then|then|and)\s+", re.IGNORECASE)

    def parse(self, text: str) -> List[Action]:
        """Parse *text* into one or more Actions.

        Compound commands separated by "and"/"then" are split and each
        sub-command is parsed independently.
        """
        if not text or not text.strip():
            return []

        text = text.strip()
        sub_commands = self._split_compound(text)
        actions: List[Action] = []
        for cmd in sub_commands:
            action = self._parse_single(cmd.strip())
            if action is not None:
                actions.append(action)
        return actions

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _split_compound(self, text: str) -> List[str]:
        """Split compound commands while preserving quoted strings."""
        parts = self.COMPOUND_SPLIT.split(text)
        return [p for p in parts if p.strip()]

    def _parse_single(self, text: str) -> "Action | None":
        """Attempt to match *text* against known patterns."""
        for pattern, action_type, extractor in _PATTERNS:
            m = pattern.search(text)
            if m:
                selector, value = extractor(m)
                return Action(
                    action_type=action_type,
                    selector=selector,
                    value=value,
                )
        return None
