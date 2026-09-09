import tldextract

# Trusted domains that bypass high risk scores
WHITELIST_DOMAINS = {
    'google.com',
    'github.com',
    'microsoft.com',
    'stackoverflow.com',
    'openai.com',
    'amazon.com',
    'paypal.com',
    'apple.com',
    'netflix.com',
    'linkedin.com'
}

# Keywords frequently targeted for brand spoofing / phishing
SUSPICIOUS_KEYWORDS = [
    'paypal', 'login', 'verify', 'bank', 'secure',
    'update', 'account', 'signin', 'amazon', 'netflix',
    'microsoft', 'google', 'apple', 'support', 'wallet'
]

def check_whitelist(url: str) -> bool:
    """Checks if the URL's registered domain is in the trusted whitelist."""
    try:
        ext = tldextract.extract(url)
        registered_domain = f"{ext.domain}.{ext.suffix}".lower()
        return registered_domain in WHITELIST_DOMAINS
    except Exception:
        return False

def detect_brand_spoofing(url: str) -> bool:
    """Checks if unverified domain contains targeted brand/security keywords."""
    if check_whitelist(url):
        return False
    
    url_lower = url.lower()
    return any(keyword in url_lower for keyword in SUSPICIOUS_KEYWORDS)

def apply_heuristics(url: str, base_risk_score: int) -> dict:
    """
    Applies Whitelist and Brand Spoofing rules to adjust the base risk score.
    Returns dictionary with adjusted score, whitelisted status, and spoof flag.
    """
    is_whitelisted = check_whitelist(url)
    if is_whitelisted:
        return {
            "risk_score": 0,
            "is_whitelisted": True,
            "is_brand_spoof": False,
            "verdict": "SAFE (Whitelisted)"
        }
    
    is_brand_spoof = detect_brand_spoofing(url)
    final_score = base_risk_score
    
    if is_brand_spoof:
        # Boost risk score if brand keywords are detected on unverified domain
        final_score = int(final_score * 1.4)
        if final_score < 65:
            final_score = 65
    
    final_score = min(max(final_score, 0), 100)
    
    if final_score >= 70:
        verdict = "HIGH RISK"
    elif final_score >= 40:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"
        
    return {
        "risk_score": final_score,
        "is_whitelisted": False,
        "is_brand_spoof": is_brand_spoof,
        "verdict": verdict
    }
