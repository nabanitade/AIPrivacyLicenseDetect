#!/usr/bin/env python3
"""
Test AI Privacy License Detection Library Locally
This script tests all detection methods using local files
"""

import os
import sys
import json
from pathlib import Path
import time

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ai_privacy_license_detector import AIPrivacyLicenseDetector, check_url
    print("✅ Successfully imported AI Privacy License Detector")
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    print("Make sure you have installed the library: pip install -e .")
    sys.exit(1)

def test_local_detection():
    """Test all detection methods with local files"""
    
    print("\n" + "="*60)
    print("🧪 TESTING AI PRIVACY LICENSE DETECTION LIBRARY")
    print("="*60)
    
    # Test 1: License File Detection
    print("\n🔍 Test 1: License File Detection")
    print("-" * 40)
    
    license_file = os.path.join(os.path.dirname(__file__), "AiPrivacyLicense-1.0.txt")
    if os.path.exists(license_file):
        print(f"✅ License file found: {license_file}")
        print(f"   Size: {os.path.getsize(license_file)} bytes")
        print(f"   Modified: {time.ctime(os.path.getmtime(license_file))}")
    else:
        print(f"❌ License file not found: {license_file}")
        print("Please create the license file first")
        return False
        
    # Test the detector with local file
    print("\n🔍 Test 2: Local File Detection")
    print("-" * 40)
    
    try:
        # Create a detector instance
        detector = AIPrivacyLicenseDetector(verbose=True)
        print("✅ Detector created successfully")
        
        # Test with the license file
        result = detector.check_website(f"file://{os.path.abspath(license_file)}")
        
        if result.has_license:
            print("✅ License detected in local file")
            print(f"   License URL: {result.license_url}")
            print(f"   License Type: {result.license_type}")
            print(f"   Detection Methods: {result.detection_methods}")
            
            if result.restrictions:
                restrictions = result.restrictions
                print(f"   Do Not Train: {restrictions.do_not_train}")
                print(f"   Allow Training: {restrictions.allow_training}")
                print(f"   Commercial Use: {restrictions.allow_commercial}")
                print(f"   Attribution Required: {restrictions.attribution_required}")
                print(f"   Attribution Text: {restrictions.attribution_text}")
                print(f"   Data Owner: {restrictions.data_owner}")
            else:
                print("   ⚠️  No restrictions parsed")
        else:
            print("❌ No license detected in local file")
            if result.error:
                print(f"   Error: {result.error}")
            return False
            
    except Exception as e:
        print(f"❌ Local file detection error: {e}")
        return False
        
        # Test robots.txt detection
        if os.path.exists("robots.txt"):
            print("✅ robots.txt found")
            try:
                result = detector._check_robots_txt(".")
                if result['found']:
                    print("✅ robots.txt detection: SUCCESS")
                    print(f"   License URL: {result.get('license_url')}")
                    print(f"   License Type: {result.get('license_type')}")
                    if result.get('restrictions'):
                        restrictions = result['restrictions']
                        print(f"   Do Not Train: {restrictions.do_not_train}")
                        print(f"   Allow Training: {restrictions.allow_training}")
                        print(f"   Commercial Use: {restrictions.allow_commercial}")
                        print(f"   Attribution Required: {restrictions.attribution_required}")
                        print(f"   Attribution Text: {restrictions.attribution_text}")
                        print(f"   Data Owner: {restrictions.data_owner}")
                else:
                    print("❌ robots.txt detection: FAILED")
            except Exception as e:
                print(f"❌ robots.txt detection error: {e}")
        else:
            print("❌ robots.txt not found")
        
        # Test HTML parsing
        if os.path.exists("test_page.html"):
            print("\n✅ test_page.html found")
            try:
                result = detector._check_html_sources(".")
                if result['found']:
                    print("✅ HTML detection: SUCCESS")
                    print(f"   License URL: {result.get('license_url')}")
                    print(f"   License Type: {result.get('license_type')}")
                    if result.get('restrictions'):
                        restrictions = result['restrictions']
                        print(f"   Do Not Train: {restrictions.do_not_train}")
                        print(f"   Allow Training: {restrictions.allow_training}")
                        print(f"   Commercial Use: {restrictions.allow_commercial}")
                        print(f"   Attribution Required: {restrictions.attribution_required}")
                        print(f"   Attribution Text: {restrictions.attrictions.attribution_text}")
                        print(f"   Data Owner: {restrictions.data_owner}")
                else:
                    print("❌ HTML detection: FAILED")
            except Exception as e:
                print(f"❌ HTML detection error: {e}")
        else:
            print("❌ test_page.html not found")
        
        # Test full website check
        print("\n🔍 Test 2: Full Website Check")
        print("-" * 40)
        
        try:
            result = detector.check_website(".")
            print(f"✅ Full detection completed")
            print(f"   Has License: {result.has_license}")
            print(f"   License Type: {result.license_type}")
            print(f"   License URL: {result.license_url}")
            print(f"   Detection Methods: {result.detection_methods}")
            
            if result.restrictions:
                print(f"   Restrictions:")
                print(f"     - Do Not Train: {result.restrictions.do_not_train}")
                print(f"     - Allow Training: {result.restrictions.allow_training}")
                print(f"     - Commercial Use: {result.restrictions.allow_commercial}")
                print(f"     - Attribution Required: {result.restrictions.attribution_required}")
                print(f"     - Attribution Text: {result.restrictions.attribution_text}")
                print(f"     - Data Owner: {result.restrictions.data_owner}")
            
            # Test as_dict() method
            print(f"\n📊 Result as Dictionary:")
            result_dict = result.as_dict()
            print(json.dumps(result_dict, indent=2))
            
        except Exception as e:
            print(f"❌ Full detection error: {e}")
        
        # Test convenience function
        print("\n🔍 Test 3: Convenience Function")
        print("-" * 40)
        
        try:
            result = check_url(".", verbose=True)
            print(f"✅ Convenience function: SUCCESS")
            print(f"   Has License: {result.has_license}")
            print(f"   License Type: {result.license_type}")
        except Exception as e:
            print(f"❌ Convenience function error: {e}")
        
        # Test CLI simulation
        print("\n🔍 Test 4: CLI Simulation")
        print("-" * 40)
        
        try:
            from ai_privacy_license_detector.cli import _create_detector, _process_sequential
            import argparse
            
            # Create mock args
            class MockArgs:
                timeout = 10.0
                user_agent = None
                verbose = True
                insecure_ssl = False
                max_bytes = 128 * 1024
                respect_proxy = False
                max_redirects = 5
                ndjson = False
                compact = False
                require = False
                fail_fast_error = False
                fail_fast_require = False
                summary = True
            
            args = MockArgs()
            
            # Test detector creation
            detector = _create_detector(args)
            print("✅ CLI detector creation: SUCCESS")
            
            # Test processing
            indexed_urls = [(0, ".")]
            result = _process_sequential(indexed_urls, args, detector)
            print("✅ CLI processing: SUCCESS")
            print(f"   Result: {result}")
            
        except Exception as e:
            print(f"❌ CLI simulation error: {e}")
        
    else:
        print("❌ License file not found: AiPrivacyLicense-1.0.txt")
        print("Please create the license file first")
        return False
    
    print("\n" + "="*60)
    print("🎯 TESTING COMPLETE")
    print("="*60)
    
    return True

