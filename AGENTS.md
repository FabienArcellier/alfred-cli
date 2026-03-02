# AGENTS.md - Guidelines for AI Coding Agents

This file contains essential information for AI agents working on the alfred-cli codebase.

## Build/Lint/Test Commands

This project uses Poetry for dependency management and alfred (self-hosted) for task running.

```bash
# Install dependencies
poetry install

# Run all tests
poetry run alfred tests
# Or directly with pytest
poetry run pytest

# Run specific test categories
poetry run alfred tests:units          # Unit tests only
poetry run alfred tests:integrations   # Integration tests only
poetry run alfred tests:acceptances    # Acceptance tests only

# Run a single test file
poetry run pytest tests/units/test_main.py

# Run a single test function
poetry run pytest tests/units/test_main.py::test_env_should_inject_environment_variable_in_sh_invocation

# Run with verbose output
poetry run pytest -v tests/units/test_main.py

# Run linting
poetry run alfred lint
# Or directly
poetry run pylint src/alfred

# Check alfred commands are functional
poetry run alfred alfred_check

# Build distribution
poetry build

# Run the CLI locally
poetry run alfred --help
```

## Code Style Guidelines

### Python Version
- **Python 3.8+** is required
- Target Python 3.9 for pylint checks

### Formatting
- **Indentation**: 4 spaces (no tabs)
- **Line endings**: LF (Unix-style)
- **Max line length**: 180 characters
- **Charset**: UTF-8
- **Trailing whitespace**: Trimmed
- **Final newline**: Required in all files except `*.tpl`

### Naming Conventions
- **Modules**: `snake_case`
- **Classes**: `PascalCase`
- **Functions/Methods**: `snake_case`
- **Variables**: `snake_case`
- **Constants**: `UPPER_CASE`
- **Private attributes**: Prefix with underscore `_`
- **Type variables**: Follow naming style (PascalCase preferred)

### Imports
- Group imports: stdlib first, then third-party, then local
- Use absolute imports for project modules
- Avoid wildcard imports (`from module import *`)
- Example:
```python
import os
import sys
from typing import List, Optional

import click

from alfred import ctx, manifest, echo
from alfred.lib import ROOT_DIR
```

### Type Hints
- Use type hints for function parameters and return values
- Import from `typing` module: `List`, `Dict`, `Optional`, `Union`, `Callable`, etc.
- Example: `def run(command: str, args: List[str]) -> Tuple[int, str, str]:`

### Error Handling
- Catch specific exceptions, avoid bare `except:`
- Use `alfred.exceptions` for custom exceptions
- For CLI errors, use `echo.error()` and exit with non-zero code
- Avoid catching `BaseException` or `Exception` unless re-raising

### Documentation
- Docstrings are **not required** for modules, classes, or functions (disabled in pylint)
- When used, follow Google style or standard conventions
- Use inline comments sparingly, only for complex logic

### Code Structure
- **Max function arguments**: 5
- **Max function locals**: 15
- **Max function branches**: 12
- **Max function returns**: 6
- **Max function statements**: 50
- **Max nested blocks**: 5
- **Max class attributes**: 7
- **Min public methods per class**: 2 (except exceptions)

### Pylint Configuration
Key disabled rules (see `.pylintrc`):
- `missing-module-docstring`
- `missing-function-docstring`
- `missing-class-docstring`
- `too-few-public-methods`
- `logging-fstring-interpolation` (use % formatting for logging)
- `no-else-return` and `no-else-raise`
- `cyclic-import`

### Testing
- Use **pytest** as the test framework
- Test files: `tests/units/`, `tests/integrations/`, `tests/acceptances/`
- Use **fixtup** for fixtures (configured in `pyproject.toml`)
- Fixtures location: `tests/fixtures/`
- Use `@pytest.mark.skipif` for platform-specific tests
- Import `alfred` module for testing: `import alfred`

### Project Structure
```
src/alfred/           # Main source code
alfred/               # Project alfred commands (build tasks)
tests/                # Test suites
docs/                 # Sphinx documentation
```

### Dependencies
- **CLI Framework**: Click (^8.1.0)
- **Configuration**: toml (^0.10)
- **Shell detection**: shellingham (^1.3.0)
- **Prompts**: prompt-toolkit (^3.0.41)

### Git Workflow
- No specific branch naming conventions enforced
- Ensure `alfred alfred_check` passes before committing
- Run full test suite: `alfred tests`

### Notes
- This is a CLI tool for automation and build scripts
- Commands are defined using `@alfred.command()` decorator
- The tool supports shell completion and virtual environment detection
- Keep heavy imports behind `alfred.CMD_RUNNING()` check for faster CLI startup
