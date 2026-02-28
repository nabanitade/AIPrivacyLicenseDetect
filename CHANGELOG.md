# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-02-28

### Added
- Initial release of AI Privacy License Detector
- Core detection methods: robots.txt, HTTP headers, meta tags, JSON-LD, license files
- Comprehensive URL sanitization and SSRF protection
- Support for multi-value headers and complex JSON-LD structures
- Context manager support for proper resource cleanup
- Convenience function `check_url()` for simple use cases
- Comprehensive test suite with offline testing
- Security documentation and contributing guidelines

### Features
- **Detection Methods**: Five different ways to find AI Privacy Licenses
- **Security First**: Blocks private IPs, odd ports, credentials, and malicious schemes
- **Performance**: Streaming responses, byte limits, timeout protection
- **Developer Experience**: Clean API, type hints, comprehensive documentation
- **Enterprise Safe**: Zero proprietary features exposed, focused detection only

### Security
- SSRF protection against localhost and private IP ranges
- Port restrictions to standard HTTP/HTTPS ports (80/443)
- Credential blocking in URLs
- Content-type guards and byte capping
- Redirect limits and timeout protection

### API
- `AIPrivacyLicenseDetector.check_website(url)` - Main detection method
- `AIPrivacyLicenseDetector.check_batch_urls(urls)` - Batch processing
- `LicenseDetectionResult` - Structured detection results
- `LicenseRestriction` - Parsed license restrictions
- Context manager support for automatic cleanup

### Documentation
- Clear scope definition (detection only, no policy decisions)
- Security features explanation
- Contributing guidelines
- Code of conduct
- Comprehensive examples

---

## Open source release (2025-02-28)
- Repository prepared for public release under Apache License 2.0
- README, pyproject.toml, and docs aligned with nabanitade/aiprivacylicenseSDK
- NOTICE.MD and LICENSE updated; PyPI publishing instructions added
