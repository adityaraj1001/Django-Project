import pandas as pd
import joblib
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

# ==================================================
# DATA & PATH SETUP (FIXED FOR PORTABILITY)
# ==================================================
DATA_PATH = "upi_transactions_2024.csv" 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "fraud_model.pkl")

# Ensure the 'model' directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# ==================================================
# LOAD & PREPARE DATA
# ==================================================
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"Dataset not found at: {DATA_PATH}")
    raise

# Clean and rename columns
df.columns = df.columns.str.lower().str.strip()
df = df.rename(columns={"amount (inr)": "amount"})

# --- FEATURE ENGINEERING ---
df['sender_bank_risk'] = 0.5 
df['receiver_bank_risk'] = 0.5
df['is_weekend'] = df['is_weekend'].astype(int)

# Clean categorical features
df['sender_age_group'] = df['sender_age_group'].fillna('Unknown')
df['receiver_age_group'] = df['receiver_age_group'].fillna('Unknown')
df['transaction type'] = df['transaction type'].fillna('Unknown')
df['merchant_category'] = df['merchant_category'].fillna('Unknown')
df['sender_state'] = df['sender_state'].fillna('Unknown')


# -----------------------------------------------------------------
# --- FIX APPLIED: Velocity and Frequency Features ---
# -----------------------------------------------------------------
df['timestamp'] = pd.to_datetime(df['timestamp'])
# CRITICAL FIX 1: Set 'timestamp' as the index before grouping
df = df.sort_values('timestamp').set_index('timestamp') 

def create_velocity_features(df, entity_col, time_window, prefix):
    """Calculates transaction count and average amount in a rolling time window."""
    
    # CRITICAL FIX 2: Removed on='timestamp' since it is the index now.
    # Count of transactions by entity (sender/receiver) in the last X hours
    # We apply the rolling count on 'amount' or any non-NaN column for efficiency
    df[f'{prefix}_txn_count_{time_window}h'] = df.groupby(entity_col)['amount'].transform(
        lambda x: x.rolling(f'{time_window}h', closed='left').count()
    ).fillna(0)
    
    # Average transaction amount by entity in the last X hours
    df[f'{prefix}_avg_amount_{time_window}h'] = df.groupby(entity_col)['amount'].transform(
        lambda x: x.rolling(f'{time_window}h', closed='left').mean()
    ).fillna(0)
    return df

# Create 1-hour and 24-hour velocity features for Sender and Receiver
df = create_velocity_features(df, 'sender_bank', 1, 'sender')
df = create_velocity_features(df, 'sender_bank', 24, 'sender')
df = create_velocity_features(df, 'receiver_bank', 1, 'receiver')
df = create_velocity_features(df, 'receiver_bank', 24, 'receiver')

# Put 'timestamp' back as a column and reset the index
df = df.reset_index(drop=False) 
# -----------------------------------------------------------------


# --- TARGET & FEATURE SELECTION ---
# Ensure 'timestamp' is in the drop list now that it is back as a column
X = df.drop(columns=['fraud_flag', 'transaction id', 'timestamp', 'transaction_status'])
y = df['fraud_flag']

# --- FEATURE LISTS (23 Features Total) ---
numeric_features = [
    "amount", "hour_of_day", "is_weekend", "sender_bank_risk", "receiver_bank_risk",
    "sender_txn_count_1h", "sender_avg_amount_1h", "sender_txn_count_24h", "sender_avg_amount_24h",
    "receiver_txn_count_1h", "receiver_avg_amount_1h", "receiver_txn_count_24h", "receiver_avg_amount_24h",
]

categorical_features = [
    "day_of_week", "device_type", "network_type", "sender_bank", "receiver_bank",
    "transaction type", "merchant_category", "sender_state", "sender_age_group", "receiver_age_group",
]

# Select only the features the model will use
X = X[numeric_features + categorical_features]


# ==================================================
# PREPROCESSING & MODEL PIPELINE (Random Forest)
# ==================================================
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ],
    remainder='passthrough'
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=300,
                max_depth=18,
                min_samples_split=5,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1,
            ),
        ),
    ]
)

# ==================================================
# TRAIN & SAVE MODEL
# ==================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Starting model training...")
model.fit(X_train, y_train)
print("Model training complete.")

joblib.dump(model, MODEL_PATH)
joblib.dump(X.columns.tolist(), os.path.join(MODEL_DIR, "feature_list.pkl"))
print(f"Model saved successfully to: {MODEL_PATH}")