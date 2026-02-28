#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Unit tests for JSON-LD license extraction
Tests the structured data parsing without network calls
"""

import unittest
from ai_privacy_license_detector import AIPrivacyLicenseDetector

class TestJsonLd(unittest.TestCase):
    
    def setUp(self):
        self.detector = AIPrivacyLicenseDetector()
    
    def test_simple_license_url(self):
        """Test extraction of simple license URL from JSON-LD"""
        data = {
            "license": "https://example.com/AiPrivacyLicense-1.0"
        }
        result = self.detector._find_license_in_json_ld(data)
        self.assertEqual(result, "https://example.com/AiPrivacyLicense-1.0")
    
    def test_nested_license_url(self):
        """Test extraction of nested license URL"""
        data = {
            "dataset": {
                "license": "https://example.com/AiPrivacyLicense-1.0"
            }
        }
        result = self.detector._find_license_in_json_ld(data)
        self.assertEqual(result, "https://example.com/AiPrivacyLicense-1.0")
    
    def test_array_of_objects(self):
        """Test extraction from array of objects"""
        data = [
            {"name": "Dataset 1", "license": "https://example.com/AiPrivacyLicense-1.0"},
            {"name": "Dataset 2", "license": "https://other.com/license"}
        ]
        result = self.detector._find_license_in_json_ld(data)
        self.assertEqual(result, "https://example.com/AiPrivacyLicense-1.0")
    
    def test_multiple_license_fields(self):
        """Test extraction when multiple license fields exist"""
        data = {
            "license": "https://other.com/license",
            "aiPrivacyLicense": "https://example.com/AiPrivacyLicense-1.0"
        }
        result = self.detector._find_license_in_json_ld(data)
        # Should find the first one with AiPrivacyLicense marker
        self.assertEqual(result, "https://example.com/AiPrivacyLicense-1.0")
    
    def test_dict_license_with_id(self):
        """Test extraction from dict license with @id field"""
        data = {
            "license": {
                "@id": "https://example.com/AiPrivacyLicense-1.0",
                "name": "AI Privacy License"
            }
        }
        result = self.detector._find_license_in_json_ld(data)
        self.assertEqual(result, "https://example.com/AiPrivacyLicense-1.0")
    
    def test_dict_license_with_url(self):
        """Test extraction from dict license with url field"""
        data = {
            "license": {
                "url": "https://example.com/AiPrivacyLicense-1.0",
                "type": "AI Privacy License"
            }
        }
        result = self.detector._find_license_in_json_ld(data)
        self.assertEqual(result, "https://example.com/AiPrivacyLicense-1.0")
    
    def test_dict_license_without_marker(self):
        """Test that dict license without marker is ignored"""
        data = {
            "license": {
                "@id": "https://example.com/other-license",
                "name": "Other License"
            }
        }
        result = self.detector._find_license_in_json_ld(data)
        self.assertIsNone(result)
    
    def test_string_input(self):
        """Test handling of string input"""
        data = "https://example.com/AiPrivacyLicense-1.0"
        result = self.detector._find_license_in_json_ld(data)
        self.assertEqual(result, "https://example.com/AiPrivacyLicense-1.0")
    
    def test_no_license_found(self):
        """Test when no license is found"""
        data = {
            "name": "Dataset",
            "description": "No license specified"
        }
        result = self.detector._find_license_in_json_ld(data)
        self.assertIsNone(result)
    
    def test_complex_nested_structure(self):
        """Test extraction from complex nested structure"""
        data = {
            "graph": [
                {
                    "type": "Dataset",
                    "distribution": [
                        {
                            "type": "DataDownload",
                            "license": "https://example.com/AiPrivacyLicense-1.0"
                        }
                    ]
                }
            ]
        }
        result = self.detector._find_license_in_json_ld(data)
        self.assertEqual(result, "https://example.com/AiPrivacyLicense-1.0")
    
    def test_malformed_data(self):
        """Test handling of malformed data"""
        data = None
        result = self.detector._find_license_in_json_ld(data)
        self.assertIsNone(result)
        
        data = 123
        result = self.detector._find_license_in_json_ld(data)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
