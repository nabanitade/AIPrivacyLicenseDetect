#!/usr/bin/env python3
"""
AI Privacy License CLI Tool
Detect AI Privacy Licenses on one or more URLs.

Usage:
  ai-license https://example.com
  ai-license -v --require https://site1 https://site2
  cat urls.txt | ai-license - --ndjson

Copyright (c) 2025 AI Privacy License Detection Library Contributors
SPDX-License-Identifier: Apache-2.0
"""

import argparse
import json
import signal
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List, Optional, Tuple
from urllib.parse import urlsplit, urlunsplit

from .detector import AIPrivacyLicenseDetector, __version__ as DETECTOR_VERSION

# Exit codes
EXIT_OK = 0
EXIT_ERROR = 1        # runtime/IO error on at least one URL (or setup)
EXIT_NO_LICENSE = 2   # completed, but at least one URL had no license (when --require)

# CLI Constants
DEFAULT_TIMEOUT = 10.0
DEFAULT_MAX_BYTES = 128 * 1024
DEFAULT_MAX_REDIRECTS = 5
DEFAULT_CONCURRENCY = 1
MAX_CONCURRENCY = 50  # Reasonable upper limit
MIN_TIMEOUT = 0.1
MAX_TIMEOUT = 300.0

# Thread-safe printing lock
print_lock = threading.Lock()


def _iter_urls(arg_urls: List[str]) -> Iterable[str]:
    """Iterator that yields URLs from command line args or stdin"""
    if len(arg_urls) == 1 and arg_urls[0] == "-":
        try:
            for line_num, line in enumerate(sys.stdin, 1):
                line = line.strip()
                if line and not line.startswith('#'):  # Skip comments
                    yield line
                elif line_num > 100000:  # Prevent runaway stdin
                    raise ValueError("Too many input lines (max 100,000)")
        except UnicodeDecodeError as e:
            raise ValueError(f"Invalid UTF-8 in stdin: {e}")
        return
    yield from arg_urls


def _normalize_url(url: str) -> str:
    """Normalize URL for deduplication and validation"""
    if not url or not isinstance(url, str):
        return url
        
    raw = url.strip()
    if not raw:
        return raw
    
    # Handle scheme-less URLs that start with //
    if raw.startswith("//"):
        raw = "https:" + raw
    
    try:
        s = urlsplit(raw)
        
        # Add default scheme if missing (common CLI input)
        if not s.scheme:
            s = urlsplit("https://" + raw)
        
        # Validate scheme
        if s.scheme not in ('http', 'https'):
            return raw  # Return original for error reporting
        
        # Handle IPv6 addresses and hostname normalization
        host = s.hostname or ""
        
        # Skip obviously invalid inputs (no hostname)
        if not host:
            return raw  # return original to keep seen/total honest
        
        # Rebuild netloc preserving IPv6 brackets
        is_ipv6 = ":" in host and not host.startswith("[")
        host_display = f"[{host}]" if is_ipv6 else host
        
        # Drop default ports, preserve non-standard ones
        default_port = 80 if s.scheme == "http" else 443 if s.scheme == "https" else None
        if s.port is None or s.port == default_port:
            netloc = host_display.lower()
        else:
            netloc = f"{host_display.lower()}:{s.port}"
        
        # Strip trailing slash only if path is not the root
        path = s.path[:-1] if (s.path and s.path != "/" and s.path.endswith("/")) else s.path
        
        # Fragments don't affect fetch; normalize by removing them for dedupe
        return urlunsplit((s.scheme, netloc, path or "/", s.query, ""))  # no fragment
        
    except Exception:
        return raw  # Return original on any parsing error


def _safe_print(s: str, *, to_stderr: bool = False, use_lock: bool = True):
    """Thread-safe printing with broken pipe handling"""
    try:
        if use_lock:
            with print_lock:
                (sys.stderr if to_stderr else sys.stdout).write(s + "\n")
                (sys.stderr if to_stderr else sys.stdout).flush()
        else:
            (sys.stderr if to_stderr else sys.stdout).write(s + "\n")
            (sys.stderr if to_stderr else sys.stdout).flush()
    except BrokenPipeError:
        # Graceful handling of broken pipes (e.g., when piping to head)
        sys.exit(EXIT_OK)
    except IOError:
        # Handle other IO errors gracefully
        sys.exit(EXIT_ERROR)


