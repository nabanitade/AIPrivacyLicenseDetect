# Contributing

Thank you for your interest in contributing to the AI Privacy License Detector!

## What This Library Does

This library detects machine-readable AI Privacy License declarations via:
- HTTP headers (`ai-privacy-license-link`)
- HTML meta tags
- JSON-LD structured data
- robots.txt directives
- Common license file paths

## What This Library Does NOT Do

- Parse Terms of Service or free-text policies
- Provide legal advice or risk scoring
- Crawl site content or ignore robots.txt
- Make policy decisions about data usage

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -e .[dev]`
3. Run tests: `pytest tests/ -v`

## Adding Features

### ✅ Safe to Add
- New detection methods for machine-readable signals
- Improved parsing of existing license fields
- Better error handling and logging
- Performance optimizations
- Additional test coverage

### ❌ Do NOT Add
- ToS/NLP parsing or classifiers
- Risk scoring or policy engines
- Compliance reporting or dashboards
- Dataset/crawler adapters
- Enterprise-specific features

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings for public methods
- Keep functions focused and small
- Write tests for new functionality

## Testing

- All tests should be offline (no network calls)
- Mock external dependencies
- Test edge cases and error conditions
- Ensure security features work correctly

## Security

- Never add features that could enable SSRF
- Maintain strict URL sanitization
- Keep content parsing safe and limited
- Test security features thoroughly

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Ensure all tests pass
6. Submit a pull request

## Questions?

If you're unsure whether a feature is appropriate, please open an issue to discuss it first.
