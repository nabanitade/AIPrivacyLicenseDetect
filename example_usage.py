#!/usr/bin/env python3
"""
Simple example of using the AI Privacy License Detector with real URLs.
This shows the basic 2-line integration pattern.

Usage: python3 example_usage.py
"""

from ai_privacy_license_detector import check_url, AIPrivacyLicenseDetector

def simple_check():
    """Simple 2-line integration example"""
    print("🚀 Simple 2-line Integration Example")
    print("=" * 40)
    
    # Example URL (replace with a real site that has AI Privacy License)
    url = "https://example.com"  # Replace with actual URL
    
    print(f"Checking: {url}")
    
    # The famous 2-line integration!
    result = check_url(url)
    print(json.dumps(result.as_dict(), indent=2))

def batch_check():
    """Batch URL checking example"""
    print("\n📋 Batch URL Checking Example")
    print("=" * 40)
    
    urls = [
        "https://example1.com",
        "https://example2.com", 
        "https://example3.com"
    ]
    
    print(f"Checking {len(urls)} URLs...")
    
    with AIPrivacyLicenseDetector(verbose=True) as detector:
        results = detector.check_batch_urls(urls)
        
        for i, result in enumerate(results):
            print(f"\n{i+1}. {result.url}")
            print(f"   License: {'✅' if result.has_license else '❌'}")
            if result.has_license:
                print(f"   Type: {result.license_type}")
                print(f"   URL: {result.license_url}")
                print(f"   Methods: {', '.join(result.detection_methods)}")

def custom_config():
    """Custom configuration example"""
    print("\n⚙️  Custom Configuration Example")
    print("=" * 40)
    
    url = "https://example.com"  # Replace with actual URL
    
    # Custom timeout, user agent, and SSL settings
    detector = AIPrivacyLicenseDetector(
        timeout=30,  # 30 second timeout
        user_agent="MyApp/1.0 (AI-Privacy-License-Check)",
        verbose=True,
        insecure_ssl=False,  # Always verify SSL in production
        max_bytes=256 * 1024  # 256KB max content
    )
    
    try:
        result = detector.check_website(url)
        print(f"Result: {result.has_license}")
        if result.has_license:
            print(f"License: {result.license_url}")
            print(f"Restrictions: {result.restrictions}")
    finally:
        detector.close()

if __name__ == "__main__":
    import json
    
    try:
        # Run examples
        simple_check()
        batch_check() 
        custom_config()
        
        print("\n🎉 All examples completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure the detector module is installed and accessible")
    except Exception as e:
        print(f"❌ Example failed: {e}")
        import traceback
        traceback.print_exc()
