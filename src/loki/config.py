"""Loki configuration defaults and helpers."""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class LokiConfig:
    """Runtime configuration for the Loki agent."""

    default_timeout: float = 30.0
    headless: bool = True
    user_agent: str = "Loki/0.1 (simulated)"
    viewport_width: int = 1280
    viewport_height: int = 720
    extra: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> "LokiConfig":
        known = {f.name for f in cls.__dataclass_fields__.values()}
        extra = {k: v for k, v in data.items() if k not in known}
        filtered = {k: v for k, v in data.items() if k in known and k != "extra"}
        return cls(**filtered, extra=extra)
