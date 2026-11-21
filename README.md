# FraudShield – Rule-Based Financial Fraud Detection

This version intentionally does **not** use AI, machine learning, model training, or pretrained models. It is a transparent rule-based transaction screening application.

## Features
- Single transaction risk assessment.
- Configurable rules and thresholds.
- Risk score from 0 to 100.
- LOW, MEDIUM, and HIGH risk classification.
- CSV batch analysis and downloadable results.
- Streamlit dashboard with Plotly charts.
- SQLite transaction history.

## Setup (Windows)
```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Setup (Linux/macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local address printed by Streamlit, usually http://localhost:8501.

## CSV columns
`amount`, `hour`, `transactions_last_hour`, `distance_km`, `failed_attempts`, `new_device`, `is_international`, and `merchant_category`.

Missing optional fields are treated as zero/default values.

## Risk scoring
| Triggered rule | Points |
|---|---:|
| Amount reaches configured high-amount threshold | 25 |
| Transaction falls in configured late-night window | 15 |
| Transactions in last hour exceed configured limit | 20 |
| Distance reaches configured location threshold | 20 |
| Failed attempts reach configured limit | 15 |
| New/unknown device | 10 |
| International transaction | 10 |

The total is capped at 100. LOW = 0–29, MEDIUM = 30–59, HIGH = 60–100.

These weights and thresholds are illustrative and must be calibrated and validated for the intended environment. A high score is an alert for review, not proof of fraud.
