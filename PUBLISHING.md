# Publishing to PyPI

This document is for maintainers who publish the `ai-privacy-license-detector` package to PyPI.

## Prerequisites

- [PyPI](https://pypi.org) account and [Test PyPI](https://test.pypi.org) account (for dry runs)
- `build` and `twine` installed: `pip install build twine`

## 1. Bump version (if needed)

- Update `version` in `pyproject.toml`
- Update `__version__` in `ai_privacy_license_detector/detector.py`
- Add a new section in `CHANGELOG.md` for the release

## 2. Build the package

From the project root:

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build source distribution and wheel
python -m build
```

This creates `dist/ai_privacy_license_detector-<version>.tar.gz` and `dist/ai_privacy_license_detector-<version>-py3-none-any.whl`.

## 3. Check the build (optional)

```bash
twine check dist/*
```

## 4. Upload to Test PyPI (recommended first)

```bash
twine upload --repository testpypi dist/*
```

You will be prompted for your Test PyPI username and password (or use `__token__` and an API token). Then test install:

```bash
pip install --index-url https://test.pypi.org/simple/ ai-privacy-license-detector
```

## 5. Upload to PyPI

When ready for production:

```bash
twine upload dist/*
```

Use your PyPI username and password, or `__token__` with a PyPI API token (recommended). Create tokens at [pypi.org/manage/account/token/](https://pypi.org/manage/account/token/).

## 6. Verify

```bash
pip install ai-privacy-license-detector
ai-license --version
```

## Notes

- Do not upload the same version twice; PyPI does not allow overwriting.
- Store API tokens securely (e.g. environment variables or keyring); never commit them.
