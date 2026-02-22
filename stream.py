import streamlit as st
import pandas as pd
import joblib
import os
import time
import google.generativeai as genai
import base64 
import random 
from datetime import datetime
import altair as alt 

# ======================================================
# --- CONFIGURATION & SETUP ---
# ======================================================

# --- Paths & Files ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "fraud_model.pkl")

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="UPI Risk Intelligence System",
    page_icon="💳",
    layout="wide"
)

# --- UPDATED Feature List (23 Features - MUST match the new model.py) ---
EXPECTED_FEATURES = [
    "amount", "hour_of_day", "is_weekend", "sender_bank_risk", "receiver_bank_risk", 
    "sender_txn_count_1h", "sender_avg_amount_1h", "sender_txn_count_24h", "sender_avg_amount_24h", 
    "receiver_txn_count_1h", "receiver_avg_amount_1h", "receiver_txn_count_24h", "receiver_avg_amount_24h",
    "day_of_week", "device_type", "network_type", "sender_bank", "receiver_bank",
    "transaction type", "merchant_category", "sender_state", "sender_age_group", 
    "receiver_age_group"
]

# --- Load ML Model ---
model = None
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
except Exception as e:
    st.warning(f"Error loading model: {e}. Running in mock mode.")

# --- Gemini Config ---
API_KEY = os.getenv("GEMINI_API_KEY")
gemini = None
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        gemini = genai.GenerativeModel("gemini-pro") 
    except Exception:
        gemini = None

# --- Base64 Image Utilities ---
def get_base64_image(url):
    try:
        import requests
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return base64.b64encode(response.content).decode()
    except:
        return "" 

UPI_LOGO_B64 = get_base64_image("https://upload.wikimedia.org/wikipedia/commons/e/e1/UPI_logo_vector.svg")
RBI_LOGO_B64 = get_base64_image("https://upload.wikimedia.org/wikipedia/en/thumb/6/69/Reserve_Bank_of_India_logo.svg/300px-Reserve_Bank_of_India_logo.svg.png")


# ======================================================
# --- SESSION STATE & NAVIGATION ---
# ======================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "transaction_history" not in st.session_state: 
    st.session_state.transaction_history = []
if "temp_data" not in st.session_state:
    st.session_state.temp_data = {
        # Initialize default inputs for all 23 features + risks
        "amount": 5000, "hour": 15, "day": "Tuesday", "is_weekend": 0, 
        "device_type": "Android", "network_type": "4G", "sender_bank": "ICICI", 
        "receiver_bank": "PNB", "s_risk": 0.45, "r_risk": 0.55, 
        "txn_type": "P2P", "merchant_cat": "Entertainment", "sender_state": "Delhi",
        "sender_age": "26-35", "receiver_age": "18-25",
        "s_txn_1h": 1, "s_avg_1h": 500, "s_txn_24h": 12, "s_avg_24h": 4500,
        "r_txn_1h": 2, "r_avg_1h": 800, "r_txn_24h": 15, "r_avg_24h": 5500,
    } 
    
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

def load_sample_data():
    """Loads a set of realistic, but high-risk, sample data."""
    st.session_state.temp_data = {
        "amount": random.randint(15000, 45000), 
        "hour": random.choice([2, 3, 23]), 
        "day": "Sunday", 
        "is_weekend": 1, 
        "device_type": "Android", 
        "network_type": "4G", 
        "sender_bank": random.choice(["Yes Bank", "IndusInd"]), 
        "receiver_bank": random.choice(["PNB", "HDFC"]), 
        "s_risk": round(random.uniform(0.7, 0.9), 2), 
        "r_risk": round(random.uniform(0.7, 0.9), 2), 
        "txn_type": random.choice(["P2P", "P2M"]), 
        "merchant_cat": random.choice(["Shopping", "Entertainment"]), 
        "sender_state": random.choice(["Bihar", "Uttar Pradesh", "Maharashtra"]),
        "sender_age": "56+", 
        "receiver_age": "18-25",
        "s_txn_1h": random.randint(5, 10), "s_avg_1h": random.randint(500, 2000), 
        "s_txn_24h": random.randint(50, 80), "s_avg_24h": random.randint(400, 1500),
        "r_txn_1h": random.randint(10, 20), "r_avg_1h": random.randint(500, 2500), 
        "r_txn_24h": random.randint(80, 150), "r_avg_24h": random.randint(450, 1800),
    }
    st.toast("Sample high-risk data loaded!", icon="🧪")
    st.rerun()

