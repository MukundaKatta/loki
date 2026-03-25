# Architecture

## Overview

Loki is a simulated browser automation agent that converts natural language
commands into structured browser actions.  No real browser is required — the
entire pipeline is deterministic and fully testable.

## Module Map

```
src/loki/
  __init__.py      Public API re-exports
  core.py          BrowserAgent, Action, ActionExecutor
  parser.py        NLCommandParser — regex-based NL-to-Action conversion
  session.py       BrowserSession — stateful navigation, cookies, data log
  config.py        LokiConfig dataclass
  cli.py           Argparse-based CLI (run / execute / history)
  __main__.py      python -m loki entry point
```

## Data Flow

```
User command (text)
  |
  v
NLCommandParser.parse()  ->  List[Action]
  |
  v
ActionExecutor.execute()  ->  result dict  (+ session state update)
  |
  v
BrowserSession  (tracks URL history, cookies, extracted data)
```

## Key Design Decisions

* **Simulated execution** — Actions are logged instead of driving a real
  browser.  This allows the full test suite to run with zero external
  dependencies.
* **Keyword-based parsing** — The NLCommandParser uses compiled regex
  patterns rather than an ML model, keeping the dependency footprint at zero.
* **Compound commands** — Commands joined by "and" / "then" are split and
  parsed independently, enabling multi-step workflows in a single line.
