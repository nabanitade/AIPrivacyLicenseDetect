#!/usr/bin/env python3
"""
🌐🌐🌐 Batch Website Testing Script for AI Privacy License Detector

This script tests multiple websites for AI Privacy License detection.
Perfect for testing multiple sites or comparing results.

Usage:
    python3 test_multiple_websites.py urls.txt
    python3 test_multiple_websites.py --urls https://site1.com https://site2.com
    python3 test_multiple_websites.py --from-file urls.txt --output results.json
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from ai_privacy_license_detector import AIPrivacyLicenseDetector


def print_header():
    """Print a nice header for the batch test."""
    print("🌐🌐🌐 AI Privacy License Detector - Batch Website Test")
    print("=" * 70)
    print()


def load_urls_from_file(filename: str) -> List[str]:
    """Load URLs from a text file (one URL per line)."""
    try:
        with open(filename, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return urls
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file '{filename}': {e}")
        sys.exit(1)


def validate_url(url: str) -> bool:
    """Validate if a URL is properly formatted."""
    return url.startswith(('http://', 'https://'))


def test_single_website(detector: AIPrivacyLicenseDetector, url: str) -> Dict[str, Any]:
    """Test a single website and return results."""
    start_time = time.time()
    
    try:
        result = detector.check_website(url)
        elapsed = time.time() - start_time
        
        return {
            "url": url,
            "success": True,
            "elapsed_time": round(elapsed, 2),
            "has_license": result.has_license,
            "license_url": result.license_url,
            "license_type": result.license_type,
            "detection_methods": result.detection_methods,
            "error": result.error,
            "timestamp": result.timestamp.isoformat() if result.timestamp else None,
            "restrictions": {
                "allow_training": result.restrictions.allow_training if result.restrictions else None,
                "allow_commercial": result.restrictions.allow_commercial if result.restrictions else None,
                "attribution_required": result.restrictions.attribution_required if result.restrictions else None,
                "attribution_text": result.restrictions.attribution_text if result.restrictions else None,
            } if result.restrictions else None
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "url": url,
            "success": False,
            "elapsed_time": round(elapsed, 2),
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def print_results_summary(results: List[Dict[str, Any]]):
    """Print a summary of all test results."""
    print("\n📊 Test Results Summary")
    print("=" * 50)
    
    total = len(results)
    successful = sum(1 for r in results if r["success"])
    failed = total - successful
    
    licenses_found = sum(1 for r in results if r["success"] and r["has_license"])
    no_licenses = successful - licenses_found
    
    print(f"🌐 Total websites tested: {total}")
    print(f"✅ Successful tests: {successful}")
    print(f"❌ Failed tests: {failed}")
    print(f"🛡️  Licenses found: {licenses_found}")
    print(f"🚫 No licenses: {no_licenses}")
    
    if successful > 0:
        avg_time = sum(r["elapsed_time"] for r in results if r["success"]) / successful
        print(f"⏱️  Average test time: {avg_time:.2f}s")
    
    print()


def print_detailed_results(results: List[Dict[str, Any]], verbose: bool = False):
    """Print detailed results for each website."""
    print("\n🔍 Detailed Results")
    print("=" * 50)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['url']}")
        print("   " + "-" * (len(result['url']) + 2))
        
        if result["success"]:
            print(f"   ✅ Status: Success ({result['elapsed_time']}s)")
            print(f"   🛡️  Has License: {result['has_license']}")
            
            if result['has_license']:
                print(f"   🔗 License URL: {result['license_url']}")
                print(f"   📋 License Type: {result['license_type']}")
                print(f"   🔍 Detection Methods: {result['detection_methods']}")
                
                if result['restrictions']:
                    print(f"   🎯 Allow Training: {result['restrictions']['allow_training']}")
                    print(f"   💼 Allow Commercial: {result['restrictions']['allow_commercial']}")
                    print(f"   📝 Attribution Required: {result['restrictions']['attribution_required']}")
                    if result['restrictions']['attribution_text']:
                        print(f"   📄 Attribution Text: {result['restrictions']['attribution_text']}")
        else:
            print(f"   ❌ Status: Failed ({result['elapsed_time']}s)")
            print(f"   💥 Error: {result['error']}")
        
        if verbose and result["success"]:
            print(f"   ⏰ Timestamp: {result['timestamp']}")


def save_results_to_file(results: List[Dict[str, Any]], filename: str):
    """Save results to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"💾 Results saved to: {filename}")
    except Exception as e:
        print(f"❌ Error saving results: {e}")


def main():
    """Main function to handle command line arguments and run batch tests."""
    parser = argparse.ArgumentParser(
        description="Test multiple websites for AI Privacy License detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 test_multiple_websites.py --from-file urls.txt
    python3 test_multiple_websites.py --urls https://site1.com https://site2.com
    python3 test_multiple_websites.py --from-file urls.txt --output results.json
    python3 test_multiple_websites.py --urls https://example.com --verbose
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--from-file", "-f", metavar="FILE",
                      help="Load URLs from a text file (one URL per line)")
    group.add_argument("--urls", "-u", nargs="+", metavar="URL",
                      help="List of URLs to test")
    
    parser.add_argument("--output", "-o", metavar="FILE",
                       help="Save results to JSON file")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("--summary-only", "-s", action="store_true",
                       help="Show only summary, not detailed results")
    
    args = parser.parse_args()
    
    # Load URLs
    if args.from_file:
        urls = load_urls_from_file(args.from_file)
        print(f"📁 Loaded {len(urls)} URLs from file: {args.from_file}")
    else:
        urls = args.urls
        print(f"🔗 Testing {len(urls)} URLs from command line")
    
    # Validate URLs
    invalid_urls = [url for url in urls if not validate_url(url)]
    if invalid_urls:
        print(f"❌ Invalid URLs found: {invalid_urls}")
        sys.exit(1)
    
    print_header()
    print(f"🚀 Starting batch test of {len(urls)} websites...")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize detector
    try:
        detector = AIPrivacyLicenseDetector()
        print("✅ Detector initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize detector: {e}")
        sys.exit(1)
    
    # Test all websites
    results = []
    for i, url in enumerate(urls, 1):
        print(f"🔍 Testing {i}/{len(urls)}: {url}")
        result = test_single_website(detector, url)
        results.append(result)
        
        # Small delay between requests to be respectful
        if i < len(urls):
            time.sleep(0.5)
    
    # Print results
    print_results_summary(results)
    
    if not args.summary_only:
        print_detailed_results(results, args.verbose)
    
    # Save results if requested
    if args.output:
        save_results_to_file(results, args.output)
    
    print("\n" + "=" * 70)
    print("🎯 Batch testing completed!")
    
    # Exit with appropriate code
    failed_tests = sum(1 for r in results if not r["success"])
    if failed_tests > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
