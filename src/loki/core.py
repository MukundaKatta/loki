"""Core browser automation engine with command parsing and action execution."""

from typing import Any, Dict, List, Optional

from loki.models import Action, ActionType
from loki.parser import NLCommandParser
from loki.session import BrowserSession


class ActionExecutor:
    """Simulated browser action executor.

    Instead of controlling a real browser, this executor logs every action
    it receives and updates the associated BrowserSession state.  This makes
    the entire system testable without any browser dependency.
    """

    def __init__(self, session: Optional[BrowserSession] = None) -> None:
        self._session = session or BrowserSession()
        self._action_log: List[Dict[str, Any]] = []
        self._execution_count = 0

    @property
    def session(self) -> BrowserSession:
        return self._session

    @property
    def action_log(self) -> List[Dict[str, Any]]:
        return list(self._action_log)

    @property
    def execution_count(self) -> int:
        return self._execution_count

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def execute(self, action: Action) -> Dict[str, Any]:
        """Execute a single action and return a result dict."""
        handler = self._get_handler(action.action_type)
        result = handler(action)
        log_entry = {
            "index": self._execution_count,
            "action": action.to_dict(),
            "result": result,
        }
        self._action_log.append(log_entry)
        self._session.add_to_action_log(action.to_dict())
        self._execution_count += 1
        return result

    def execute_many(self, actions: List[Action]) -> List[Dict[str, Any]]:
        """Execute a sequence of actions, returning all results."""
        return [self.execute(a) for a in actions]

    def reset(self) -> None:
        """Clear the action log and reset the counter."""
        self._action_log.clear()
        self._execution_count = 0

    # ------------------------------------------------------------------
    # Action handlers (simulated)
    # ------------------------------------------------------------------

    def _get_handler(self, action_type: ActionType):
        handlers = {
            ActionType.NAVIGATE: self._handle_navigate,
            ActionType.CLICK: self._handle_click,
            ActionType.TYPE: self._handle_type,
            ActionType.SCROLL: self._handle_scroll,
            ActionType.EXTRACT: self._handle_extract,
            ActionType.WAIT: self._handle_wait,
            ActionType.SCREENSHOT: self._handle_screenshot,
            ActionType.BACK: self._handle_back,
            ActionType.FORWARD: self._handle_forward,
            ActionType.REFRESH: self._handle_refresh,
        }
        return handlers.get(action_type, self._handle_unknown)

    def _handle_navigate(self, action: Action) -> Dict[str, Any]:
        url = action.value or ""
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url
        self._session.navigate(url)
        return {"status": "ok", "url": url}

    def _handle_click(self, action: Action) -> Dict[str, Any]:
        return {
            "status": "ok",
            "clicked": action.selector or "unknown",
        }

    def _handle_type(self, action: Action) -> Dict[str, Any]:
        return {
            "status": "ok",
            "typed": action.value or "",
            "target": action.selector or "unknown",
        }

    def _handle_scroll(self, action: Action) -> Dict[str, Any]:
        direction = action.value or "down"
        return {"status": "ok", "direction": direction}

    def _handle_extract(self, action: Action) -> Dict[str, Any]:
        selector = action.selector or "body"
        simulated_text = "<extracted text from '{}'>".format(selector)
        self._session.add_extracted_data(selector, simulated_text)
        return {"status": "ok", "selector": selector, "data": simulated_text}

    def _handle_wait(self, action: Action) -> Dict[str, Any]:
        try:
            seconds = float(action.value) if action.value else 1.0
        except (ValueError, TypeError):
            seconds = 1.0
        return {"status": "ok", "waited_seconds": seconds}

    def _handle_screenshot(self, action: Action) -> Dict[str, Any]:
        return {"status": "ok", "screenshot": "simulated_screenshot.png"}

    def _handle_back(self, action: Action) -> Dict[str, Any]:
        url = self._session.go_back()
        return {"status": "ok", "url": url}

    def _handle_forward(self, action: Action) -> Dict[str, Any]:
        url = self._session.go_forward()
        return {"status": "ok", "url": url}

    def _handle_refresh(self, action: Action) -> Dict[str, Any]:
        return {"status": "ok", "url": self._session.current_url}

    def _handle_unknown(self, action: Action) -> Dict[str, Any]:
        return {"status": "error", "message": "Unknown action type"}


class BrowserAgent:
    """High-level browser automation agent.

    Accepts natural language commands, parses them into ``Action`` objects via
    ``NLCommandParser``, and executes them through ``ActionExecutor``.
    """

    def __init__(
        self,
        session: Optional[BrowserSession] = None,
        parser: Optional[NLCommandParser] = None,
        executor: Optional[ActionExecutor] = None,
    ) -> None:
        self._session = session or BrowserSession()
        self._parser = parser or NLCommandParser()
        self._executor = executor or ActionExecutor(self._session)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def session(self) -> BrowserSession:
        return self._session

    @property
    def parser(self) -> NLCommandParser:
        return self._parser

    @property
    def executor(self) -> ActionExecutor:
        return self._executor

    @property
    def history(self) -> List[Dict[str, Any]]:
        return self._executor.action_log

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, command: str) -> List[Dict[str, Any]]:
        """Parse a natural language command and execute the resulting actions.

        Returns a list of result dicts, one per action executed.
        """
        if not command or not command.strip():
            return []
        actions = self._parser.parse(command)
        return self._executor.execute_many(actions)

    def run_script(self, script: str) -> List[Dict[str, Any]]:
        """Run multiple commands separated by newlines.

        Blank lines and lines starting with ``#`` are ignored.
        """
        results = []
        for line in script.strip().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            results.extend(self.run(line))
        return results

    def get_extracted_data(self) -> Dict[str, str]:
        """Return all data extracted during this session."""
        return self._session.extracted_data

    def get_current_url(self) -> Optional[str]:
        """Return the current URL of the simulated browser."""
        return self._session.current_url

    def reset(self) -> None:
        """Reset the agent — clears session, executor log, etc."""
        self._session.reset()
        self._executor.reset()
