#!/usr/bin/env python3
"""
🌐 Website Testing Script for AI Privacy License Detector

This script provides comprehensive testing of any website for AI Privacy License detection.
It tests all detection methods and provides detailed output.

Usage:
    python3 test_website.py https://example.com
    python3 test_website.py --verbose https://example.com
    python3 test_website.py --all-methods https://example.com
"""

import argparse
import sys
import time
from datetime import datetime
from ai_privacy_license_detector import AIPrivacyLicenseDetector


def print_header():
    """Print a nice header for the test."""
    print("🌐 AI Privacy License Detector - Website Test")
    print("=" * 60)
    print()


def test_website(url, verbose=False, all_methods=False):
    """Test a website for AI Privacy License detection."""
    
    print(f"🔍 Testing website: {url}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    # Initialize detector
    try:
        detector = AIPrivacyLicenseDetector()
        print("✅ Detector initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize detector: {e}")
        return False
    
    # Test 1: Full website check
    print("\n📋 Test 1: Full Website Check")
    print("-" * 30)
    start_time = time.time()
    
    try:
        result = detector.check_website(url)
        elapsed = time.time() - start_time
        
        print(f"✅ Website check completed in {elapsed:.2f} seconds")
        print(f"   Has License: {result.has_license}")
        print(f"   License URL: {result.license_url}")
        print(f"   License Type: {result.license_type}")
        print(f"   Detection Methods: {result.detection_methods}")
        print(f"   Error: {result.error}")
        print(f"   Timestamp: {result.timestamp}")
        
        if result.restrictions:
            print(f"   Allow Training: {result.restrictions.allow_training}")
            print(f"   Allow Commercial: {result.restrictions.allow_commercial}")
            print(f"   Attribution Required: {result.restrictions.attribution_required}")
            if result.restrictions.attribution_text:
                print(f"   Attribution Text: {result.restrictions.attribution_text}")
        else:
            print("   No restrictions detected")
            
    except Exception as e:
        print(f"❌ Website check failed: {e}")
        return False
    
    # Test 2: Individual detection methods (if requested)
    if all_methods:
        print("\n🔬 Test 2: Individual Detection Methods")
        print("-" * 40)
        
        methods = [
            ("HTTP Headers", detector._check_http_headers),
            ("robots.txt", detector._check_robots_txt),
            ("HTML Sources", detector._check_html_sources),
            ("License Files", detector._check_license_file),
        ]
        
        for method_name, method_func in methods:
            print(f"\n   Testing {method_name}...")
            try:
                start_time = time.time()
                result = method_func(url)
                elapsed = time.time() - start_time
                
                print(f"      ✅ Completed in {elapsed:.2f}s")
                print(f"      Result: {result}")
                
            except Exception as e:
                print(f"      ❌ Failed: {e}")
    
    # Test 3: CLI equivalent test
    if verbose:
        print("\n🖥️  Test 3: CLI Equivalent")
        print("-" * 30)
        
        try:
            import subprocess
            cmd = [sys.executable, "-m", "ai_privacy_license_detector.cli", "--verbose", url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ CLI test successful")
                print("   Output:")
                for line in result.stdout.strip().split('\n'):
                    print(f"      {line}")
            else:
                print(f"❌ CLI test failed with return code {result.returncode}")
                print(f"   Error: {result.stderr}")
                
        except Exception as e:
            print(f"❌ CLI test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Website testing completed!")
    return True


def main():
    """Main function to handle command line arguments and run tests."""
    parser = argparse.ArgumentParser(
        description="Test a website for AI Privacy License detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 test_website.py https://example.com
    python3 test_website.py --verbose https://example.com
    python3 test_website.py --all-methods https://example.com
    python3 test_website.py --verbose --all-methods https://example.com
        """
    )
    
    parser.add_argument("url", help="URL to test")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Enable verbose output including CLI test")
    parser.add_argument("--all-methods", "-a", action="store_true",
                       help="Test all individual detection methods")
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print("❌ Error: URL must start with http:// or https://")
        sys.exit(1)
    
    print_header()
    
    # Run the test
    success = test_website(args.url, args.verbose, args.all_methods)
    
    if success:
        print("🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("💥 Some tests failed. Check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
