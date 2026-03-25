"""Shared data models for Loki."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class ActionType(Enum):
    """Supported browser action types."""

    NAVIGATE = "navigate"
    CLICK = "click"
    TYPE = "type"
    SCROLL = "scroll"
    EXTRACT = "extract"
    WAIT = "wait"
    SCREENSHOT = "screenshot"
    BACK = "back"
    FORWARD = "forward"
    REFRESH = "refresh"


@dataclass
class Action:
    """A structured browser action produced by parsing a natural language command.

    Attributes:
        action_type: The kind of browser action to perform.
        selector: CSS selector or element description for targeting.
        value: Value to type, URL to navigate to, or other action-specific data.
        metadata: Additional key-value pairs for the action.
    """

    action_type: ActionType
    selector: Optional[str] = None
    value: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the action to a dictionary."""
        result = {"type": self.action_type.value}
        if self.selector is not None:
            result["selector"] = self.selector
        if self.value is not None:
            result["value"] = self.value
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    def __str__(self) -> str:
        parts = [self.action_type.value]
        if self.selector:
            parts.append("target='{}'".format(self.selector))
        if self.value:
            parts.append("value='{}'".format(self.value))
        return "Action({})".format(", ".join(parts))