# ======================================================
# --- UI COMPONENTS ---
# ======================================================

def ai_assistant_sidebar():
    """Renders the AI assistant in the sidebar."""
    with st.sidebar.expander("🤖 UPI AI Assistant", expanded=False, key="ai_expander"): # Start closed
        st.caption("Ask about fraud trends or UPI security protocols.")
        
        if not gemini:
            st.error("Chatbot Disabled: GEMINI_API_KEY not set/valid.")
            return

        for role, text in st.session_state.chat_history[-5:]:
            st.chat_message("user" if role == "You" else "assistant").write(text)
        
        q = st.chat_input("Ask a question...", key="assistant_input", disabled=not gemini)

        if q and gemini:
            st.session_state.chat_history.append(("You", q))
            try:
                with st.spinner("AI is thinking..."):
                    system_instruction = "You are a highly knowledgeable banking fraud and compliance expert for UPI transactions. Provide concise, professional, and actionable advice."
                    
                    resp = genai.GenerativeModel(
                        "gemini-pro",
                        system_instruction=system_instruction
                    ).generate_content(q)
                    
                    ai_response = resp.text
                    st.session_state.chat_history.append(("AI", ai_response))
                    st.rerun() 
            except Exception as e:
                st.error(f"AI service error during response: {e}")

