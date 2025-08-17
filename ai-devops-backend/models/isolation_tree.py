import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

# Load training data
logs_df = pd.read_csv("synthetic_logs.csv")
tasks_df = pd.read_csv("synthetic_tasks.csv")
metrics_df = pd.read_csv("synthetic_metrics.csv")

print("Logs columns:", logs_df.columns.tolist())
print("Tasks columns:", tasks_df.columns.tolist())
print("Metrics columns:", metrics_df.columns.tolist())

# --- Preprocess LOGS ---
# Encode categorical columns (log_level + component)
logs_df['log_level_enc'] = LabelEncoder().fit_transform(logs_df['log_level'])
logs_df['component_enc'] = LabelEncoder().fit_transform(logs_df['component'])
logs_features = logs_df[['log_level_enc', 'component_enc']]

# --- Preprocess TASKS ---
tasks_df['status_enc'] = LabelEncoder().fit_transform(tasks_df['status'])
tasks_df['priority_enc'] = LabelEncoder().fit_transform(tasks_df['priority'])
tasks_features = tasks_df[['status_enc', 'priority_enc']]

# --- Preprocess METRICS ---
metrics_features = metrics_df[['cpu_usage', 'memory_usage', 'disk_io', 'network_latency']]

# --- Combine all into one dataset ---
combined_features = pd.concat([logs_features, tasks_features, metrics_features], axis=1)

# --- Train Isolation Forest ---
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(combined_features)

# --- Save trained model ---
joblib.dump(model, "trained_model.pkl")
print("✅ Model trained and saved to trained_model.pkl")
