# AI Privacy License Detector Documentation

This directory contains documentation for the AI Privacy License Detector library.

## Overview

The AI Privacy License Detector is a Python library that helps AI companies detect and respect AI Privacy Licenses when crawling websites, processing user queries, or building training datasets.

## Quick Start

```python
from ai_privacy_license_detector import AIPrivacyLicenseDetector

# Initialize detector
detector = AIPrivacyLicenseDetector(verbose=True)

# Check a website
result = detector.check_website("https://example.com")

if result.has_license:
    print(f"License detected: {result.license_type}")
    # Check if crawling is allowed
    decision = detector.should_proceed_with_crawling(result.restrictions)
    print(f"Can crawl: {decision['proceed']}")
```

## Features

- **License Detection**: Automatically detect AI Privacy Licenses from websites
- **Terms of Service Analysis**: Parse ToS documents for AI usage restrictions
- **Real-time Query Handling**: Handle user queries with URL restrictions
- **User Response Generation**: Create user-friendly messages about restrictions
- **CLI Tool**: Command-line interface for batch processing
- **Framework Integration**: Examples for Scrapy, PyTorch, LangChain, etc.

## Installation

```bash
pip install ai-privacy-license-detector
```

## Documentation Sections

- [API Reference](api.md) - Complete API documentation
- [Integration Examples](integrations.md) - Framework-specific examples
- [CLI Usage](cli.md) - Command-line tool documentation
- [Configuration](configuration.md) - Setup and configuration options

## License

Apache License 2.0 - see LICENSE file for details.
