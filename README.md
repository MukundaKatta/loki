# Loki — Browser Automation Agent

> **Norse Mythology: The Trickster God** | AI-powered browser automation via natural language

[![CI](https://github.com/MukundaKatta/loki/actions/workflows/ci.yml/badge.svg)](https://github.com/MukundaKatta/loki/actions/workflows/ci.yml)
[![GitHub Pages](https://img.shields.io/badge/Live_Demo-Visit_Site-blue?style=for-the-badge)](https://MukundaKatta.github.io/loki/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- **Natural Language Commands** — control a browser with plain English
- **Command Parsing** — regex-based NL-to-action conversion (no ML model needed)
- **Compound Commands** — chain multiple actions: `"go to google.com and search for AI"`
- **Session Management** — tracks URL history, cookies, and extracted data
- **Simulated Execution** — fully testable without a real browser
- **CLI Interface** — interactive REPL and script execution

## Supported Commands

| Command | Example |
|---------|---------|
| Navigate | `go to example.com` |
| Click | `click the login button` |
| Type | `type hello in the search box` |
| Scroll | `scroll down` |
| Extract | `extract the text from the heading` |
| Wait | `wait for 3 seconds` |
| Screenshot | `take a screenshot` |
| Back/Forward | `go back` / `go forward` |
| Search | `search for machine learning` |

## Quickstart

```bash
# Clone
git clone https://github.com/MukundaKatta/loki.git
cd loki

# Install
pip install -e ".[dev]"

# Run tests
make test

# Interactive mode
python -m loki run
```

### Example Session

```
loki> go to github.com
{"status": "ok", "url": "https://github.com"}

loki> click the sign in button
{"status": "ok", "clicked": "sign in"}

loki> type myuser in the username field
{"status": "ok", "typed": "myuser", "target": "username field"}
```

### Script Execution

```bash
# Create a script
cat > script.loki << 'EOF'
go to example.com
click the login button
type admin in the username field
type secret in the password field
click the submit button
EOF

# Run it
python -m loki execute script.loki
```

## Architecture

```
User command (text)
  -> NLCommandParser.parse()  -> List[Action]
  -> ActionExecutor.execute() -> result dict
  -> BrowserSession           -> state tracking
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

## Project Structure

```
loki/
├── src/loki/
│   ├── core.py      BrowserAgent, Action, ActionExecutor
│   ├── parser.py    NLCommandParser (regex-based)
│   ├── session.py   BrowserSession (URL history, cookies, data)
│   ├── config.py    Configuration dataclass
│   └── cli.py       CLI entry points
├── tests/
│   ├── test_core.py
│   ├── test_parser.py
│   └── test_session.py
├── docs/
│   └── ARCHITECTURE.md
└── pyproject.toml
```

## Live Demo

Visit the landing page: **https://MukundaKatta.github.io/loki/**

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — See [LICENSE](LICENSE) for details.

Part of the [Mythological Portfolio](https://github.com/MukundaKatta) by Officethree Technologies.
