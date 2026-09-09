import re
import urllib.parse
from datetime import datetime
import tldextract
import pandas as pd

FEATURE_COLUMNS = [
    'url_length',
    'has_at_symbol',
    'has_https',
    'no_of_dots',
    'has_ip',
    'hyphen_count',
    'domain_age_days'
]

def is_ip_address(url: str) -> int:
    """Checks if the host in the URL is a raw IP address."""
    parsed = urllib.parse.urlparse(url if '://' in url else f'http://{url}')
    host = parsed.netloc.split(':')[0]
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    return 1 if re.match(ip_pattern, host) else 0

def get_domain_age_days(url: str, enable_whois: bool = False) -> int:
    """
    Safely calculates domain age in days using WHOIS.
    Defaults to 0 if disabled or if lookup fails/times out.
    """
    if not enable_whois:
        return 0
    
    try:
        import whois
        ext = tldextract.extract(url)
        domain_name = f"{ext.domain}.{ext.suffix}"
        w = whois.whois(domain_name)
        creation_date = w.creation_date
        
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        if creation_date:
            if hasattr(creation_date, 'tzinfo') and creation_date.tzinfo is not None:
                creation_date = creation_date.replace(tzinfo=None)
            age = (datetime.now() - creation_date).days
            return max(age, 0)
        return 0
    except Exception:
        return 0

def extract_features(url: str, enable_whois: bool = False) -> list:
    """
    Extracts a list of 7 feature values from a given URL string.
    Returns: [url_length, has_at_symbol, has_https, no_of_dots, has_ip, hyphen_count, domain_age_days]
    """
    clean_url = url.strip()
    
    url_length = len(clean_url)
    has_at = 1 if '@' in clean_url else 0
    has_https = 1 if clean_url.lower().startswith('https') else 0
    no_of_dots = clean_url.count('.')
    has_ip = is_ip_address(clean_url)
    hyphen_count = clean_url.count('-')
    domain_age = get_domain_age_days(clean_url, enable_whois=enable_whois)
    
    return [
        url_length,
        has_at,
        has_https,
        no_of_dots,
        has_ip,
        hyphen_count,
        domain_age
    ]

def extract_features_df(url: str, enable_whois: bool = False) -> pd.DataFrame:
    """
    Extracts features and returns a single-row Pandas DataFrame matching model feature columns.
    """
    features = extract_features(url, enable_whois=enable_whois)
    return pd.DataFrame([features], columns=FEATURE_COLUMNS)
