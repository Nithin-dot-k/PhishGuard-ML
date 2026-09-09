import pytest
from src.phishguard.feature_extractor import extract_features, extract_features_df, is_ip_address
from src.phishguard.heuristic_engine import check_whitelist, detect_brand_spoofing, apply_heuristics

def test_is_ip_address():
    assert is_ip_address("http://192.168.1.1/login") == 1
    assert is_ip_address("https://google.com") == 0

def test_extract_features_length_and_dots():
    url = "https://sub.example.com/path"
    feats = extract_features(url, enable_whois=False)
    # [url_length, has_at, has_https, no_of_dots, has_ip, hyphen_count, domain_age]
    assert feats[0] == len(url)
    assert feats[1] == 0
    assert feats[2] == 1
    assert feats[3] == 2
    assert feats[4] == 0

def test_extract_features_df_columns():
    df = extract_features_df("https://example.com", enable_whois=False)
    assert len(df) == 1
    assert list(df.columns) == [
        'url_length', 'has_at_symbol', 'has_https',
        'no_of_dots', 'has_ip', 'hyphen_count', 'domain_age_days'
    ]

def test_check_whitelist():
    assert check_whitelist("https://google.com/search") is True
    assert check_whitelist("https://github.com/nithin/project") is True
    assert check_whitelist("https://fake-google-login.com") is False

def test_detect_brand_spoofing():
    assert detect_brand_spoofing("http://paypal-verify-account.com") is True
    assert detect_brand_spoofing("https://my-blog.com") is False

def test_apply_heuristics_whitelisted():
    res = apply_heuristics("https://google.com", base_risk_score=90)
    assert res['risk_score'] == 0
    assert res['is_whitelisted'] is True
    assert res['verdict'] == "SAFE (Whitelisted)"
