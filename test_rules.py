from fraudshield.rules import analyze_transaction

def test_low_risk_transaction():
    result = analyze_transaction({
        "amount": 1000, "hour": 14, "transactions_last_hour": 1,
        "distance_km": 2, "failed_attempts": 0,
        "new_device": 0, "is_international": 0
    })
    assert result["risk_level"] == "LOW"
    assert result["risk_score"] == 0

def test_multiple_rules_raise_risk():
    result = analyze_transaction({
        "amount": 80000, "hour": 2, "transactions_last_hour": 8,
        "distance_km": 250, "failed_attempts": 4,
        "new_device": 1, "is_international": 1
    })
    assert result["risk_level"] == "HIGH"
    assert result["risk_score"] == 100
    assert len(result["reasons"]) >= 6

def test_medium_risk():
    result = analyze_transaction({
        "amount": 60000, "hour": 14, "transactions_last_hour": 1,
        "distance_km": 2, "failed_attempts": 0,
        "new_device": 0, "is_international": 0
    })
    assert result["risk_level"] == "LOW" or result["risk_level"] == "MEDIUM"
