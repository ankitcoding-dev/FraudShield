# FRAUDSHIELD
## Rule-Based Financial Fraud Detection System
### College Project Report

## 1. Abstract
FraudShield is a Python-based financial transaction screening application. It checks transaction attributes against a set of predefined fraud-risk rules and calculates a risk score from 0 to 100. It classifies transactions into LOW, MEDIUM, and HIGH risk categories. The system includes a Streamlit dashboard, CSV batch analysis, visual summaries, and SQLite transaction history. This version does not use artificial intelligence or machine learning.

## 2. Problem Statement
Financial institutions face increasingly sophisticated fraudulent transactions. The objective is to create a transaction monitoring system that identifies suspicious patterns and raises alerts while keeping its decisions understandable.

## 3. Objectives
1. Analyze transaction details.
2. Detect suspicious patterns using predefined conditions.
3. Calculate a transparent risk score.
4. Categorize transactions into risk levels.
5. Support CSV-based batch analysis.
6. Maintain transaction history.
7. Provide a dashboard for monitoring results.

## 4. Scope
This is an academic prototype that demonstrates rule-based transaction monitoring. It does not connect to banking/payment networks and must not be used to automatically block real payments.

## 5. Technologies Used
- Python: application logic.
- Streamlit: web dashboard.
- Pandas and NumPy: tabular data and sample data generation.
- Plotly: charts.
- SQLite: local transaction storage.

## 6. System Modules
1. Input module: accepts transaction details manually or through CSV.
2. Rule engine: checks amount, time, transaction frequency, location distance, failed attempts, device, and international status.
3. Risk scoring module: adds points for each triggered rule.
4. Decision module: classifies the risk score.
5. Dashboard module: displays metrics and charts.
6. Database module: stores and retrieves analyzed transactions.

## 7. Rule Engine and Scoring
| Rule | Condition (default) | Score |
|---|---|---:|
| High amount | Amount >= ₹50,000 | 25 |
| Late night | Hour from 00:00 through 04:00 | 15 |
| High frequency | More than 5 transactions/hour | 20 |
| Far location | Distance >= 100 km | 20 |
| Failed attempts | 3 or more | 15 |
| New device | New device indicator = 1 | 10 |
| International | International indicator = 1 | 10 |

The sum of triggered rule points is capped at 100.

- LOW: 0–29 points.
- MEDIUM: 30–59 points.
- HIGH: 60–100 points.

Thresholds are configurable in the dashboard. The score is an explainable rule score, not a statistical probability that a transaction is fraudulent.

## 8. False-Positive Considerations
A false positive occurs when a legitimate transaction is flagged. The prototype makes its rules and points visible so an operator can understand why an alert was generated. Thresholds can be adjusted, and medium-risk transactions can be reviewed rather than automatically blocked. In a real deployment, rules must be tested on representative historical data, monitored for customer impact, and approved by domain experts.

## 9. Database Design
The SQLite table stores transaction ID, amount, risk score, risk level, decision, timestamp, and a JSON representation of the analyzed record.

## 10. Hardware and Software Requirements
Hardware: ordinary laptop/desktop with 4 GB RAM recommended.
Software: Python 3.10+, pip, and a modern web browser.

## 11. Installation and Execution
1. Extract the project ZIP.
2. Open the project directory in VS Code.
3. Create and activate a virtual environment.
4. Install dependencies using `pip install -r requirements.txt`.
5. Run `streamlit run app.py`.
6. Open the local URL printed in the terminal.

## 12. Test Cases
| Test | Input | Expected behavior |
|---|---|---|
| Normal purchase | Low amount, daytime, familiar location/device | Usually LOW |
| Large amount | Amount >= configured limit | Adds 25 points |
| Late-night purchase | Hour 0–4 by default | Adds 15 points |
| Rapid transactions | More than configured hourly count | Adds 20 points |
| Distant location | Distance >= configured limit | Adds 20 points |
| Failed attempts | At least 3 by default | Adds 15 points |
| New device | New device = Yes | Adds 10 points |
| CSV upload | Valid CSV file | Displays scores and export option |

## 13. Advantages
- Simple to understand and implement.
- Transparent decisions.
- Low computational requirements.
- Easy to adjust business rules.
- No model training or external dataset required.

## 14. Limitations
- Rules cannot automatically learn new fraud patterns.
- Fixed thresholds may not fit every customer.
- Fraudsters may adapt to known rules.
- A rule score is not a calibrated fraud probability.
- Real deployment requires security, privacy, monitoring, and human oversight.

## 15. Future Enhancements
- Customer-specific baselines.
- Rule management with role-based permissions.
- Audit logs and secure authentication.
- Integration with a payment simulator.
- Validation against anonymized historical data.
- Optional ML extension in a separate future version.

## 16. Conclusion
FraudShield demonstrates a complete rule-based transaction monitoring workflow. It identifies suspicious transaction attributes, calculates an explainable risk score, classifies risk, and provides dashboard reporting and transaction history. It meets the academic objective without implementing an AI or machine-learning model.

## References
1. Python documentation: https://docs.python.org/3/
2. Streamlit documentation: https://docs.streamlit.io/
3. Pandas documentation: https://pandas.pydata.org/docs/
4. SQLite documentation: https://www.sqlite.org/docs.html
5. Plotly Python documentation: https://plotly.com/python/
