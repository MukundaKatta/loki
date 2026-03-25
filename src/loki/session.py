"""Browser session state management.

Tracks navigation history, cookies, extracted data, and the full action log
for a simulated browser session.
"""

from typing import Any, Dict, List, Optional


class BrowserSession:
    """Stateful representation of a simulated browser session.

    Keeps track of:
    * Current URL and navigation history (with back/forward support).
    * A cookie jar (simple dict).
    * Data extracted during the session.
    * A chronological log of every action executed.
    """

    def __init__(self) -> None:
        self._history: List[str] = []
        self._history_index: int = -1
        self._cookies: Dict[str, str] = {}
        self._extracted_data: Dict[str, str] = {}
        self._action_log: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def current_url(self) -> Optional[str]:
        if 0 <= self._history_index < len(self._history):
            return self._history[self._history_index]
        return None

    @property
    def history(self) -> List[str]:
        return list(self._history)

    @property
    def cookies(self) -> Dict[str, str]:
        return dict(self._cookies)

    @property
    def extracted_data(self) -> Dict[str, str]:
        return dict(self._extracted_data)

    @property
    def action_log(self) -> List[Dict[str, Any]]:
        return list(self._action_log)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self, url: str) -> None:
        """Navigate to *url*, truncating any forward history."""
        if self._history_index < len(self._history) - 1:
            self._history = self._history[: self._history_index + 1]
        self._history.append(url)
        self._history_index = len(self._history) - 1

    def go_back(self) -> Optional[str]:
        """Move back in history.  Returns the new current URL or ``None``."""
        if self._history_index > 0:
            self._history_index -= 1
        return self.current_url

    def go_forward(self) -> Optional[str]:
        """Move forward in history.  Returns the new current URL or ``None``."""
        if self._history_index < len(self._history) - 1:
            self._history_index += 1
        return self.current_url

    # ------------------------------------------------------------------
    # Cookies
    # ------------------------------------------------------------------

    def set_cookie(self, name: str, value: str) -> None:
        self._cookies[name] = value

    def get_cookie(self, name: str) -> Optional[str]:
        return self._cookies.get(name)

    def delete_cookie(self, name: str) -> None:
        self._cookies.pop(name, None)

    # ------------------------------------------------------------------
    # Extracted data
    # ------------------------------------------------------------------

    def add_extracted_data(self, key: str, value: str) -> None:
        self._extracted_data[key] = value

    # ------------------------------------------------------------------
    # Action log
    # ------------------------------------------------------------------

    def add_to_action_log(self, entry: Dict[str, Any]) -> None:
        self._action_log.append(entry)

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Clear all session state."""
        self._history.clear()
        self._history_index = -1
        self._cookies.clear()
        self._extracted_data.clear()
        self._action_log.clear()
