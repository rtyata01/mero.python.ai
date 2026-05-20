# ==========================================
# MINIMAL PRODUCTION ML PIPELINE
# ==========================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
import joblib

# ==========================================
# STEP 1 — SAMPLE DATA
# ==========================================

data = {
    "amount": [100, 2500, 50, 5000, 120, 3000, 80, 7000, 200, 1500],
    "transaction_count": [2, 25, 1, 40, 3, 30, 2, 50, 5, 15],
    "account_age_days": [400, 30, 800, 10, 365, 20, 900, 5, 600, 90],
    "is_fraud": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

print("\n=== RAW DATA ===")
print(df)

# ==========================================
# STEP 2 — VALIDATION
# ==========================================

required_columns = [
    "amount",
    "transaction_count",
    "account_age_days",
    "is_fraud"
]

for col in required_columns:
    assert col in df.columns, f"Missing column: {col}"

assert df.isnull().sum().sum() == 0, "Dataset contains null values"

print("\n=== VALIDATION PASSED ===")

# ==========================================
# STEP 3 — FEATURE ENGINEERING
# ==========================================

# Log transform amount
df["log_amount"] = np.log1p(df["amount"])

# Fraud-risk ratio feature
df["txn_per_day"] = (
    df["transaction_count"] /
    (df["account_age_days"] + 1)
)

print("\n=== TRANSFORMED DATA ===")
print(df)

# ==========================================
# STEP 4 — PREPARE TRAINING DATA
# ==========================================

X = df[
    [
        "log_amount",
        "transaction_count",
        "account_age_days",
        "txn_per_day"
    ]
]

y = df["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================
# STEP 5 — BUILD ML PIPELINE
# ==========================================

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression())
])

# ==========================================
# STEP 6 — TRAIN MODEL
# ==========================================

pipeline.fit(X_train, y_train)

print("\n=== MODEL TRAINED ===")

# ==========================================
# STEP 7 — EVALUATE MODEL
# ==========================================

y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n=== EVALUATION ===")
print(f"Accuracy: {accuracy:.2f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ==========================================
# STEP 8 — SAVE MODEL
# ==========================================

joblib.dump(pipeline, "fraud_model.pkl")

print("\n=== MODEL SAVED ===")
print("Saved as fraud_model.pkl")

# ==========================================
# STEP 9 — LOAD MODEL
# ==========================================

loaded_model = joblib.load("fraud_model.pkl")

print("\n=== MODEL RELOADED ===")

# ==========================================
# STEP 10 — TEST NEW PREDICTIONS
# ==========================================

new_transactions = pd.DataFrame({
    "log_amount": [np.log1p(6000), np.log1p(90)],
    "transaction_count": [45, 2],
    "account_age_days": [7, 700],
    "txn_per_day": [
        45 / (7 + 1),
        2 / (700 + 1)
    ]
})

predictions = loaded_model.predict(new_transactions)

print("\n=== NEW PREDICTIONS ===")

for i, pred in enumerate(predictions):
    label = "FRAUD" if pred == 1 else "NOT FRAUD"
    print(f"Transaction {i+1}: {label}")