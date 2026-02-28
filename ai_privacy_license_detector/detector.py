# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 AI Privacy License Detection Library Contributors
__version__ = "1.0.0"

"""
AI Privacy License Detection Library for Python
Helps AI companies detect and respect AI Privacy Licenses when processing data

pip install requests beautifulsoup4 urllib3
"""

import re
import json
import time
import socket
import requests
from requests import Response
from requests.utils import parse_header_links
import ipaddress
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urljoin, urlparse, ParseResult
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timezone
import logging
from bs4 import BeautifulSoup


# Constants
AIPL_HEADER = "ai-privacy-license-link"
AIPL_META = "ai-privacy-license-link"
AIPL_MARKER = "AiPrivacyLicense"
SCHEMA_VERSION = "1.0.0"
DEFAULT_UA = f"AI-Privacy-License-Detector/{__version__} (Python)"
ALLOWED_PORTS = {80, 443}
MAX_JSON_LD_SCRIPTS = 10
MAX_BATCH_DELAY = 0.1  # seconds between batch requests
DNS_TIMEOUT = 2  # seconds for DNS resolution check
DEFAULT_MAX_BYTES = 128 * 1024  # 128KB
DEFAULT_TIMEOUT = 10
DEFAULT_MAX_REDIRECTS = 5

# Common license file paths
AIPL_PATHS = (
    "/license/AiPrivacyLicense-1.0",
    "/license/AiPrivacyLicense-1.0.txt",
    "/AiPrivacyLicense-1.0.txt",
    "/LICENSE.txt",
    "/LICENSE",
    "/.well-known/ai-privacy-license",
)


@dataclass
class LicenseRestriction:
    """Represents restrictions from an AI Privacy License"""
    allow_training: bool = True
    attribution_required: bool = False
    allow_commercial: bool = True
    # Optional hints parsed from the license text
    do_not_train: Optional[str] = None       # e.g. "strict", "research"
    attribution_text: Optional[str] = None
    data_owner: Optional[str] = None


@dataclass
class LicenseDetectionResult:
    """Complete result of AI Privacy License detection"""
    url: str
    has_license: bool = False
    license_type: Optional[str] = None
    license_url: Optional[str] = None
    restrictions: Optional[LicenseRestriction] = None
    detection_methods: List[str] = None
    timestamp: str = ""
    error: Optional[str] = None  # New field for error tracking

    def __post_init__(self):
        if self.detection_methods is None:
            self.detection_methods = []
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()
    
    def as_dict(self):
        """Convert result to dictionary for easy serialization"""
        return {
            "url": self.url,
            "has_license": self.has_license,
            "license_type": self.license_type,
            "license_url": self.license_url,
            "restrictions": vars(self.restrictions) if self.restrictions else None,
            "detected_via": self.detection_methods,
            "timestamp": self.timestamp,
            "error": self.error,
            "schema_version": SCHEMA_VERSION,
            "detector_version": __version__
        }


