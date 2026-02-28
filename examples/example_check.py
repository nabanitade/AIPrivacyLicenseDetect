#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Example: 2-line integration for checking a single website
This is the core use case demonstrated in your pitch
"""

from ai_privacy_license_detector import AIPrivacyLicenseDetector

# The famous 2-line integration
detector = AIPrivacyLicenseDetector()
result = detector.check_website("https://example.com")

# Print results
print(f"URL: {result.url}")
print(f"Has License: {result.has_license}")
if result.has_license:
    print(f"License Type: {result.license_type}")
    print(f"License URL: {result.license_url}")
    if result.restrictions:
        print(f"Allow Training: {result.restrictions.allow_training}")
        print(f"Attribution Required: {result.restrictions.attribution_required}")
        print(f"Allow Commercial: {result.restrictions.allow_commercial}")
        if result.restrictions.do_not_train:
            print(f"Do Not Train: {result.restrictions.do_not_train}")
else:
    print("No AI Privacy License found")

# Get JSON-friendly output
import json
print("\nJSON Output:")
print(json.dumps(result.as_dict(), indent=2))
