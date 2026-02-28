# Security

This library is designed with security in mind, particularly protecting against Server-Side Request Forgery (SSRF) attacks.

## Security Features

### URL Sanitization
- **Scheme restrictions**: Only `http://` and `https://` URLs are allowed
- **Credential blocking**: URLs with embedded credentials (`user:pass@host`) are rejected
- **Port restrictions**: Only standard ports 80 (HTTP) and 443 (HTTPS) are allowed

### IP Address Protection
- **Optional DNS check**: When `enable_dns_check=True` (default), hostnames are resolved to detect private IPs; when disabled, only literal IPs and localhost are checked
- **Private IP blocking**: Rejects localhost, private ranges (192.168.x.x, 10.x.x.x, 172.16-31.x.x)
- **Reserved IP blocking**: Blocks loopback, link-local, multicast, and reserved IP ranges
- **Literal IP detection**: Automatically detects and validates IP address literals

### Content Safety
- **Streamed reads**: All content is streamed with byte limits (max 128KB)
- **Content-type guards**: Only processes text, JSON, XML, YAML, and JavaScript content
- **Resource cleanup**: Proper socket cleanup to prevent connection leaks

### Network Security
- **Redirect limits**: Maximum of 5 redirects to prevent infinite loops
- **Timeout protection**: Configurable timeouts for all network requests
- **Retry limits**: Exponential backoff with maximum retry limits

## Reporting Security Issues

If you discover a security vulnerability, please report it privately to [contact@aiprivacylicense.com](mailto:contact@aiprivacylicense.com) before disclosing it publicly.

## Security Considerations

- This library only fetches metadata endpoints and declared license files
- It does not crawl page content or ignore robots.txt directives
- URL scheme, credentials, and port checks are always local; hostname resolution is optional for stronger SSRF protection
- The library is designed for detection only, not for making policy decisions