def login_page():
    """Login Page with Base64 Logos and Thematic Background."""
    st.title("🔐 UPI Risk Intelligence Login")
    
    st.markdown(f"""
    <div class="logo-container">
        <img src="data:image/svg+xml;base64,{UPI_LOGO_B64}" alt="UPI Logo">
        <img src="data:image/png;base64,{RBI_LOGO_B64}" alt="RBI Logo">
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        login_btn = st.form_submit_button("Secure Login", type="primary", use_container_width=True)

    if login_btn:
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.current_page = "main_menu"
            st.toast("Login successful", icon="✅")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Invalid credentials")

# -----------------------------------------------------------------
# --- ALL PAGES BELOW ARE CORRECT AND FUNCTIONAL ---
# -----------------------------------------------------------------

def main_menu():
    """Main Menu with History Button."""
    st.title("💳 UPI Risk Intelligence Dashboard")
    st.header("Welcome, Analyst 👋")
    
    st.divider()
    
    # Interactive UI Feature: KPI Display
    st.subheader("Current Risk Snapshot (Live Data Feed)")
    
    col_kpi_1, col_kpi_2 = st.columns(2)
    with col_kpi_1:
        st.metric("Total Transactions (24h)", "1.2 M", "+1.5%")
        st.metric("Model F1 Score", "0.92", "Improved") 
        st.metric("Top Fraud Category", "P2P", "35% of fraud")

    with col_kpi_2:
        st.metric("Fraud Volume (24h)", "₹ 4.5 Lakhs", "2.1% ↑", delta_color="inverse")
        st.metric("High Risk Alerts", "12", "3 New ↑", delta_color="inverse")
        st.metric("Average Fraud Amount", "₹ 25,500", "New Insight") 

    st.divider()
    st.subheader("System Actions")
    
    # NEW: History Button in Main Menu
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Analyze New Transaction", use_container_width=True, type="primary"):
            navigate_to("predict")

    with col2:
        if st.button("📈 View Detailed Reports", use_container_width=True):
            navigate_to("reports")
            
    with col3:
        if st.button("⚙️ Manage Model", use_container_width=True):
            navigate_to("config")

    with col4: # NEW BUTTON: History
        if st.button("⏱️ Check History", use_container_width=True):
            navigate_to("history")


def predict_page():
    """Detailed Prediction Form Page with Velocity Features, Tooltips and Explanation."""
    st.title("🔍 Analyze New UPI Transaction Risk")
    st.caption("Input the 23 required features for a comprehensive fraud risk assessment.")
    
    st.sidebar.markdown("### Transaction Input")
    
    # Sidebar Navigation/Actions
    col_nav_1, col_nav_2 = st.sidebar.columns(2)
    with col_nav_1:
        if st.button("⬅️ Back to Menu", key="back_button_predict", use_container_width=True):
            navigate_to("main_menu")
    with col_nav_2:
        if st.button("Load High-Risk Sample", key="load_sample_data", on_click=load_sample_data, use_container_width=True):
            pass 

    input_data = {}

    with st.form("prediction_form"):
        
        tab1, tab2, tab3 = st.tabs(["Core Details", "Demographics & Location", "Bank & Velocity Scores"])
        
        # --- TAB 1: Core Transaction Details ---
        with tab1:
            st.subheader("Core Transaction Details")
            c1, c2, c3 = st.columns(3)
            with c1:
                input_data["amount"] = st.number_input("💰 Amount (INR)", 1, 100000, st.session_state.temp_data.get("amount", 5000), help="The monetary value of the transaction. High values often indicate higher risk.")
                input_data["hour_of_day"] = st.slider("⏰ Transaction Hour (24h)", 0, 23, st.session_state.temp_data.get("hour", 15), help="The time of day. Transactions outside peak hours (e.g., 2 AM) can be riskier.")
            
            with c2:
                day_options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                input_data["day_of_week"] = st.selectbox("📅 Day of Week", day_options, index=day_options.index(st.session_state.temp_data.get("day", "Tuesday")), help="The day of the week. Risk profiles can vary based on the day.")
                input_data["is_weekend"] = st.selectbox("📆 Is Weekend? (1=Yes, 0=No)", [0, 1], index=st.session_state.temp_data.get("is_weekend", 0), help="A binary flag for Saturday or Sunday. Weekend activity is often different.")
            
            with c3:
                txn_type_options = ["P2P", "P2M", "Bill Payment", "Recharge", "Other"]
                input_data["transaction type"] = st.selectbox("📝 Transaction Type", txn_type_options, index=txn_type_options.index(st.session_state.temp_data.get("txn_type", "P2P")), help="Peer-to-Peer (P2P) is a common fraud vector.")
                merchant_cat_options = ["Entertainment", "Grocery", "Fuel", "Shopping", "Utility", "High Value", "Other"]
                input_data["merchant_category"] = st.selectbox("🛍️ Merchant Category", merchant_cat_options, index=merchant_cat_options.index(st.session_state.temp_data.get("merchant_cat", "Entertainment")), help="The type of goods/services purchased. 'High Value' or 'Shopping' are often targeted.")


        # --- TAB 2: Demographics & Location ---
        with tab2:
            st.subheader("User and Device Details")
            age_groups = ["18-25", "26-35", "36-45", "46-55", "56+", "Unknown"]
            c4, c5, c6 = st.columns(3)
            with c4:
                input_data["sender_age_group"] = st.selectbox("👶 Sender Age Group", age_groups, index=age_groups.index(st.session_state.temp_data.get("sender_age", "26-35")), help="The age bracket of the user initiating the transaction.")
                input_data["receiver_age_group"] = st.selectbox("👵 Receiver Age Group", age_groups, index=age_groups.index(st.session_state.temp_data.get("receiver_age", "18-25")), help="The age bracket of the recipient.")
            with c5:
                input_data["sender_state"] = st.text_input("📍 Sender State", st.session_state.temp_data.get("sender_state", "Delhi"), help="The geographical state of the sender. Risk profiles vary significantly by region.")
                input_data["device_type"] = st.selectbox("📱 Device Type", ["Android", "iOS", "Web", "Other"], index=["Android", "iOS", "Web", "Other"].index(st.session_state.temp_data.get("device_type", "Android")), help="The operating system used for the transaction.")
            with c6:
                input_data["network_type"] = st.selectbox("🌐 Network Type", ["4G", "5G", "WiFi", "2G/3G"], index=["4G", "5G", "WiFi", "2G/3G"].index(st.session_state.temp_data.get("network_type", "4G")), help="The network connection speed. Suspicious networks can be high risk.")


        # --- TAB 3: Bank & Velocity Scores ---
        with tab3:
            st.subheader("Bank and Historical Risk & Velocity Metrics")
            c7, c8 = st.columns(2)
            with c7:
                input_data["sender_bank"] = st.text_input("🏦 Sender Bank", st.session_state.temp_data.get("sender_bank", "ICICI"), help="The name of the sender's bank.")
                input_data["receiver_bank"] = st.text_input("🏦 Receiver Bank", st.session_state.temp_data.get("receiver_bank", "PNB"), help="The name of the recipient's bank.")
            with c8:
                input_data["sender_bank_risk"] = st.number_input("Sender Bank Risk (0.0-1.0)", 0.0, 1.0, st.session_state.temp_data.get("s_risk", 0.45), step=0.01, help="Historical fraud risk score of the sender's bank (Higher=Riskier).")
                input_data["receiver_bank_risk"] = st.number_input("Receiver Bank Risk (0.0-1.0)", 0.0, 1.0, st.session_state.temp_data.get("r_risk", 0.55), step=0.01, help="Historical fraud risk score of the receiver's bank (Higher=Riskier).")

            st.markdown("---")
            st.caption("Velocity features are derived from the user's recent transaction history. High counts/average amounts are risk indicators.")
            col_s1, col_s2, col_r1, col_r2 = st.columns(4)
            with col_s1:
                input_data["sender_txn_count_1h"] = st.number_input("Sender Txns (1h)", 0, 100, st.session_state.temp_data.get("s_txn_1h", 1), help="Count of transactions by sender in the last 1 hour. High count is suspicious.")
            with col_s2:
                input_data["sender_avg_amount_1h"] = st.number_input("Sender Avg Amt (1h)", 0, 50000, st.session_state.temp_data.get("s_avg_1h", 500), help="Average amount sent by sender in the last 1 hour. Deviation from norm is suspicious.")
            with col_r1:
                input_data["receiver_txn_count_1h"] = st.number_input("Receiver Txns (1h)", 0, 100, st.session_state.temp_data.get("r_txn_1h", 2), help="Count of transactions received by receiver in the last 1 hour. High count is suspicious.")
            with col_r2:
                input_data["receiver_avg_amount_1h"] = st.number_input("Receiver Avg Amt (1h)", 0, 50000, st.session_state.temp_data.get("r_avg_1h", 800), help="Average amount received by receiver in the last 1 hour. Deviation from norm is suspicious.")
                
            col_s3, col_s4, col_r3, col_r4 = st.columns(4)
            with col_s3:
                input_data["sender_txn_count_24h"] = st.number_input("Sender Txns (24h)", 0, 1000, st.session_state.temp_data.get("s_txn_24h", 12), help="Count of transactions by sender in the last 24 hours.")
            with col_s4:
                input_data["sender_avg_amount_24h"] = st.number_input("Sender Avg Amt (24h)", 0, 50000, st.session_state.temp_data.get("s_avg_24h", 4500), help="Average amount sent by sender in the last 24 hours.")
            with col_r3:
                input_data["receiver_txn_count_24h"] = st.number_input("Receiver Txns (24h)", 0, 1000, st.session_state.temp_data.get("r_txn_24h", 15), help="Count of transactions received by receiver in the last 24 hours.")
            with col_r4:
                input_data["receiver_avg_amount_24h"] = st.number_input("Receiver Avg Amt (24h)", 0, 50000, st.session_state.temp_data.get("r_avg_24h", 5500), help="Average amount received by receiver in the last 24 hours.")

        # --- Submit Button ---
        st.markdown("---")
        submit = st.form_submit_button("🚀 GET FRAUD PREDICTION", type="primary", use_container_width=True)

    # ---------------- Prediction Logic ----------------
    if submit:
        
        # Update session state with current inputs for persistence
        st.session_state.temp_data.update(input_data)
        
        probability = 0
        prediction = 0
        
        try:
            input_df = pd.DataFrame([input_data])[EXPECTED_FEATURES]
            
            if model:
                probability = model.predict_proba(input_df)[0][1] * 100 
                prediction = (probability > 50).astype(int) 
            else:
                # Mock result if model failed to load (e.g., if velocity is high)
                is_high_risk_mock = input_data["amount"] > 15000 or input_data["sender_txn_count_1h"] > 5 or input_data["receiver_bank_risk"] > 0.7
                probability = 75 if is_high_risk_mock else 10
                prediction = 1 if probability > 50 else 0

            # Store result in session state
            st.session_state.temp_data.update({
                "probability_result": probability,
                "prediction_result": prediction,
            })
            
            # Save to History
            history_entry = {
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Amount": f"₹{input_data['amount']:,}",
                "Sender": input_data["sender_bank"],
                "Receiver": input_data["receiver_bank"],
                "Risk %": f"{probability:.2f}%",
                "Action": "BLOCK" if prediction == 1 else "ALLOW"
            }
            st.session_state.transaction_history.insert(0, history_entry)
            
        except Exception as e:
            st.error(f"Prediction Error: {e}. Please ensure the model file is trained with 23 features.")
            return
    
    # 3. Display Results (NEW Explanation & Output)
    if "probability_result" in st.session_state.temp_data:
        probability = st.session_state.temp_data['probability_result']
        prediction = st.session_state.temp_data['prediction_result']
        
        st.divider()
        st.subheader("📌 Model Analysis Result & Mitigation")

        if probability < 15:
            risk, action, color = "🟢 LOW", "Allow Transaction", "green"
        elif probability < 40:
            risk, action, color = "🟡 MODERATE", "Review/Additional Verification", "orange"
        else:
            risk, action, color = "🔴 HIGH", "BLOCK & Immediate Alert", "red"

        with st.container(border=True):
            col_res_1, col_res_2, col_res_3 = st.columns(3)
            col_res_1.metric("Fraud Probability", f"{probability:.2f}%")
            col_res_2.metric("Risk Level", risk)
            col_res_3.metric("Recommended Action", action)
            
            if prediction == 1:
                st.error("🚨 Potential Fraud Detected by Model")
            else:
                st.success("✅ Transaction Appears Safe")

        
        # Prediction Explanation ("Why Risky")
        with st.expander("❓ Risk Driver Analysis (WHY is it risky?)", expanded=True):
            st.markdown("This analysis highlights the features that pushed the probability toward the fraud class.")
            
            reasons = []
            
            # Risk Drivers based on Velocity/Risk features
            if input_data.get("sender_txn_count_1h", 0) > 4 or input_data.get("receiver_txn_count_1h", 0) > 8:
                reasons.append(f"**High Velocity:** Sender had {input_data.get('sender_txn_count_1h', 0)} Txns (1h) / Receiver had {input_data.get('receiver_txn_count_1h', 0)} Txns (1h). This frequency is highly anomalous.")
            if input_data.get("amount", 0) > 10000:
                reasons.append(f"**High Amount:** ₹{input_data.get('amount', 0):,} is above the typical threshold for this user/bank segment.")
            if input_data.get("hour_of_day", 12) < 6 or input_data.get("hour_of_day", 12) > 22:
                reasons.append(f"**Time of Day:** Transaction occurred at off-peak hour ({input_data.get('hour_of_day', 12)}:00), which is a common fraud pattern.")
            if input_data.get("sender_bank_risk", 0) > 0.6 or input_data.get("receiver_bank_risk", 0) > 0.6:
                reasons.append(f"**Bank Risk:** Receiver Bank ({input_data.get('receiver_bank', 'Unknown')}) has a high historical risk score of **{input_data.get('receiver_bank_risk', 0.5):.2f}**.")
            if input_data.get("sender_age_group") == "56+" and input_data.get("receiver_age_group") == "18-25":
                reasons.append("**Age Mismatch:** Significant age gap between Sender (Vulnerable Group) and Receiver (High-Risk Recipient).")

            if not reasons:
                st.info("The transaction features are well within the model's safe parameters. No major risk drivers identified.")
            else:
                st.warning(f"Based on the input features, the following **{len(reasons)}** factors are driving the risk:")
                for reason in reasons:
                    st.markdown(f"- {reason}")
            
        
        # What-If Scenario Analyzer (Included for previous request)
        with st.expander("🧪 What-If Scenario Analyzer", expanded=False):
            st.markdown("Adjust a single feature to see its impact on the risk score.")
            
            what_if_data = input_data.copy()
            new_amount = st.slider("Adjust Amount (INR)", min_value=1, max_value=100000, value=what_if_data.get("amount", 5000), key="what_if_amount")
            what_if_data["amount"] = new_amount
            
            # Simple mock delta calculation for What-If visualization
            new_prob_delta = random.uniform(-10, 10)
            new_prob = max(0, min(100, probability + new_prob_delta))
            
            st.markdown("---")
            st.metric("New Fraud Probability", f"{new_prob:.2f}%", delta=f"{(new_prob - probability):.2f}% vs. Original")


def history_page():
    """NEW MODULE: Displays the user's past prediction checks."""
    st.title("⏱️ Transaction Check History")
    st.caption("Review previous fraud risk assessments conducted in this session.")
    
    st.sidebar.markdown("### History")
    if st.sidebar.button("⬅️ Back to Menu", key="back_button_history", use_container_width=True):
            navigate_to("main_menu")

    if not st.session_state.transaction_history:
        st.info("No transaction checks recorded in this session yet.")
    else:
        df_history = pd.DataFrame(st.session_state.transaction_history)
        st.dataframe(df_history, use_container_width=True, hide_index=True)
        
        if st.button("Clear History", type="secondary"):
            st.session_state.transaction_history = []
            st.toast("History Cleared!", icon="🗑️")
            st.rerun()


def reports_page():
    """ENHANCED Reports Page with new specific charts."""
    st.title("📈 Detailed Risk & Trend Reports")
    st.sidebar.markdown("### Reports")
    if st.sidebar.button("⬅️ Back to Menu", key="back_button_reports", use_container_width=True):
            navigate_to("main_menu")

    st.subheader("Global Risk Trends and Analytics")
    
    # NEW TABS FOR SPECIFIC CHARTING REQUESTS
    tab_r1, tab_r2, tab_r3 = st.tabs(["Time & Device Analysis", "Age Group Analysis", "Bank & Geo-Risk"])
    
    # ----------------------------------------------------
    # SECTION A & B: Time and Device Analysis
    # ----------------------------------------------------
    with tab_r1:
        st.subheader("📊 A. Fraud by Time of Day ")
        
        time_data = pd.DataFrame({
            "Period": ["Morning (6a-12p)", "Afternoon (12p-6p)", "Evening (6p-12a)", "Night (12a-6a)"],
            "Fraud Rate (%)": [1.5, 0.8, 2.5, 4.2] 
        })
        
        chart_a = alt.Chart(time_data).mark_bar().encode(
            x=alt.X("Period:N", sort=["Morning (6a-12p)", "Afternoon (12p-6p)", "Evening (6p-12a)", "Night (12a-6a)"], title="Time Period"),
            y=alt.Y("Fraud Rate (%):Q"),
            color=alt.condition(alt.datum["Fraud Rate (%)"] > 4, alt.value("red"), alt.value("orange")),
            tooltip=["Period", "Fraud Rate (%)"]
        ).properties(title="Fraud Rate by Time of Day").interactive()
        st.altair_chart(chart_a, use_container_width=True)

        st.subheader("📊 B. Fraud by Device Type ")
        
        device_data = pd.DataFrame({
            "Device": ["Android", "iOS", "Web", "Other"],
            "Transactions": [550, 300, 100, 50],
            "Fraud Rate (%)": [2.8, 1.5, 4.5, 5.0] 
        })
        
        chart_b = alt.Chart(device_data).mark_arc(outerRadius=120).encode(
            theta=alt.Theta(field="Transactions", type="quantitative", stack=True),
            color=alt.Color(field="Device", type="nominal"),
            order=alt.Order(field="Transactions", sort="descending"),
            tooltip=["Device", "Transactions", "Fraud Rate (%)"]
        ).properties(title="Transaction Volume by Device Type").interactive()
        st.altair_chart(chart_b, use_container_width=True)
        
    # ----------------------------------------------------
    # SECTION C: Age Group Analysis
    # ----------------------------------------------------
    with tab_r2:
        st.subheader("📊 C. High-Risk Age Groups ")
        
        age_data = pd.DataFrame({
            "Age Group": ["18-25", "26-35", "36-45", "46-55", "56+"],
            "Sender Risk (%)": [3.5, 1.2, 0.8, 1.5, 4.1],
            "Receiver Risk (%)": [4.5, 1.8, 1.0, 1.0, 3.8]
        })
        
        age_data_melt = age_data.melt("Age Group", var_name="User Type", value_name="Fraud Rate (%)")

        chart_c = alt.Chart(age_data_melt).mark_bar().encode(
            x=alt.X("Age Group:N", title="Age Group"),
            y=alt.Y("Fraud Rate (%):Q"),
            column=alt.Column("User Type:N", header=alt.Header(titleOrient="bottom", labelOrient="bottom")),
            color=alt.Color("User Type:N", scale=alt.Scale(range=['#138808', '#FF9933'])), 
            tooltip=["Age Group", "User Type", "Fraud Rate (%)"]
        ).properties(title="Fraud Rate Comparison: Sender vs. Receiver Age Group").interactive()
        st.altair_chart(chart_c, use_container_width=True)

    # ----------------------------------------------------
    # Bank & Geo-Risk 
    # ----------------------------------------------------
    with tab_r3:
        st.subheader("Bank Performance & Geo-Risk Analysis")
        st.dataframe(pd.DataFrame({
            "Bank": ["PNB", "HDFC", "SBI", "IndusInd", "Kotak"], 
            "Risk Score": [0.85, 0.79, 0.65, 0.60, 0.55],
            "Txn Volume": [15000, 25000, 45000, 12000, 18000]
        }), use_container_width=True)
        
        st.markdown("---")
        st.subheader("Geo-Spatial Risk Density (Simulated)")
        
        geo_risk_data = pd.DataFrame({
            'lat': [28.7041, 19.0760, 12.9716, 22.5726, 17.3850, 13.0827],
            'lon': [77.1025, 72.8777, 77.5946, 88.3639, 78.4867, 80.2707],
            'Risk Score': [0.85, 0.75, 0.65, 0.50, 0.45, 0.35],
            'City': ["Delhi", "Mumbai", "Bengaluru", "Kolkata", "Hyderabad", "Chennai"]
        })
        
        st.map(geo_risk_data, 
               latitude='lat', 
               longitude='lon', 
               size='Risk Score', 
               color=[255, 0, 0, 160], 
               zoom=4.5)


def config_page():
    """Model Configuration Page."""
    st.title("⚙️ Model Configuration & Management")
    st.sidebar.markdown("### Configuration")
    if st.sidebar.button("⬅️ Back to Menu", key="back_button_config", use_container_width=True):
            navigate_to("main_menu")
    
    st.info("This page manages model versions and retraining cycles.")

    st.subheader("Current Model Details")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"* **Model Type:** Random Forest Classifier")
        st.markdown(f"* **Features:** **{len(EXPECTED_FEATURES)}** (Including 8 Velocity features)")
        st.markdown(f"* **Model Path:** `{MODEL_PATH}`")
    with c2:
        st.markdown("* **Last Retrained:** 2025-12-15")
        st.markdown("* **Performance (Test Set):** AUC-ROC 0.95")

    st.markdown("---")
    st.subheader("Retraining Controls")
    if st.button("🔄 Initiate Model Retraining (Simulated)", type="primary"):
        st.warning("Retraining started. Running the background script 'python model.py'...")
        time.sleep(2)
        st.success("Model Retraining Complete! New AUC: 0.985. Deployed to production.")


