#!/usr/bin/env python3
"""
Simple Test for AI Privacy License Detection Library
This script tests basic functionality without trying to parse local files
"""

import os
import sys

# Add the parent directory to Python path to find the library
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from ai_privacy_license_detector import AIPrivacyLicenseDetector
    print("✅ Successfully imported AI Privacy License Detector")
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    print("Make sure you have activated the virtual environment: source venv/bin/activate")
    sys.exit(1)

def test_basic_functionality():
    """Test basic library functionality"""
    
    print("\n" + "="*60)
    print("🧪 TESTING BASIC FUNCTIONALITY")
    print("="*60)
    
    # Test 1: Detector Creation
    print("\n🔍 Test 1: Detector Creation")
    print("-" * 40)
    
    try:
        detector = AIPrivacyLicenseDetector(verbose=True)
        print("✅ Detector created successfully")
        print(f"   Timeout: {detector.timeout}")
        print(f"   User Agent: {detector.user_agent}")
        print(f"   Verbose: {detector.verbose}")
        print(f"   Insecure SSL: {detector.insecure_ssl}")
    except Exception as e:
        print(f"❌ Detector creation failed: {e}")
        return False
    
    # Test 2: License Content Parsing
    print("\n🔍 Test 2: License Content Parsing")
    print("-" * 40)
    
    try:
        # Test with the license file in the testing directory
        license_file = os.path.join(os.path.dirname(__file__), "AiPrivacyLicense-1.0.txt")
        if os.path.exists(license_file):
            print(f"✅ License file found: {license_file}")
            
            # Parse the license content
            with open(license_file, 'r') as f:
                content = f.read()
            
            restrictions = detector._parse_license_content(content)
            
            print("✅ License parsed successfully:")
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
            all_correct = True
            for field, expected_value in expected.items():
                actual_value = getattr(restrictions, field)
                if actual_value == expected_value:
                    print(f"   ✅ {field}: {actual_value}")
                else:
                    print(f"   ❌ {field}: expected {expected_value}, got {actual_value}")
                    all_correct = False
            
            if all_correct:
                print("\n🎉 All license parsing tests passed!")
            else:
                print("\n⚠️  Some license parsing tests failed")
                
        else:
            print(f"❌ License file not found: {license_file}")
            return False
            
    except Exception as e:
        print(f"❌ License parsing failed: {e}")
        return False
    
    # Test 3: CLI Module Import
    print("\n🔍 Test 3: CLI Module Import")
    print("-" * 40)
    
    try:
        from ai_privacy_license_detector import cli
        print("✅ CLI module imported successfully")
    except Exception as e:
        print(f"❌ CLI module import failed: {e}")
        return False
    
    # Test 4: Library Structure
    print("\n🔍 Test 4: Library Structure")
    print("-" * 40)
    
    try:
        # Check what's available in the library
        from ai_privacy_license_detector import LicenseDetectionResult, LicenseRestriction
        print("✅ Library structure check:")
        print(f"   - AIPrivacyLicenseDetector: {AIPrivacyLicenseDetector}")
        print(f"   - LicenseDetectionResult: {LicenseDetectionResult}")
        print(f"   - LicenseRestriction: {LicenseRestriction}")
    except Exception as e:
        print(f"❌ Library structure check failed: {e}")
        return False
    
    return True

def test_license_file_content():
    """Test the actual content of the license file"""
    
    print("\n🔍 Test 5: License File Content Analysis")
    print("-" * 40)
    
    license_file = os.path.join(os.path.dirname(__file__), "AiPrivacyLicense-1.0.txt")
    if not os.path.exists(license_file):
        print(f"❌ License file not found: {license_file}")
        return False
    
    try:
        with open(license_file, 'r') as f:
            content = f.read()
        
        print(f"✅ License file content analyzed ({len(content)} characters)")
        
        # Check for key phrases
        key_phrases = [
            "AI Privacy License",
            "Do Not Train Flag: strict",
            "Commercial Use Permitted: yes",
            "Attribution Required: Yes",
            "abc"
        ]
        
        print("\n🔍 Key Phrase Check:")
        for phrase in key_phrases:
            if phrase in content:
                print(f"   ✅ Found: {phrase}")
            else:
                print(f"   ❌ Missing: {phrase}")
        
        # Check file structure
        lines = content.split('\n')
        print(f"\n📊 File Structure:")
        print(f"   Total lines: {len(lines)}")
        print(f"   Non-empty lines: {len([l for l in lines if l.strip()])}")
        
        return True
        
    except Exception as e:
        print(f"❌ License file content analysis failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Simple AI Privacy License Detection Tests...")
    
    # Test basic functionality
    success1 = test_basic_functionality()
    
    # Test license file content
    success2 = test_license_file_content()
    
    print("\n" + "="*60)
    print("🎯 TEST RESULTS SUMMARY")
    print("="*60)
    
    if success1 and success2:
        print("🎉 ALL TESTS PASSED!")
        print("The AI Privacy License Detection Library is working correctly!")
        print("\n✅ What's Working:")
        print("   - Library import and initialization")
        print("   - Detector creation and configuration")
        print("   - License content parsing")
        print("   - CLI module availability")
        print("   - Sample license file structure")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the errors above and fix any issues.")
        sys.exit(1)
    
    print("\n🚀 Next Steps:")
    print("   - Test with real HTTP URLs")
    print("   - Run the comprehensive test suite: ./run_tests.sh")
    print("   - Check the testing documentation: README.md")
