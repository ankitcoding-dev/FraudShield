import streamlit as st
import pandas as pd
import plotly.express as px
from fraudshield.rules import analyze_transaction, analyze_dataframe, explain_transaction
from fraudshield.storage import init_db, save_transactions, load_transactions, clear_history
from fraudshield.data import make_sample_transactions

st.set_page_config(page_title="FraudShield", page_icon="🛡️", layout="wide")
st.title("🛡️ FraudShield")
st.caption("Rule-Based Financial Fraud Detection System | Python College Project")

init_db()

with st.sidebar:
    st.header("Risk rule settings")
    st.caption("Adjust the thresholds used by the rule engine.")
    high_amount = st.number_input("High transaction amount (₹)", min_value=1000, value=50000, step=5000)
    night_start = st.slider("Late-night start hour", 0, 23, 0)
    night_end = st.slider("Late-night end hour", 0, 23, 4)
    max_tx_hour = st.number_input("Transactions/hour alert threshold", min_value=1, value=5)
    location_km = st.number_input("Unusual location distance (km)", min_value=1, value=100)
    failed_limit = st.number_input("Failed attempts alert threshold", min_value=1, value=3)
    st.divider()
    st.info("This version uses explicit rules only. It does not train or load an AI/ML model.")

config = {
    "high_amount": float(high_amount),
    "night_start": int(night_start),
    "night_end": int(night_end),
    "max_tx_hour": int(max_tx_hour),
    "location_km": float(location_km),
    "failed_limit": int(failed_limit),
}

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Dashboard", "Analyze transaction", "CSV analysis", "History", "About"
])

with tab1:
    st.subheader("Fraud monitoring dashboard")
    history = load_transactions()
    if history.empty:
        st.info("No saved transactions yet. Showing a sample demonstration dataset.")
        demo = make_sample_transactions(100, seed=19)
        view = analyze_dataframe(demo, config)
    else:
        view = history

    total = len(view)
    flagged = int((view["risk_level"] == "HIGH").sum()) if total else 0
    medium = int((view["risk_level"] == "MEDIUM").sum()) if total else 0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Transactions", f"{total:,}")
    c2.metric("High-risk alerts", f"{flagged:,}")
    c3.metric("Medium-risk", f"{medium:,}")
    c4.metric("High-risk rate", f"{flagged / total * 100:.1f}%" if total else "0%")

    left, right = st.columns(2)
    with left:
        st.plotly_chart(
            px.pie(view, names="risk_level", title="Risk level distribution", hole=0.4),
            use_container_width=True
        )
    with right:
        st.plotly_chart(
            px.histogram(view, x="risk_score", nbins=20, title="Risk score distribution"),
            use_container_width=True
        )
    st.subheader("Recent transactions")
    st.dataframe(view.tail(15), use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Analyze a transaction")
    with st.form("transaction_form"):
        c1, c2, c3 = st.columns(3)
        amount = c1.number_input("Transaction amount (₹)", min_value=0.0, value=2500.0, step=100.0)
        hour = c2.slider("Transaction hour", 0, 23, 14)
        tx_hour = c3.number_input("Transactions in the last hour", min_value=0, value=1)
        c4, c5, c6 = st.columns(3)
        distance = c4.number_input("Distance from usual location (km)", min_value=0.0, value=5.0)
        failed = c5.number_input("Recent failed attempts", min_value=0, value=0)
        device = c6.selectbox("New/unknown device?", ["No", "Yes"])
        c7, c8 = st.columns(2)
        international = c7.selectbox("International transaction?", ["No", "Yes"])
        merchant = c8.selectbox(
            "Merchant category",
            ["Grocery", "Fuel", "Shopping", "Travel", "Electronics", "Digital goods", "Other"]
        )
        submit = st.form_submit_button("Check transaction", type="primary")

    if submit:
        record = {
            "amount": amount, "hour": hour, "transactions_last_hour": tx_hour,
            "distance_km": distance, "failed_attempts": failed,
            "new_device": int(device == "Yes"),
            "is_international": int(international == "Yes"),
            "merchant_category": merchant
        }
        result = analyze_transaction(record, config)
        result["transaction_id"] = f"TX-{pd.Timestamp.now().strftime('%y%m%d%H%M%S')}"
        save_transactions(pd.DataFrame([result]))
        a, b, c = st.columns(3)
        a.metric("Risk score", f"{result['risk_score']}/100")
        b.metric("Risk level", result["risk_level"])
        c.metric("Decision", result["decision"])
        if result["risk_level"] == "HIGH":
            st.error("High-risk transaction. Send for manual investigation.")
        elif result["risk_level"] == "MEDIUM":
            st.warning("Some risk indicators found. Review recommended.")
        else:
            st.success("No major configured risk indicators found.")
        st.write("**Triggered rules**")
        for reason in result["reasons"]:
            st.write(f"• {reason}")
        if not result["reasons"]:
            st.write("• No configured risk rules were triggered.")

with tab3:
    st.subheader("Analyze transactions from CSV")
    sample = make_sample_transactions(5, seed=4)
    st.download_button("Download CSV template", sample.to_csv(index=False), "fraudshield_template.csv", "text/csv")
    upload = st.file_uploader("Upload transaction CSV", type=["csv"])
    if upload:
        try:
            raw = pd.read_csv(upload)
            results = analyze_dataframe(raw, config)
            st.dataframe(results, use_container_width=True, hide_index=True)
            st.metric("High-risk transactions", int((results["risk_level"] == "HIGH").sum()))
            st.download_button("Download analyzed CSV", results.to_csv(index=False),
                               "fraudshield_analyzed.csv", "text/csv")
            if st.button("Save these results to history"):
                save_transactions(results)
                st.success(f"Saved {len(results)} transactions.")
        except Exception as exc:
            st.error(f"Unable to process CSV: {exc}")

with tab4:
    st.subheader("Transaction history")
    history = load_transactions()
    if history.empty:
        st.info("No transaction records saved yet.")
    else:
        st.dataframe(history, use_container_width=True, hide_index=True)
        st.download_button("Export history", history.to_csv(index=False), "fraudshield_history.csv", "text/csv")
        if st.button("Clear transaction history"):
            clear_history()
            st.success("History cleared. Refresh the page to update the table.")

with tab5:
    st.subheader("About FraudShield")
    st.markdown("""
**FraudShield** is a rule-based financial fraud detection prototype for academic demonstration.

It checks transaction details against transparent, configurable conditions:
- unusually high transaction amount;
- late-night activity;
- unusually high transaction frequency;
- large distance from the usual location;
- repeated failed attempts;
- new device;
- international transaction.

Each triggered rule adds points to a risk score. The total score is converted into LOW, MEDIUM, or HIGH risk.

**No machine learning or AI model is used.** This is a decision-support demonstration, not a production banking security system. Rules need institution-specific calibration, testing, and human review before any real-world use.
""")
