#!/usr/bin/env python3
"""
🎮 Interactive Website Testing Script for AI Privacy License Detector

This script provides an interactive way to test websites for AI Privacy License detection.
Perfect for exploring and learning how the detector works.

Usage:
    python3 interactive_test.py
"""

import sys
import time
from datetime import datetime
from ai_privacy_license_detector import AIPrivacyLicenseDetector


def print_header():
    """Print a nice header for the interactive test."""
    print("🎮 AI Privacy License Detector - Interactive Test")
    print("=" * 60)
    print("Type 'help' for commands, 'quit' to exit")
    print()


def print_help():
    """Print help information."""
    print("\n📖 Available Commands:")
    print("  test <url>           - Test a single website")
    print("  methods <url>        - Test individual detection methods")
    print("  cli <url>            - Test CLI equivalent")
    print("  compare <url1> <url2> - Compare two websites")
    print("  help                 - Show this help message")
    print("  quit                 - Exit the program")
    print("  clear                - Clear the screen")
    print("\n📝 Examples:")
    print("  test https://example.com")
    print("  methods https://example.com")
    print("  compare https://site1.com https://site2.com")
    print()


def validate_url(url: str) -> bool:
    """Validate if a URL is properly formatted."""
    return url.startswith(('http://', 'https://'))


def test_website(url: str, detector: AIPrivacyLicenseDetector):
    """Test a website and display results."""
    print(f"\n🔍 Testing: {url}")
    print("-" * 40)
    
    start_time = time.time()
    
    try:
        result = detector.check_website(url)
        elapsed = time.time() - start_time
        
        print(f"✅ Completed in {elapsed:.2f} seconds")
        print(f"🛡️  Has License: {result.has_license}")
        print(f"🔗 License URL: {result.license_url}")
        print(f"📋 License Type: {result.license_type}")
        print(f"🔍 Detection Methods: {result.detection_methods}")
        
        if result.restrictions:
            print(f"🎯 Allow Training: {result.restrictions.allow_training}")
            print(f"💼 Allow Commercial: {result.restrictions.allow_commercial}")
            print(f"📝 Attribution Required: {result.restrictions.attribution_required}")
            if result.restrictions.attribution_text:
                print(f"📄 Attribution Text: {result.restrictions.attribution_text}")
        else:
            print("🚫 No restrictions detected")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def test_individual_methods(url: str, detector: AIPrivacyLicenseDetector):
    """Test individual detection methods for a website."""
    print(f"\n🔬 Testing individual methods for: {url}")
    print("-" * 50)
    
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


def test_cli_equivalent(url: str):
    """Test the CLI equivalent for a website."""
    print(f"\n🖥️  Testing CLI equivalent for: {url}")
    print("-" * 45)
    
    try:
        import subprocess
        cmd = [sys.executable, "-m", "ai_privacy_license_detector.cli", "--verbose", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ CLI test successful")
            print("Output:")
            for line in result.stdout.strip().split('\n'):
                print(f"   {line}")
        else:
            print(f"❌ CLI test failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ CLI test failed: {e}")


def compare_websites(url1: str, url2: str, detector: AIPrivacyLicenseDetector):
    """Compare two websites."""
    print(f"\n🔄 Comparing websites:")
    print(f"   1. {url1}")
    print(f"   2. {url2}")
    print("-" * 50)
    
    results = []
    for i, url in enumerate([url1, url2], 1):
        print(f"\n🔍 Testing {i}: {url}")
        try:
            start_time = time.time()
            result = detector.check_website(url)
            elapsed = time.time() - start_time
            
            results.append({
                "url": url,
                "has_license": result.has_license,
                "elapsed": elapsed,
                "methods": result.detection_methods
            })
            
            print(f"   ✅ Has License: {result.has_license}")
            print(f"   ⏱️  Time: {elapsed:.2f}s")
            print(f"   🔍 Methods: {result.detection_methods}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({"url": url, "error": str(e)})
    
    # Show comparison
    if len(results) == 2 and "error" not in results[0] and "error" not in results[1]:
        print(f"\n📊 Comparison Summary:")
        print(f"   Site 1 ({url1}): {'🛡️' if results[0]['has_license'] else '🚫'}")
        print(f"   Site 2 ({url2}): {'🛡️' if results[1]['has_license'] else '🚫'}")
        
        if results[0]['has_license'] != results[1]['has_license']:
            print(f"   🎯 Difference: One site has a license, the other doesn't")
        else:
            print(f"   🎯 Both sites have the same license status")


def clear_screen():
    """Clear the screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Main interactive loop."""
    print_header()
    
    # Initialize detector
    try:
        detector = AIPrivacyLicenseDetector()
        print("✅ Detector initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize detector: {e}")
        sys.exit(1)
    
    print("\n🚀 Ready to test websites! Type 'help' for commands.")
    
    while True:
        try:
            command = input("\n🎮 > ").strip()
            
            if not command:
                continue
                
            parts = command.split()
            cmd = parts[0].lower()
            
            if cmd == 'quit' or cmd == 'exit':
                print("👋 Goodbye!")
                break
                
            elif cmd == 'help':
                print_help()
                
            elif cmd == 'clear':
                clear_screen()
                print_header()
                
            elif cmd == 'test' and len(parts) >= 2:
                url = parts[1]
                if validate_url(url):
                    test_website(url, detector)
                else:
                    print("❌ Invalid URL. Must start with http:// or https://")
                    
            elif cmd == 'methods' and len(parts) >= 2:
                url = parts[1]
                if validate_url(url):
                    test_individual_methods(url, detector)
                else:
                    print("❌ Invalid URL. Must start with http:// or https://")
                    
            elif cmd == 'cli' and len(parts) >= 2:
                url = parts[1]
                if validate_url(url):
                    test_cli_equivalent(url)
                else:
                    print("❌ Invalid URL. Must start with http:// or https://")
                    
            elif cmd == 'compare' and len(parts) >= 3:
                url1, url2 = parts[1], parts[2]
                if validate_url(url1) and validate_url(url2):
                    compare_websites(url1, url2, detector)
                else:
                    print("❌ Invalid URLs. Both must start with http:// or https://")
                    
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