def _dump_json(obj, ndjson: bool, compact: bool, indent: Optional[int], use_lock: bool = True):
    """Output JSON with consistent formatting"""
    try:
        if ndjson or compact:
            output = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
        else:
            output = json.dumps(obj, indent=indent, ensure_ascii=False)
        _safe_print(output, use_lock=use_lock)
    except (TypeError, ValueError) as e:
        # Handle JSON serialization errors
        error_obj = {"error": f"JSON serialization failed: {str(e)}", "url": obj.get("url", "unknown")}
        fallback = json.dumps(error_obj, separators=(",", ":"))
        _safe_print(fallback, to_stderr=True, use_lock=use_lock)


def _validate_args(args) -> Optional[str]:
    """Validate command line arguments"""
    if args.timeout < MIN_TIMEOUT or args.timeout > MAX_TIMEOUT:
        return f"Timeout must be between {MIN_TIMEOUT} and {MAX_TIMEOUT} seconds"
    
    if args.max_bytes < 1024:
        return "max-bytes must be at least 1024"
    
    if args.max_redirects < 0 or args.max_redirects > 20:
        return "max-redirects must be between 0 and 20"
    
    if args.concurrency < 1 or args.concurrency > MAX_CONCURRENCY:
        return f"concurrency must be between 1 and {MAX_CONCURRENCY}"
    
    if args.fail_fast_require and not args.require:
        return "--fail-fast-require requires --require"
    
    return None


def _build_url_index(url_iter) -> Tuple[List[Tuple[int, str]], set]:
    """Build deduplicated URL index"""
    seen = set()
    indexed = []
    
    for i, u in enumerate(url_iter):
        if i > 100000:  # Prevent runaway input
            raise ValueError("Too many URLs (max 100,000)")
            
        nu = _normalize_url(u)
        if nu in seen:
            continue
        seen.add(nu)
        indexed.append((i, nu))
    
    return indexed, seen


def _create_detector(args):
    """Create a detector instance with given args"""
    return AIPrivacyLicenseDetector(
        timeout=args.timeout,
        user_agent=args.user_agent,
        verbose=args.verbose and args.concurrency == 1,  # Avoid log interleaving
        insecure_ssl=args.insecure_ssl,
        max_bytes=args.max_bytes,
        trust_env=args.respect_proxy,
        max_redirects=args.max_redirects,
    )


def _handle_result(result_data, args) -> Tuple[bool, bool]:
    """Handle a single result and return (had_error, had_no_license)"""
    url, payload, error = result_data
    
    if error:
        error_obj = {"url": url, "error": error, "ok": False}
        _dump_json(
            error_obj, 
            args.ndjson, 
            args.compact, 
            None if args.compact or args.ndjson else 2
        )
        return True, False  # had_error=True, had_no_license=False
    else:
        _dump_json(
            payload, 
            args.ndjson, 
            args.compact, 
            None if args.compact or args.ndjson else 2
        )
        has_license = payload.get("has_license", False)
        return False, not has_license  # had_error=False, had_no_license=not has_license


def _process_sequential(indexed_urls, args, detector):
    """Process URLs sequentially"""
    had_error = False
    had_no_license = False
    error_count = 0
    no_license_count = 0
    licensed_count = 0
    processed = 0
    
    for i, normalized_url in indexed_urls:
        try:
            result = detector.check_website(normalized_url)
            payload = result.as_dict()
            
            processed += 1
            
            if payload.get("has_license", False):
                licensed_count += 1
            else:
                no_license_count += 1
                if args.require:
                    had_no_license = True
                    if args.fail_fast_require:
                        break
            
            _dump_json(
                payload, 
                args.ndjson, 
                args.compact, 
                None if args.compact or args.ndjson else 2,
                use_lock=False  # Single-threaded, no need for lock
            )
            
        except KeyboardInterrupt:
            _safe_print("Interrupted by user", to_stderr=True, use_lock=False)
            raise
        except Exception as e:
            processed += 1
            had_error = True
            error_count += 1
            
            error_obj = {"url": normalized_url, "error": str(e), "ok": False}
            _dump_json(
                error_obj, 
                args.ndjson, 
                args.compact, 
                None if args.compact or args.ndjson else 2,
                use_lock=False
            )
            
            if args.fail_fast_error:
                break
    
    return had_error, had_no_license, error_count, no_license_count, licensed_count, processed


