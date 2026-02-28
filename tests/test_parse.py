#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Unit tests for license content parsing
Tests the core parsing logic without network calls
"""

import unittest
from ai_privacy_license_detector import AIPrivacyLicenseDetector

class TestParse(unittest.TestCase):
    
    def setUp(self):
        self.detector = AIPrivacyLicenseDetector()
    
    def test_strict_deny_parsing(self):
        """Test parsing of strict 'do not train' license"""
        content = """
        Do Not Train Flag: strict
        Commercial Use Permitted: yes
        Attribution Required: no
        """
        restrictions = self.detector._parse_license_content(content)
        
        self.assertEqual(restrictions.do_not_train, "strict")
        self.assertFalse(restrictions.allow_training)
        self.assertTrue(restrictions.allow_commercial)
        self.assertFalse(restrictions.attribution_required)
    
    def test_allow_with_attribution_parsing(self):
        """Test parsing of training allowed with attribution required"""
        content = """
        Do Not Train Flag: allow
        Commercial Use Permitted: yes
        Attribution Required: yes
        Attribution Text: Please cite our dataset
        """
        restrictions = self.detector._parse_license_content(content)
        
        self.assertEqual(restrictions.do_not_train, "allow")
        self.assertTrue(restrictions.allow_training)
        self.assertTrue(restrictions.allow_commercial)
        self.assertTrue(restrictions.attribution_required)
        self.assertEqual(restrictions.attribution_text, "Please cite our dataset")
    
    def test_research_only_parsing(self):
        """Test parsing of research-only license"""
        content = """
        Do Not Train Flag: research
        Commercial Use Permitted: no
        Attribution Required: yes
        Data Owner Name: Research Institute
        """
        restrictions = self.detector._parse_license_content(content)
        
        self.assertEqual(restrictions.do_not_train, "research")
        self.assertFalse(restrictions.allow_training)  # research != allow
        self.assertFalse(restrictions.allow_commercial)
        self.assertTrue(restrictions.attribution_required)
        self.assertEqual(restrictions.data_owner, "Research Institute")
    
    def test_empty_content(self):
        """Test parsing of empty content"""
        restrictions = self.detector._parse_license_content("")
        
        # Should return defaults
        self.assertTrue(restrictions.allow_training)
        self.assertFalse(restrictions.attribution_required)
        self.assertTrue(restrictions.allow_commercial)
        self.assertIsNone(restrictions.do_not_train)
        self.assertIsNone(restrictions.attribution_text)
        self.assertIsNone(restrictions.data_owner)
    
    def test_truthy_values(self):
        """Test various truthy/falsy value formats"""
        content = """
        Commercial Use Permitted: 1
        Attribution Required: Y
        """
        restrictions = self.detector._parse_license_content(content)
        
        self.assertTrue(restrictions.allow_commercial)
        self.assertTrue(restrictions.attribution_required)
    
    def test_falsy_values(self):
        """Test various falsy value formats"""
        content = """
        Commercial Use Permitted: 0
        Attribution Required: N
        """
        restrictions = self.detector._parse_license_content(content)
        
        self.assertFalse(restrictions.allow_commercial)
        self.assertFalse(restrictions.attribution_required)

if __name__ == '__main__':
    unittest.main()