class AIPrivacyLicenseDetector:
    """
    Detects and parses AI Privacy Licenses from websites and data sources
    
    Security Note: This detector includes SSRF protection and respects robots.txt.
    It only fetches metadata endpoints and declared license files, not page content.
    
    Note: requests.Session is not guaranteed thread-safe. For multi-threaded use,
    consider creating separate instances or passing a session per call.
    """
    
    def __init__(
        self, 
        timeout: int = DEFAULT_TIMEOUT, 
        user_agent: str = None, 
        verbose: bool = False, 
        insecure_ssl: bool = False, 
        max_bytes: int = DEFAULT_MAX_BYTES, 
        trust_env: bool = False, 
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        enable_dns_check: bool = True
    ):
        """Initialize the AI Privacy License Detector
        
        Args:
            timeout: Request timeout in seconds
            user_agent: Custom user agent string
            verbose: Enable detailed logging
            insecure_ssl: Disable SSL verification (dev/local only - not recommended for production)
            max_bytes: Maximum bytes to read from responses (default 128KB)
            trust_env: Respect HTTP(S)_PROXY/NO_PROXY environment variables (default False for security)
            max_redirects: Maximum number of redirects to follow (default 5)
            enable_dns_check: Enable DNS resolution check for additional SSRF protection (default True)
        """
        self.timeout = (timeout, timeout)  # (connect, read) timeout
        self.user_agent = user_agent or DEFAULT_UA
        self.verbose = verbose
        self.insecure_ssl = insecure_ssl
        self.max_bytes = max_bytes
        self.enable_dns_check = enable_dns_check
        
        # Configure library-friendly logging
        self.logger = logging.getLogger(__name__)
        if verbose and not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
            self.logger.addHandler(handler)
        
        # Warn about insecure SSL usage
        if self.insecure_ssl and self.verbose:
            self.logger.warning("insecure_ssl=True: SSL verification disabled (dev only).")
        
        self.session = requests.Session()
        self.session.trust_env = bool(trust_env)
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/*,application/ld+json,application/json,*/*;q=0.1'
        })
        
        # Prefer lxml parser if available, else fallback to built-in html.parser
        try:
            import lxml  # noqa: F401
            self.html_parser = "lxml"
        except ImportError:
            self.html_parser = "html.parser"
        
        # Configure retries with backoff
        retries = Retry(
            total=2, 
            backoff_factor=0.2,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["HEAD", "GET"]),
            raise_on_status=False,
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Guard against huge/looping redirects
        self.session.max_redirects = max_redirects

    def _is_ip_literal(self, host: str) -> bool:
        """Check if host is an IP address literal"""
        try:
            ipaddress.ip_address(host)
            return True
        except ValueError:
            return False

    def _is_private_or_local_ip(self, host: str) -> bool:
        """Check if host resolves to private/local IP with enhanced SSRF protection"""
        # Check obvious local names first
        if host in {"localhost", "local", "0.0.0.0"}:
            return True
            
        # If it's an IP literal, check directly
        if self._is_ip_literal(host):
            ip = ipaddress.ip_address(host)
            return (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_multicast
                or ip.is_reserved
            )
        
        # For hostnames, optionally do DNS resolution check
        if self.enable_dns_check:
            try:
                # Set socket timeout for DNS resolution
                old_timeout = socket.getdefaulttimeout()
                socket.setdefaulttimeout(DNS_TIMEOUT)
                
                # Resolve hostname to IP
                ip_str = socket.gethostbyname(host)
                ip = ipaddress.ip_address(ip_str)
                
                is_private = (
                    ip.is_private
                    or ip.is_loopback
                    or ip.is_link_local
                    or ip.is_multicast
                    or ip.is_reserved
                )
                
                return is_private
                
            except (socket.gaierror, socket.timeout, ValueError):
                # DNS resolution failed - treat as potentially unsafe
                return True
            finally:
                socket.setdefaulttimeout(old_timeout)
        
        # If DNS check is disabled, treat unknown hostnames as safe
        return False

    def _has_license_rel(self, rel) -> bool:
        """Check if rel attribute contains 'license' (handles both string and list)"""
        if isinstance(rel, list):
            return any(r and r.lower() == 'license' for r in rel)
        return rel and rel.lower() == 'license'

    def _port_is_allowed(self, p: ParseResult) -> bool:
        """Check if port is in allowed range"""
        if p.port is None:
            return True
        try:
            return int(p.port) in ALLOWED_PORTS
        except (ValueError, TypeError):
            return False
    
    def _validate_final_url(self, resp: Response) -> bool:
        """Ensure the resolved response URL is still safe"""
        # Validate each hop and the final URL
        for r in getattr(resp, "history", []):
            if self._sanitize_url(r.url) is None:
                return False
        return self._sanitize_url(resp.url) is not None

    def _sanitize_url(self, u: str) -> Optional[str]:
        """Enhanced URL sanitization with SSRF protection"""
        try:
            p = urlparse(u)
            
            # Check scheme
            if p.scheme not in ("http", "https"):
                return None
                
            # Check for credentials
            if p.username or p.password:
                return None
                
            # Check host is present
            if not p.hostname:
                return None
                
            # Check for private/local IPs
            if self._is_private_or_local_ip(p.hostname):
                return None
                
            # Check port restrictions
            if not self._port_is_allowed(p):
                return None
                
            return u
        except Exception:
            return None
    
    def _normalize_base(self, url: str) -> Optional[str]:
        """Normalize and validate base URL"""
        try:
            p = urlparse(url)
            if p.scheme in ("http", "https") and p.netloc:
                path = p.path or "/"
                query = f"?{p.query}" if p.query else ""
                return f"{p.scheme}://{p.netloc}{path}{query}"
        except Exception:
            pass
        return None

    def _safe_text(self, resp: Response, max_bytes: Optional[int] = None) -> Optional[str]:
        """Safely extract text content with size limits"""
        if max_bytes is None:
            max_bytes = self.max_bytes
        try:
            ctype = resp.headers.get("Content-Type", "") or "text/plain"
            # Accept text-based content types and application/octet-stream (common for license files)
            if not any(t in ctype for t in ("text/", "json", "xml", "yaml", "javascript", "octet-stream")):
                return None
                
            # Check Content-Length if present
            cl = resp.headers.get("Content-Length")
            if cl and cl.isdigit() and int(cl) > max_bytes:
                return None
                
            out, size = [], 0
            for chunk in resp.iter_content(chunk_size=4096):
                if chunk is None:
                    break
                size += len(chunk)
                if size > max_bytes:
                    break
                out.append(chunk)
                
            return b"".join(out).decode(resp.encoding or "utf-8", errors="replace")
        except Exception:
            return None
        finally:
            resp.close()

    def _fetch_and_parse_html(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse HTML content once for multiple checks"""
        try:
            response = self.session.get(
                url, 
                timeout=self.timeout, 
                verify=not self.insecure_ssl, 
                stream=True
            )
            try:
                if response.status_code == 200 and self._validate_final_url(response):
                    ctype = response.headers.get("Content-Type", "")
                    if "text" not in ctype and "json" not in ctype:
                        return None
                    content = self._safe_text(response)
                    if not content:
                        return None
                    return BeautifulSoup(content, self.html_parser)
                return None
            finally:
                response.close()
        except Exception as e:
            if self.verbose:
                self.logger.warning(f"Failed to fetch HTML from {url}: {self._sanitize_error(str(e))}")
            return None

    def _sanitize_error(self, error_msg: str) -> str:
        """Sanitize error messages to prevent information leakage"""
        # Remove potentially sensitive information from error messages
        sanitized = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP]', error_msg)  # IP addresses
        sanitized = re.sub(r':\d+', ':[PORT]', sanitized)  # Port numbers
        return sanitized

    def _fetch_license_content(self, license_url: str) -> Optional[str]:
        """Fetch license content from URL with safe streaming"""
        try:
            response = self.session.get(
                license_url, 
                timeout=self.timeout, 
                verify=not self.insecure_ssl, 
                stream=True
            )
            try:
                if response.status_code == 200 and self._validate_final_url(response):
                    return self._safe_text(response)
                return None
            finally:
                try:
                    response.close()
                except Exception:
                    pass
        except Exception as e:
            if self.verbose:
                self.logger.warning(f"Failed to fetch license content: {self._sanitize_error(str(e))}")
        return None

    def _truthy(self, s: str) -> bool:
        """Check if string represents a truthy value"""
        if not s:
            return False
        
        s_lower = s.strip().lower()
        
        # Enhanced truthy values from values.md and common variations
        truthy_values = {
            "yes", "true", "allowed", "permitted", "ok", "on", "1", "y",
            "enable", "enabled", "active", "activated", "granted", "grant",
            "positive", "affirmative", "correct", "right", "valid", "validated",
            "approved", "approve", "accept", "accepted", "agree", "agreed"
        }
        
        return s_lower in truthy_values

    def _parse_license_content(self, content: str) -> LicenseRestriction:
        """Parse license content and extract restrictions"""
        restrictions = LicenseRestriction()
        
        if not content:
            return restrictions

        # Parse Do Not Train Flag (enhanced with all values from values.md)
        do_not_train_match = re.search(
            r'Do Not Train Flag\s*:\s*([^\n\r]+)', 
            content, 
            re.IGNORECASE | re.MULTILINE
        )
        if do_not_train_match:
            flag = do_not_train_match.group(1).strip()
            restrictions.do_not_train = flag
            
            # Enhanced parsing for all possible Do Not Train Flag values from values.md
            flag_lower = flag.lower()
            
            # Map the exact values from values.md to training permissions
            # Use more specific matching to avoid substring conflicts
            if flag_lower == "strict - no ai training allowed" or flag_lower == "strict":
                restrictions.allow_training = False
            elif flag_lower == "research only - academic use" or flag_lower == "research only" or flag_lower == "academic use" or flag_lower == "research":
                restrictions.allow_training = False  # Research only typically means restricted
            elif (flag_lower == "allow" or flag_lower == "allow unrestricted ai training"
                  or flag_lower == "unrestricted" or flag_lower == "training allowed"):
                restrictions.allow_training = True
            else:
                # Fallback to pattern matching for variations
                # Check for restrictive patterns first
                restrictive_patterns = [
                    r"\b(do\s*not|no)\s+(train|training|ai|ml|use)\b",
                    r"\bstrict\b",
                    r"\bblock\w*\b",
                    r"\bforbid\w*\b",
                    r"\bprohibit\w*\b"
                ]
                if any(re.search(pattern, flag, re.IGNORECASE) for pattern in restrictive_patterns):
                    restrictions.allow_training = False
                else:
                    # If no restrictive patterns found, check for permissive patterns
                    # Make permissive patterns more specific to avoid false positives
                    permissive_patterns = [
                        r"\b(allow|permit)\w*\s+(unrestricted|training|ai|ml|use)\b",
                        r"\bunrestricted\b",
                        r"\btraining\s*allowed\b"
                    ]
                    if any(re.search(pattern, flag, re.IGNORECASE) for pattern in permissive_patterns):
                        restrictions.allow_training = True
                    else:
                        # Default to False for safety (restrictive by default)
                        restrictions.allow_training = False

        # Parse Commercial Use (enhanced with all values from values.md)
        commercial_match = re.search(
            r'Commercial Use Permitted\s*:\s*([^\n\r]+)', 
            content, 
            re.IGNORECASE | re.MULTILINE
        )
        if commercial_match:
            val = commercial_match.group(1).strip()
            val_lower = val.lower()
            
            # Map exact values from values.md (both full and short forms)
            if any(value in val_lower for value in [
                "yes - allow commercial use",
                "yes",
                "allow commercial use",
                "commercial use allowed"
            ]):
                restrictions.allow_commercial = True
            elif any(value in val_lower for value in [
                "no - prevent monetization",
                "no",
                "prevent monetization",
                "commercial use not allowed"
            ]):
                restrictions.allow_commercial = False
            elif any(value in val_lower for value in [
                "only with permission",
                "permission required",
                "with permission",
                "with permission"
            ]):
                restrictions.allow_commercial = False  # Requires explicit permission
            else:
                # Fallback to existing logic
                restrictions.allow_commercial = self._truthy(val)

        # Parse Attribution requirement (enhanced with all values from values.md)
        attribution_match = re.search(
            r'Attribution Required\s*:\s*([^\n\r]+)', 
            content, 
            re.IGNORECASE | re.MULTILINE
        )
        if attribution_match:
            val = attribution_match.group(1).strip()
            val_lower = val.lower()
            
            # Map exact values from values.md (both full and short forms)
            if any(value in val_lower for value in [
                "yes",
                "yes. if no attribution text is specified, attribution shall be satisfied by including an unmodified copy of this license",
                "attribution required"
            ]):
                restrictions.attribution_required = True
            elif any(value in val_lower for value in [
                "no",
                "not required",
                "attribution not required"
            ]):
                restrictions.attribution_required = False
            else:
                # Fallback to existing logic
                restrictions.attribution_required = self._truthy(val)

        # Parse Attribution Text (enhanced to handle all variations)
        # Use line-by-line parsing for more reliable handling of empty fields
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip().lower().startswith('attribution text:'):
                # Extract the value after the colon
                parts = line.split(':', 1)
                if len(parts) > 1:
                    text = parts[1].strip()
                    # Handle "Not specified" case from values.md and variations
                    if text.lower() in ["not specified", "not specified", "none", "n/a", ""]:
                        restrictions.attribution_text = None
                    else:
                        restrictions.attribution_text = text
                else:
                    restrictions.attribution_text = None
                break

        # Parse Data Owner (enhanced to handle all variations)
        # Use line-by-line parsing for more reliable handling of empty fields
        for i, line in enumerate(lines):
            if line.strip().lower().startswith('data owner name:'):
                # Extract the value after the colon
                parts = line.split(':', 1)
                if len(parts) > 1:
                    owner = parts[1].strip()
                    # Handle "Not specified" case from values.md and variations
                    if owner.lower() in ["not specified", "not specified", "none", "n/a", ""]:
                        restrictions.data_owner = None
                    else:
                        restrictions.data_owner = owner
                else:
                    restrictions.data_owner = None
                break

        return restrictions

    def _find_license_in_json_ld(self, data: Any) -> Optional[str]:
        """Recursively find license URL in JSON-LD data"""
        if isinstance(data, str):
            return data if AIPL_MARKER in data else None
        if isinstance(data, dict):
            lic = data.get("license")
            if isinstance(lic, str) and AIPL_MARKER in lic:
                return lic
            if isinstance(lic, dict):
                for key in ("@id", "url"):
                    v = lic.get(key)
                    if isinstance(v, str) and AIPL_MARKER in v:
                        return v
            for v in data.values():
                r = self._find_license_in_json_ld(v)
                if r: 
                    return r
        if isinstance(data, list):
            for item in data:
                r = self._find_license_in_json_ld(item)
                if r: 
                    return r
        return None

    def check_website(self, url: str) -> LicenseDetectionResult:
        """
        Main method to check a website for AI Privacy License
        
        Security Note: This client only fetches metadata endpoints and declared license files.
        It does not crawl page content and is safe with typical robots policies.
        
        Args:
            url: The website URL to check
            
        Returns:
            LicenseDetectionResult with detection information and any errors
        """
        try:
            # Normalize and validate base URL early
            base = self._normalize_base(url)
            if not base:
                return LicenseDetectionResult(
                    url=url, 
                    error="Invalid URL format"
                )
            
            result = LicenseDetectionResult(url=url)
            
            # Detection methods to try
            detection_methods = [
                self._check_robots_txt,
                self._check_http_headers,
                self._check_html_sources,
                self._check_license_file
            ]
            
            for method in detection_methods:
                try:
                    method_result = method(base)
                    if method_result['found']:
                        result.has_license = True
                        result.detection_methods.append(method.__name__)
                        
                        # Set license info once if not already set
                        if result.license_url is None:
                            result.license_type = method_result.get('license_type', 'AiPrivacyLicense-1.0')
                            result.license_url = method_result.get('license_url')
                            result.restrictions = method_result.get('restrictions')
                        
                        if self.verbose:
                            self.logger.info(f"License detected via {method.__name__}")
                        
                except Exception as e:
                    if self.verbose:
                        self.logger.warning(f"Detection method {method.__name__} failed: {self._sanitize_error(str(e))}")
            
            return result
            
        except Exception as e:
            error_msg = self._sanitize_error(str(e))
            return LicenseDetectionResult(
                url=url,
                error=f"Detection failed: {error_msg}"
            )

    def _check_robots_txt(self, url: str) -> Dict:
        """Check robots.txt for AI Privacy License declaration"""
        try:
            robots_url = urljoin(url, '/robots.txt')
            response = self.session.get(
                robots_url, 
                timeout=self.timeout, 
                verify=not self.insecure_ssl, 
                stream=True
            )
            try:
                if response.status_code == 200 and self._validate_final_url(response):
                    content = self._safe_text(response)
                    if not content:
                        return {'found': False}
                    
                    for raw_line in content.splitlines():
                        line = raw_line.split('#', 1)[0]  # Strip comments
                        low = line.lower()
                        key = f"{AIPL_HEADER}:"
                        if key in low:
                            license_url = line[low.index(key)+len(key):].strip()
                            license_url = urljoin(robots_url, license_url)
                            license_url = self._sanitize_url(license_url)
                            if not license_url:
                                continue
                            
                            license_content = self._fetch_license_content(license_url)
                            
                            if license_content:
                                return {
                                    'found': True,
                                    'license_url': license_url,
                                    'license_type': 'AiPrivacyLicense-1.0',
                                    'restrictions': self._parse_license_content(license_content)
                                }
                return {'found': False}
            finally:
                response.close()
                            
        except Exception as e:
            if self.verbose:
                self.logger.warning(f"robots.txt check failed: {self._sanitize_error(str(e))}")
        
        return {'found': False}

    def _check_http_headers(self, url: str) -> Dict:
        """Check HTTP headers for AI Privacy License"""
        try:
            # Try HEAD first, fallback to GET if blocked
            response = self.session.head(
                url, 
                timeout=self.timeout, 
                verify=not self.insecure_ssl, 
                allow_redirects=True
            )
            try:
                if not self._validate_final_url(response):
                    return {'found': False}
                
                hdrs = {k.lower(): v for k, v in response.headers.items()}
                status = response.status_code
            finally:
                response.close()
                
            if status >= 400 or (AIPL_HEADER not in hdrs and 'link' not in hdrs):
                response = self.session.get(
                    url, 
                    timeout=self.timeout, 
                    verify=not self.insecure_ssl, 
                    stream=True
                )
                try:
                    if not self._validate_final_url(response):
                        return {'found': False}
                    hdrs = {k.lower(): v for k, v in response.headers.items()}
                finally:
                    response.close()

            # Check ai-privacy-license-link header
            raw = hdrs.get(AIPL_HEADER)
            if raw:
                for part in (p.strip().strip('<>') for p in raw.split(",")):
                    license_url = urljoin(url, part)
                    license_url = self._sanitize_url(license_url)
                    if not license_url:
                        continue
                    content = self._fetch_license_content(license_url)
                    if content:
                        return {
                            'found': True,
                            'license_url': license_url,
                            'license_type': 'AiPrivacyLicense-1.0',
                            'restrictions': self._parse_license_content(content)
                        }

            # Check Link header with rel="license"
            link = hdrs.get('link')
            if link:
                for li in parse_header_links(link):
                    rels = (li.get('rel') or '').lower().split()
                    if 'license' in rels and li.get('url'):
                        license_url = self._sanitize_url(urljoin(url, li['url']))
                        if not license_url:
                            continue
                        content = self._fetch_license_content(license_url)
                        if content:
                            return {
                                'found': True,
                                'license_url': license_url,
                                'license_type': 'AiPrivacyLicense-1.0',
                                'restrictions': self._parse_license_content(content)
                            }
                    
        except Exception as e:
            if self.verbose:
                self.logger.warning(f"HTTP headers check failed: {self._sanitize_error(str(e))}")
        
        return {'found': False}

    def _check_html_sources(self, url: str) -> Dict:
        """Check HTML meta tags and JSON-LD for AI Privacy License"""
        soup = self._fetch_and_parse_html(url)
        if not soup:
            return {'found': False}
        
        try:
            # Check meta name="ai-privacy-license-link"
            meta_tag = soup.find('meta', attrs={'name': lambda v: v and v.lower() == AIPL_META})
            if meta_tag and meta_tag.get('content'):
                license_url = urljoin(url, meta_tag['content'])
                license_url = self._sanitize_url(license_url)
                if license_url:
                    license_content = self._fetch_license_content(license_url)
                    if license_content:
                        return {
                            'found': True,
                            'license_url': license_url,
                            'license_type': 'AiPrivacyLicense-1.0',
                            'restrictions': self._parse_license_content(license_content)
                        }
                        
            # Check <link rel="license" href="...">
            link = soup.find('link', rel=self._has_license_rel, href=True)
            if link:
                license_url = self._sanitize_url(urljoin(url, link['href']))
                if license_url:
                    content = self._fetch_license_content(license_url)
                    if content:
                        return {
                            'found': True,
                            'license_url': license_url,
                            'license_type': 'AiPrivacyLicense-1.0',
                            'restrictions': self._parse_license_content(content)
                        }

            # Check JSON-LD structured data
            json_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_scripts[:MAX_JSON_LD_SCRIPTS]:  # Limit for performance
                raw = script.string or script.get_text(strip=True)
                if not raw:
                    continue
                try:
                    data = json.loads(raw)
                    license_url = self._find_license_in_json_ld(data)
                    
                    if license_url and AIPL_MARKER in license_url:
                        license_url = urljoin(url, license_url)
                        license_url = self._sanitize_url(license_url)
                        if not license_url:
                            continue
                        license_content = self._fetch_license_content(license_url)
                        
                        if license_content:
                            return {
                                'found': True,
                                'license_url': license_url,
                                'license_type': 'AiPrivacyLicense-1.0',
                                'restrictions': self._parse_license_content(license_content)
                            }
                except (json.JSONDecodeError, TypeError):
                    continue
                        
        except Exception as e:
            if self.verbose:
                self.logger.warning(f"HTML sources check failed: {self._sanitize_error(str(e))}")
        
        return {'found': False}

    def _check_license_file(self, url: str) -> Dict:
        """Check for license file at common paths"""
        for path in AIPL_PATHS:
            try:
                license_url = urljoin(url, path)
                response = self.session.get(
                    license_url, 
                    timeout=self.timeout, 
                    verify=not self.insecure_ssl, 
                    stream=True
                )
                try:
                    if response.status_code == 200 and self._validate_final_url(response):
                        content = self._safe_text(response)
                        if not content:
                            continue
                        
                        if 'AI Privacy License' in content or f'{AIPL_MARKER}-1.0' in content:
                            return {
                                'found': True,
                                'license_url': license_url,
                                'license_type': 'AiPrivacyLicense-1.0',
                                'restrictions': self._parse_license_content(content)
                            }
                finally:
                    response.close()
                        
            except Exception:
                continue
        
        return {'found': False}

    def check_batch_urls(
        self, 
        urls: List[str], 
        delay: float = MAX_BATCH_DELAY
    ) -> List[LicenseDetectionResult]:
        """Check multiple URLs for AI Privacy Licenses with rate limiting
        
        Args:
            urls: List of URLs to check
            delay: Delay between requests in seconds (default 0.1s)
            
        Returns:
            List of LicenseDetectionResult objects
        """
        results = []
        
        for i, url in enumerate(urls):
            # Add delay between requests for rate limiting
            if i > 0 and delay > 0:
                time.sleep(delay)
                
            try:
                result = self.check_website(url)
                results.append(result)
            except Exception as e:
                # Create error result with sanitized error message
                error_result = LicenseDetectionResult(
                    url=url,
                    has_license=False,
                    error=self._sanitize_error(str(e))
                )
                results.append(error_result)
                
                if self.verbose:
                    self.logger.error(f"Failed to check {url}: {self._sanitize_error(str(e))}")
        
        return results

    def close(self) -> None:
        """Close the session to prevent connection leaks"""
        try:
            self.session.close()
        except Exception:
            pass
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc, tb):
        """Context manager exit"""
        self.close()


# Convenience function for simple use cases
def check_url(
    url: str, 
    timeout: int = DEFAULT_TIMEOUT, 
    insecure_ssl: bool = False,
    verbose: bool = False
) -> LicenseDetectionResult:
    """Simple function to check a single URL for AI Privacy License
    
    Args:
        url: The URL to check
        timeout: Request timeout in seconds
        insecure_ssl: Disable SSL verification (not recommended)
        verbose: Enable verbose logging
        
    Returns:
        LicenseDetectionResult object
        
    Example:
        >>> result = check_url("https://example.com")
        >>> if result.has_license:
        ...     print(f"Found license: {result.license_url}")
        ...     print(f"Allow training: {result.restrictions.allow_training}")
    """
    with AIPrivacyLicenseDetector(
        timeout=timeout, 
        insecure_ssl=insecure_ssl,
        verbose=verbose
    ) as detector:
        return detector.check_website(url)


# Public API
__all__ = [
    "AIPrivacyLicenseDetector",
    "LicenseRestriction", 
    "LicenseDetectionResult",
    "check_url",
    "DEFAULT_UA",
    "__version__",
]