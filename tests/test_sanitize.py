#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Unit tests for URL sanitization
Tests the security features without network calls
"""

import unittest
from ai_privacy_license_detector import AIPrivacyLicenseDetector

class TestSanitize(unittest.TestCase):
    
    def setUp(self):
        self.detector = AIPrivacyLicenseDetector()
    
    def test_valid_http_urls(self):
        """Test that valid HTTP URLs pass through (DNS check disabled to avoid resolution of hostnames)"""
        # Use detector with enable_dns_check=False so hostnames like sub.example.com
        # are not rejected when DNS fails or resolves to a private IP in test env
        detector = AIPrivacyLicenseDetector(enable_dns_check=False)
        valid_urls = [
            "http://example.com",
            "https://example.com",
            "http://sub.example.com/path"
            # Removed: "https://example.com:8080/path?param=value#fragment" - non-standard port
        ]
        
        for url in valid_urls:
            result = detector._sanitize_url(url)
            self.assertEqual(result, url, f"Failed to sanitize: {url}")
    
    def test_invalid_schemes_rejected(self):
        """Test that invalid schemes are rejected"""
        invalid_urls = [
            "file:///etc/passwd",
            "ftp://example.com",
            "javascript:alert('xss')",
            "data:text/html,<script>alert('xss')</script>",
            "mailto:user@example.com",
            "tel:+1234567890"
        ]
        
        for url in invalid_urls:
            result = self.detector._sanitize_url(url)
            self.assertIsNone(result, f"Should reject: {url}")
    
    def test_urls_with_credentials_rejected(self):
        """Test that URLs with embedded credentials are rejected"""
        credential_urls = [
            "http://user:pass@example.com",
            "https://admin:secret@example.com/path",
            "http://username:password@sub.example.com:8080"
        ]
        
        for url in credential_urls:
            result = self.detector._sanitize_url(url)
            self.assertIsNone(result, f"Should reject credentials in: {url}")
    
    def test_private_ips_rejected(self):
        """Test that private IP ranges are rejected"""
        private_ips = [
            "http://localhost",
            "http://127.0.0.1",
            "http://192.168.1.1",
            "http://10.0.0.1",
            "http://172.16.0.1",
            "http://0.0.0.0",
            "http://169.254.1.1"  # link-local
        ]
        
        for url in private_ips:
            result = self.detector._sanitize_url(url)
            self.assertIsNone(result, f"Should reject private IP: {url}")
    
    def test_odd_ports_rejected(self):
        """Test that non-standard ports are rejected"""
        odd_ports = [
            "http://example.com:8080",
            "https://example.com:3000",
            "http://example.com:22",
            "https://example.com:5432"
        ]
        
        for url in odd_ports:
            result = self.detector._sanitize_url(url)
            self.assertIsNone(result, f"Should reject odd port: {url}")
    
    def test_standard_ports_allowed(self):
        """Test that standard ports are allowed"""
        standard_ports = [
            "http://example.com:80",
            "https://example.com:443",
            "http://example.com",  # default port
            "https://example.com"  # default port
        ]
        
        for url in standard_ports:
            result = self.detector._sanitize_url(url)
            self.assertIsNotNone(result, f"Should allow standard port: {url}")
    
    def test_malformed_urls_rejected(self):
        """Test that malformed URLs are rejected"""
        malformed_urls = [
            "not-a-url",
            "http://",
            "https://",
            "://example.com",
            "example.com",
            ""
        ]
        
        for url in malformed_urls:
            result = self.detector._sanitize_url(url)
            self.assertIsNone(result, f"Should reject malformed: {url}")
    
    def test_base_url_normalization(self):
        """Test base URL normalization"""
        test_cases = [
            ("http://example.com", "http://example.com/"),
            ("https://example.com/path", "https://example.com/path"),
            ("https://example.com/path/", "https://example.com/path/"),
            ("http://sub.example.com:8080", "http://sub.example.com:8080/"),
        ]
        
        for input_url, expected in test_cases:
            result = self.detector._normalize_base(input_url)
            self.assertEqual(result, expected, f"Failed to normalize: {input_url}")
    
    def test_invalid_base_urls_rejected(self):
        """Test that invalid base URLs are rejected"""
        invalid_base_urls = [
            "file:///etc/passwd",
            "ftp://example.com",
            "javascript:alert('xss')",
            "not-a-url",
            "",
            "example.com"
        ]
        
        for url in invalid_base_urls:
            result = self.detector._normalize_base(url)
            self.assertIsNone(result, f"Should reject invalid base: {url}")
    
    def test_edge_case_urls(self):
        """Test edge case URL handling"""
        edge_cases = [
            ("http://example.com", "http://example.com/"),
            ("https://example.com/", "https://example.com/"),
            ("http://example.com//", "http://example.com//"),
            ("https://example.com/path//", "https://example.com/path//"),
        ]
        
        for input_url, expected in edge_cases:
            result = self.detector._normalize_base(input_url)
            self.assertEqual(result, expected, f"Edge case failed: {input_url}")

if __name__ == '__main__':
    unittest.main()