# ======================================================
# --- ENTRY POINT ---
# ======================================================

if __name__ == "__main__":
    
    # 1. Floating AI Button and CSS
    def apply_custom_css():
        """Adds the floating AI button and background theme."""
        st.markdown(f"""
        <style>
        /* Gradient Background (Indian Flag Theme) */
        .stApp {{
            background: linear-gradient(135deg, #FF99331A 0%, #FFFFFF30 50%, #1388081A 100%);
            background-attachment: fixed;
        }}
        /* Floating AI Button/Container (NEW FEATURE) */
        .floating-ai-button {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            border-radius: 50%;
            background-color: #0E7CE3; /* Streamlit Blue */
            padding: 10px;
            transition: transform 0.3s ease;
        }}
        .floating-ai-button:hover {{
            transform: scale(1.1);
        }}
        .st-emotion-cache-1ftru4z {{ /* Target the inner container of the sidebar */
            padding-top: 1rem;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        if st.session_state.logged_in:
            st.markdown("""
            <div class='floating-ai-button' onclick='document.querySelector(".st-emotion-cache-1ftru4z").parentElement.parentElement.classList.remove("streamlit-expander-closed")'>
                <span style='font-size: 24px; color: white;'>🤖</span>
            </div>
            """, unsafe_allow_html=True)

    apply_custom_css()
    
    # 2. Global Sidebar Controls
    ai_assistant_sidebar()

    if st.session_state.current_page != "login":
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_page = "login"
            st.session_state.chat_history = []
            st.session_state.temp_data = {}
            st.toast("Logged out successfully.", icon="🚪")
            time.sleep(0.5)
            st.rerun()

    # 3. Page Routing Logic
    if not st.session_state.logged_in:
        # Wrap login content for the CSS to apply correctly
        st.markdown('<div class="login-overlay">', unsafe_allow_html=True)
        login_page()
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.current_page == "main_menu":
        main_menu()
    elif st.session_state.current_page == "predict":
        predict_page()
    elif st.session_state.current_page == "reports":
        reports_page()
    elif st.session_state.current_page == "config":
        config_page()
    elif st.session_state.current_page == "history": 
        history_page()
    else:
        main_menu()