def _worker_function(entry, args):
    """Worker function for concurrent processing"""
    i, url = entry
    try:
        with _create_detector(args) as detector:
            result = detector.check_website(url)
            payload = result.as_dict()
        return i, url, payload, None
    except Exception as e:
        return i, url, None, str(e)


def _process_concurrent(indexed_urls, args):
    """Process URLs concurrently"""
    had_error = False
    had_no_license = False
    error_count = 0
    no_license_count = 0
    licensed_count = 0
    processed = 0
    
    results = [None] * len(indexed_urls)
    stop_early = False
    
    max_workers = max(1, min(args.concurrency, len(indexed_urls) or 1))
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(_worker_function, entry, args): entry 
            for entry in indexed_urls
        }
        
        try:
            for future in as_completed(futures):
                i, url, payload, error = future.result()
                
                if error:
                    processed += 1
                    had_error = True
                    error_count += 1
                    
                    error_obj = {"url": url, "error": error, "ok": False}
                    _dump_json(error_obj, args.ndjson, args.compact, 
                             None if args.compact or args.ndjson else 2)
                    
                    if args.fail_fast_error:
                        stop_early = True
                        break
                else:
                    results[i] = (url, payload)
                    
                    # Check for fail-fast on require
                    if (args.require and args.fail_fast_require and 
                        not payload.get("has_license", False)):
                        had_no_license = True
                        stop_early = True
                        break
                        
        except KeyboardInterrupt:
            _safe_print("Interrupted by user", to_stderr=True)
            stop_early = True
            raise
        finally:
            if stop_early:
                # Cancel remaining futures
                for future in futures:
                    future.cancel()
                executor.shutdown(wait=False, cancel_futures=True)
    
    # Process results in original order
    for slot in results:
        if slot is None:
            continue
            
        processed += 1
        url, payload = slot
        
        _dump_json(payload, args.ndjson, args.compact, 
                  None if args.compact or args.ndjson else 2)
        
        if payload.get("has_license", False):
            licensed_count += 1
        else:
            no_license_count += 1
            if args.require:
                had_no_license = True
    
    return had_error, had_no_license, error_count, no_license_count, licensed_count, processed


