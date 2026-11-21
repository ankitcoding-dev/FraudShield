import pandas as pd

DEFAULT_CONFIG = {
    "high_amount": 50000.0,
    "night_start": 0,
    "night_end": 4,
    "max_tx_hour": 5,
    "location_km": 100.0,
    "failed_limit": 3,
}

RULES = [
    ("high_amount", 25, "High transaction amount"),
    ("late_night", 15, "Late-night transaction"),
    ("high_velocity", 20, "High transaction frequency"),
    ("far_location", 20, "Unusual transaction location"),
    ("failed_attempts", 15, "Multiple failed attempts"),
    ("new_device", 10, "New or unknown device"),
    ("international", 10, "International transaction"),
]

def _as_number(row, key, default=0):
    try:
        value = pd.to_numeric(row.get(key, default), errors="coerce")
        return default if pd.isna(value) else float(value)
    except (TypeError, ValueError):
        return float(default)

def _is_night(hour, start, end):
    # Supports ranges that cross midnight, such as 22:00–04:00.
    if start <= end:
        return start <= hour <= end
    return hour >= start or hour <= end

def analyze_transaction(row, config=None):
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    amount = _as_number(row, "amount")
    hour = int(_as_number(row, "hour", 12)) % 24
    velocity = _as_number(row, "transactions_last_hour")
    distance = _as_number(row, "distance_km")
    failed = _as_number(row, "failed_attempts")
    new_device = bool(_as_number(row, "new_device"))
    international = bool(_as_number(row, "is_international"))

    checks = {
        "high_amount": amount >= cfg["high_amount"],
        "late_night": _is_night(hour, int(cfg["night_start"]), int(cfg["night_end"])),
        "high_velocity": velocity > cfg["max_tx_hour"],
        "far_location": distance >= cfg["location_km"],
        "failed_attempts": failed >= cfg["failed_limit"],
        "new_device": new_device,
        "international": international,
    }

    score = sum(points for key, points, _ in RULES if checks[key])
    score = min(score, 100)
    level = "HIGH" if score >= 60 else ("MEDIUM" if score >= 30 else "LOW")
    decision = "FLAG FOR REVIEW" if level == "HIGH" else (
        "REVIEW" if level == "MEDIUM" else "NO ALERT"
    )
    reasons = [label for key, _, label in RULES if checks[key]]

    result = dict(row)
    result.update({
        "risk_score": int(score),
        "risk_level": level,
        "decision": decision,
        "reasons": reasons,
    })
    return result

def analyze_dataframe(frame, config=None):
    if not isinstance(frame, pd.DataFrame):
        frame = pd.DataFrame(frame)
    rows = [analyze_transaction(row.to_dict(), config) for _, row in frame.iterrows()]
    return pd.DataFrame(rows)

def explain_transaction(row, config=None):
    return analyze_transaction(row, config)["reasons"]
