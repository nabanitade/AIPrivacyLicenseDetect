#!/usr/bin/env python3
"""
End-to-end test of the AI Privacy License Detector using mocked HTTP responses.
This tests all detection methods without requiring internet access.

Usage: python3 test_detector_demo.py
"""

import json
import responses
from ai_privacy_license_detector import AIPrivacyLicenseDetector

BASE = "https://example.com"

LICENSE_TEXT = """AI Privacy License - AiPrivacyLicense-1.0
Do Not Train Flag: not allowed for training
Commercial Use Permitted: yes
Attribution Required: true
Attribution Text: Example Co. Data
Data Owner Name: Example Co.
"""

@responses.activate
def run_demo():
    """Test all detection methods with mocked responses"""
    print("🚀 Testing AI Privacy License Detector End-to-End")
    print("=" * 50)
    
    # 1. robots.txt announces the license location
    responses.add(
        responses.GET, f"{BASE}/robots.txt",
        body="User-agent: *\nDisallow:\nAI-Privacy-License-Link: /.well-known/ai-privacy-license\n",
        status=200,
        content_type="text/plain",
    )
    print("✅ Mocked robots.txt with license link")

    # 2. Root page with HTML hints + JSON-LD and a Link: rel=license header
    html = """
    <html>
      <head>
        <meta name="ai-privacy-license-link" content="/.well-known/ai-privacy-license" />
        <link rel="license" href="/license/AiPrivacyLicense-1.0.txt" />
        <script type="application/ld+json">
        {
          "@context":"https://schema.org",
          "@type":"WebPage",
          "license":"https://example.com/AiPrivacyLicense-1.0.txt"
        }
        </script>
      </head>
      <body>Hello</body>
    </html>
    """
    
    # HEAD request with Link header
    responses.add(
        responses.HEAD, BASE,
        headers={
            "Link": '</license/AiPrivacyLicense-1.0.txt>; rel="license"'
        },
        status=200,
    )
    
    # GET request with HTML content and Link header
    responses.add(
        responses.GET, BASE,
        body=html,
        status=200,
        content_type="text/html; charset=utf-8",
        headers={
            "Link": '</license/AiPrivacyLicense-1.0.txt>; rel="license"'
        },
    )
    print("✅ Mocked HTML page with meta tags, link tags, and JSON-LD")

    # 3. Common license endpoints
    responses.add(
        responses.GET, f"{BASE}/.well-known/ai-privacy-license",
        body=LICENSE_TEXT,
        status=200,
        content_type="text/plain",
    )
    responses.add(
        responses.GET, f"{BASE}/license/AiPrivacyLicense-1.0.txt",
        body=LICENSE_TEXT,
        status=200,
        content_type="text/plain",
    )
    responses.add(
        responses.GET, f"{BASE}/AiPrivacyLicense-1.0.txt",
        body=LICENSE_TEXT,
        status=200,
        content_type="text/plain",
    )
    print("✅ Mocked license file endpoints")

    # Test the detector
    print("\n🔍 Running detector...")
    detector = AIPrivacyLicenseDetector(verbose=True)
    
    try:
        result = detector.check_website(BASE)
        
        print("\n📊 Detection Results:")
        print("-" * 30)
        print(f"URL: {result.url}")
        print(f"Has License: {result.has_license}")
        print(f"License Type: {result.license_type}")
        print(f"License URL: {result.license_url}")
        print(f"Detection Methods: {result.detection_methods}")
        
        if result.restrictions:
            print(f"\n🔒 License Restrictions:")
            print(f"  - Allow Training: {result.restrictions.allow_training}")
            print(f"  - Attribution Required: {result.restrictions.attribution_required}")
            print(f"  - Allow Commercial: {result.restrictions.allow_commercial}")
            print(f"  - Do Not Train: {result.restrictions.do_not_train}")
            print(f"  - Attribution Text: {result.restrictions.attribution_text}")
            print(f"  - Data Owner: {result.restrictions.data_owner}")
        
        print(f"\n📋 Full JSON Result:")
        print(json.dumps(result.as_dict(), indent=2))
        
        # Verify all detection methods were found
        expected_methods = [
            "_check_robots_txt",
            "_check_http_headers", 
            "_check_html_sources",
            "_check_license_file"
        ]
        
        print(f"\n✅ Verification:")
        for method in expected_methods:
            if method in result.detection_methods:
                print(f"  ✓ {method} - Found")
            else:
                print(f"  ✗ {method} - Missing")
                
        if result.has_license:
            print(f"\n🎉 SUCCESS: License detected via {len(result.detection_methods)} methods!")
        else:
            print(f"\n❌ FAILED: No license detected")
            
    finally:
        detector.close()
        print("\n🧹 Detector closed")

if __name__ == "__main__":
    try:
        run_demo()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Install required packages: pip install responses")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