def main():
    """Main CLI entry point"""
    # Handle signals gracefully
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, OSError):
        # Not available on all platforms
        pass
    
    # Windows Unicode support
    if sys.platform.startswith("win"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    parser = argparse.ArgumentParser(
        description="Check URLs for AI Privacy License compliance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ai-license https://example.com
  ai-license --ndjson https://site1.com https://site2.com
  cat urls.txt | ai-license - --ndjson
  echo "https://example.com" | ai-license - --require --summary
  ai-license --concurrency 5 --timeout 15 https://example.com

Exit codes:
  0: Success - all URLs processed successfully
  1: Error - runtime/network errors occurred  
  2: No license - some URLs lack licenses (when --require is used)

Security Notes:
  - SSRF protection is enabled by default
  - Use --insecure-ssl only for development/testing
  - Respects robots.txt and only fetches metadata endpoints

Rate Limiting:
  - Built-in delays between requests in concurrent mode
  - Use --concurrency to control parallel requests
  - Be respectful to target servers
        """,
    )
    
    # Positional arguments
    parser.add_argument(
        "url", nargs="+",
        help='URL(s) to check. Use "-" to read URLs from stdin (one per line)',
    )
    
    # Output options
    parser.add_argument(
        "--ndjson", action="store_true", 
        help="Output newline-delimited JSON (one object per URL)"
    )
    parser.add_argument(
        "--compact", action="store_true", 
        help="Compact JSON output (no indentation)"
    )
    parser.add_argument(
        "--summary", action="store_true", 
        help="Print summary statistics to stderr"
    )
    
    # Behavior options  
    parser.add_argument(
        "--require", action="store_true", 
        help="Exit with code 2 if any URL lacks a license"
    )
    parser.add_argument(
        "--fail-fast-error", action="store_true", 
        help="Stop processing on first network/runtime error"
    )
    parser.add_argument(
        "--fail-fast-require", action="store_true", 
        help="Stop processing on first missing license (requires --require)"
    )
    
    # Network options
    parser.add_argument(
        "--timeout", type=float, default=DEFAULT_TIMEOUT,
        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})"
    )
    parser.add_argument(
        "--max-redirects", type=int, default=DEFAULT_MAX_REDIRECTS,
        help=f"Maximum redirects to follow (default: {DEFAULT_MAX_REDIRECTS})"
    )
    parser.add_argument(
        "--max-bytes", type=int, default=DEFAULT_MAX_BYTES,
        help=f"Maximum bytes per response (default: {DEFAULT_MAX_BYTES})"
    )
    parser.add_argument(
        "--user-agent", default=None, 
        help="Custom User-Agent string"
    )
    parser.add_argument(
        "--respect-proxy", action="store_true", 
        help="Respect HTTP_PROXY/HTTPS_PROXY environment variables"
    )
    parser.add_argument(
        "--insecure-ssl", action="store_true", 
        help="Disable SSL certificate verification (development only)"
    )
    
    # Performance options
    parser.add_argument(
        "--concurrency", type=int, default=DEFAULT_CONCURRENCY,
        help=f"Number of parallel requests (default: {DEFAULT_CONCURRENCY}, max: {MAX_CONCURRENCY})"
    )
    
    # Debug options
    parser.add_argument(
        "--verbose", "-v", action="store_true", 
        help="Enable verbose logging to stderr"
    )
    
    # Version
    parser.add_argument(
        "--version", action="version", 
        version=f"%(prog)s {DETECTOR_VERSION}"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    validation_error = _validate_args(args)
    if validation_error:
        _safe_print(f"Error: {validation_error}", to_stderr=True, use_lock=False)
        return EXIT_ERROR
    
    # Warn about insecure SSL
    if args.insecure_ssl:
        _safe_print("Warning: SSL verification disabled (development only)", 
                   to_stderr=True, use_lock=False)
    
    # Initialize counters
    had_error = False
    had_no_license = False
    error_count = 0
    no_license_count = 0
    licensed_count = 0
    processed = 0
    
    try:
        # Build URL index with deduplication
        indexed_urls, seen_urls = _build_url_index(_iter_urls(args.url))
        
        if not indexed_urls:
            _safe_print("No URLs to process", to_stderr=True, use_lock=False)
            return EXIT_OK
        
        # Process URLs
        if args.concurrency == 1:
            # Sequential processing
            with _create_detector(args) as detector:
                (had_error, had_no_license, error_count,
                 no_license_count, licensed_count, processed) = _process_sequential(
                    indexed_urls, args, detector
                )
        else:
            # Concurrent processing
            (had_error, had_no_license, error_count,
             no_license_count, licensed_count, processed) = _process_concurrent(
                indexed_urls, args
            )
    
    except KeyboardInterrupt:
        _safe_print("Operation cancelled by user", to_stderr=True, use_lock=False)
        return EXIT_ERROR
    except ValueError as e:
        _safe_print(f"Input error: {e}", to_stderr=True, use_lock=False)
        return EXIT_ERROR
    except Exception as e:
        _safe_print(f"Unexpected error: {e}", to_stderr=True, use_lock=False)
        return EXIT_ERROR
    
    # Print summary if requested
    if args.summary:
        total_unique = len(seen_urls)
        _safe_print(
            f"Summary: unique_inputs={total_unique} processed={processed} "
            f"licensed={licensed_count} no_license={no_license_count} errors={error_count}",
            to_stderr=True, use_lock=False
        )
    
    # Determine exit code
    if had_error:
        return EXIT_ERROR
    if args.require and had_no_license:
        return EXIT_NO_LICENSE
    return EXIT_OK


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(EXIT_ERROR)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(EXIT_ERROR)