import os
import pandas as pd
import lightgbm as lgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# -------- CONFIG --------
DATA_PATH = "Version 4/data/processed/cbc_dataset_final.csv"
MODEL_PATH = "Version 4/models/lightgbm_disease_model.pkl"
TARGET_ENCODER_PATH = "Version 4/models/label_encoder.pkl"
FEATURE_ENCODERS_PATH = "Version 4/models/feature_encoders.pkl"
os.makedirs("Version 4/models", exist_ok=True)
# ------------------------

# ✅ Load data
df = pd.read_csv(DATA_PATH)

# ✅ Split into X and y
X = df.drop(columns=["Disease"])
y = df["Disease"]

# ✅ Encode string features (CBC status like 'Low', 'High') using LabelEncoder
feature_encoders = {}
for col in X.select_dtypes(include='object').columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    feature_encoders[col] = le

# ✅ Encode the target
target_encoder = LabelEncoder()
y_encoded = target_encoder.fit_transform(y)

# ✅ Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# ✅ LightGBM Dataset
train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_test, label=y_test)

# ✅ Model Parameters
params = {
    "objective": "multiclass",
    "num_class": len(target_encoder.classes_),
    "metric": "multi_logloss",
    "verbosity": -1
}

# ✅ Train Model with Callbacks (early stopping)
print("📈 Training LightGBM model...")
model = lgb.train(
    params,
    train_data,
    valid_sets=[val_data],
    num_boost_round=100,
    callbacks=[
        lgb.early_stopping(stopping_rounds=10),
        lgb.log_evaluation(period=10)
    ]
)

# ✅ Evaluate
y_pred = model.predict(X_test)
y_pred_labels = y_pred.argmax(axis=1)

print("\n🧾 Classification Report:")
print(classification_report(y_test, y_pred_labels, target_names=target_encoder.classes_))

# ✅ Save model and encoders
joblib.dump(model, MODEL_PATH)
joblib.dump(target_encoder, TARGET_ENCODER_PATH)
joblib.dump(feature_encoders, FEATURE_ENCODERS_PATH)

print(f"\n✅ Model saved to: {MODEL_PATH}")
print(f"✅ Target encoder saved to: {TARGET_ENCODER_PATH}")
print(f"✅ Feature encoders saved to: {FEATURE_ENCODERS_PATH}")