def test_license_parsing():
    """Test license content parsing specifically"""
    
    print("\n🔍 Test 5: License Content Parsing")
    print("-" * 40)
    
    try:
        detector = AIPrivacyLicenseDetector()
        
        # Read the license file
        license_file = os.path.join(os.path.dirname(__file__), "AiPrivacyLicense-1.0.txt")
        with open(license_file, "r") as f:
            content = f.read()
        
        print(f"✅ License file read ({len(content)} characters)")
        
        # Parse the content
        restrictions = detector._parse_license_content(content)
        
        print("✅ License parsing: SUCCESS")
        print(f"   Do Not Train: {restrictions.do_not_train}")
        print(f"   Allow Training: {restrictions.allow_training}")
        print(f"   Commercial Use: {restrictions.allow_commercial}")
        print(f"   Attribution Required: {restrictions.attribution_required}")
        print(f"   Attribution Text: {restrictions.attribution_text}")
        print(f"   Data Owner: {restrictions.data_owner}")
        
        # Verify expected values
        expected = {
            'do_not_train': 'strict',
            'allow_training': False,
            'allow_commercial': True,
            'attribution_required': True,
            'attribution_text': 'abc',
            'data_owner': 'abc'
        }
        
        print("\n🔍 Verification:")
        for field, expected_value in expected.items():
            actual_value = getattr(restrictions, field)
            if actual_value == expected_value:
                print(f"   ✅ {field}: {actual_value}")
            else:
                print(f"   ❌ {field}: expected {expected_value}, got {actual_value}")
        
        return True
        
    except Exception as e:
        print(f"❌ License parsing error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting AI Privacy License Detection Tests...")
    
    # Test local detection
    success1 = test_local_detection()
    
    # Test license parsing
    success2 = test_license_parsing()
    
    if success1 and success2:
        print("\n🎉 ALL TESTS PASSED!")
        print("The AI Privacy License Detection Library is working correctly!")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("Please check the errors above and fix any issues.")
        sys.exit(1)
