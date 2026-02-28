#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Unit tests for HTTP header detection
Tests the header parsing and multi-value support
"""

import unittest
from unittest.mock import Mock, patch
from ai_privacy_license_detector import AIPrivacyLicenseDetector

class TestHeaders(unittest.TestCase):
    
    def setUp(self):
        self.detector = AIPrivacyLicenseDetector()
    
    def test_single_header_value(self):
        """Test detection of single header value"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = 'https://example.com/'
        mock_response.history = []
        mock_response.headers = {
            'ai-privacy-license-link': 'https://example.com/AiPrivacyLicense-1.0'
        }
        
        with patch.object(self.detector, '_validate_final_url', return_value=True):
            with patch.object(self.detector.session, 'head', return_value=mock_response):
                with patch.object(self.detector, '_fetch_license_content', return_value="Do Not Train Flag: allow"):
                    result = self.detector._check_http_headers("https://example.com")
                    self.assertTrue(result['found'])
                    self.assertEqual(result['license_url'], 'https://example.com/AiPrivacyLicense-1.0')
    
    def test_multi_value_header(self):
        """Test detection of multi-value header with comma separation"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = 'https://example.com/'
        mock_response.history = []
        mock_response.headers = {
            'ai-privacy-license-link': 'https://example.com/AiPrivacyLicense-1.0, https://backup.com/license'
        }
        
        with patch.object(self.detector, '_validate_final_url', return_value=True):
            with patch.object(self.detector.session, 'head', return_value=mock_response):
                with patch.object(self.detector, '_fetch_license_content', return_value="Do Not Train Flag: allow"):
                    result = self.detector._check_http_headers("https://example.com")
                    self.assertTrue(result['found'])
                    # Should use first valid license found
                    self.assertEqual(result['license_url'], 'https://example.com/AiPrivacyLicense-1.0')
    
    def test_case_insensitive_header_lookup(self):
        """Test that header lookup is case insensitive"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = 'https://example.com/'
        mock_response.history = []
        mock_response.headers = {
            'AI-PRIVACY-LICENSE-LINK': 'https://example.com/AiPrivacyLicense-1.0'
        }
        
        with patch.object(self.detector, '_validate_final_url', return_value=True):
            with patch.object(self.detector.session, 'head', return_value=mock_response):
                with patch.object(self.detector, '_fetch_license_content', return_value="Do Not Train Flag: allow"):
                    result = self.detector._check_http_headers("https://example.com")
                    self.assertTrue(result['found'])
    
    def test_header_fallback_to_get(self):
        """Test fallback from HEAD to GET when HEAD fails"""
        mock_head_response = Mock()
        mock_head_response.status_code = 405  # Method Not Allowed
        mock_head_response.url = 'https://example.com/'
        mock_head_response.history = []
        mock_head_response.headers = {}
        
        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_get_response.url = 'https://example.com/'
        mock_get_response.history = []
        mock_get_response.headers = {
            'ai-privacy-license-link': 'https://example.com/AiPrivacyLicense-1.0'
        }
        
        def request_side_effect(method, url, **kwargs):
            if method.upper() == 'HEAD':
                return mock_head_response
            return mock_get_response

        def sanitize_pass_https(u):
            if u and (u.startswith("http://") or u.startswith("https://")):
                return u
            return None

        with patch.object(self.detector, '_validate_final_url', return_value=True):
            with patch.object(self.detector, '_sanitize_url', side_effect=sanitize_pass_https):
                with patch.object(self.detector.session, 'request', side_effect=request_side_effect):
                    with patch.object(self.detector, '_fetch_license_content', return_value="Do Not Train Flag: allow"):
                        result = self.detector._check_http_headers("https://example.com")
                        self.assertTrue(result['found'])
    
    def test_no_license_header(self):
        """Test when no license header is present"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        
        with patch.object(self.detector.session, 'head', return_value=mock_response):
            result = self.detector._check_http_headers("https://example.com")
            self.assertFalse(result['found'])
    
    def test_invalid_license_url(self):
        """Test handling of invalid license URLs in header"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {
            'ai-privacy-license-link': 'file:///etc/passwd'  # Invalid scheme
        }
        
        with patch.object(self.detector.session, 'head', return_value=mock_response):
            result = self.detector._check_http_headers("https://example.com")
            self.assertFalse(result['found'])

if __name__ == '__main__':
    unittest.main()
