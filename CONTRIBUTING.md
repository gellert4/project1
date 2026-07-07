# Contributing to Sherlock

Thank you for your interest in contributing to Sherlock! Here's how to help:

## Getting Started

1. **Fork the repository**
2. **Clone your fork** and create a feature branch
3. **Install dependencies** (see Development section in README)
4. **Make your changes** with clear commit messages
5. **Test your changes** with `pytest`
6. **Submit a Pull Request** with a clear description

## Development Workflow

### Setup Local Environment

```bash
python -m venv venv
source venv/bin/activate  # Unix/Mac
venv\Scripts\activate     # Windows

pip install -r backend/requirements.txt
```

### Running Tests

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=backend test_*.py

# Run specific test
pytest test_api.py::test_health_check -v
```

### Code Style

- Follow PEP 8
- Use 4 spaces for indentation
- Add docstrings to all functions/classes
- Type hints where possible

### Commit Message Format

```
<type>: <description>

<body>

<footer>
```

Examples:
- `feat: add PDF support for case files`
- `fix: handle empty vector store error`
- `docs: update API endpoint documentation`
- `test: add integration tests for query engine`

## What We're Looking For

- Bug fixes with test coverage
- Performance improvements
- Documentation improvements
- New features (please open an issue first to discuss)
- Test coverage improvements

## Code Review Process

1. Submit PR with description of changes
2. CI tests must pass
3. Code review by maintainers
4. Address feedback
5. Merge and deploy

## Reporting Issues

Found a bug? Have a suggestion?

1. Check existing issues first
2. Provide clear reproduction steps
3. Include relevant logs/screenshots
4. Describe expected vs actual behavior

## Questions?

Open a discussion or issue with the `question` label.

Thank you for contributing!
