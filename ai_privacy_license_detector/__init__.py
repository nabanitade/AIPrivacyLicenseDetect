# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 AI Privacy License Detection Library Contributors
"""
AI Privacy License Detector Package
Detect and respect AI Privacy Licenses when crawling or processing data
"""

from .detector import (
    AIPrivacyLicenseDetector,
    LicenseDetectionResult,
    LicenseRestriction,
    __version__,
)

def check_url(url: str, **kwargs) -> LicenseDetectionResult:
    """
    Convenience function to check a single URL for AI Privacy License
    
    Args:
        url: The website URL to check
        **kwargs: Additional arguments to pass to AIPrivacyLicenseDetector
        
    Returns:
        LicenseDetectionResult with detection information
    """
    detector = AIPrivacyLicenseDetector(**kwargs)
    return detector.check_website(url)

__all__ = [
    "AIPrivacyLicenseDetector",
    "LicenseDetectionResult", 
    "LicenseRestriction",
    "check_url",
    "__version__"
]
