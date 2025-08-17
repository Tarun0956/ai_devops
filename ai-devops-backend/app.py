# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load trained model once (with error handling)
try:
    model = joblib.load(os.path.join("models", "trained_model.pkl"))
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("⚠️ Model file not found. Some endpoints may not work.")
    model = None

# Load the JSON data files
def load_json_data():
    try:
        with open("mock_data/logs.json", "r") as f:
            logs_data = json.load(f)
        with open("mock_data/tasks.json", "r") as f:
            tasks_data = json.load(f)
        with open("mock_data/metrics.json", "r") as f:
            metrics_data = json.load(f)
        return logs_data, tasks_data, metrics_data
    except FileNotFoundError as e:
        print(f"⚠️ Data files not found: {e}")
        return [], [], []

@app.route("/logs", methods=["GET"])
def get_logs():
    logs_data, _, _ = load_json_data()
    return jsonify(logs_data)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    _, tasks_data, _ = load_json_data()
    return jsonify(tasks_data)

@app.route("/metrics", methods=["GET"])
def get_metrics():
    _, _, metrics_data = load_json_data()
    return jsonify(metrics_data)

@app.route("/insights", methods=["GET", "POST"])
def insights():
    try:
        if request.method == "POST":
            # Handle POST request with JSON data
            data = request.get_json()
            logs = pd.DataFrame(data["logs"])
            tasks = pd.DataFrame(data["tasks"])
            metrics = pd.DataFrame(data["metrics"])
        else:
            # Handle GET request - load from files
            logs_data, tasks_data, metrics_data = load_json_data()
            if not logs_data or not tasks_data or not metrics_data:
                return jsonify({"insights": ["⚠️ No data available for analysis"]})
            
            logs = pd.DataFrame(logs_data)
            tasks = pd.DataFrame(tasks_data)
            metrics = pd.DataFrame(metrics_data)

        if model is None:
            # Return mock insights if model is not available
            mock_insights = [
                "🔥 CPU usage trending upward - consider scaling resources",
                "✅ Memory usage stable across all components", 
                "⚡ Network latency spikes detected during peak hours",
                "⚠️ Error rate in components higher than normal",
                "📈 Task completion rate improved by 15% this week",
                "🔧 Disk I/O bottleneck identified in operations",
                "🎯 Recommended optimization: implement caching layer"
            ]
            return jsonify({"insights": mock_insights})

        # --- Preprocess LOGS ---
        if not logs.empty:
            logs["log_level_enc"] = LabelEncoder().fit_transform(logs["log_level"])
            logs["component_enc"] = LabelEncoder().fit_transform(logs["component"])
            logs_features = logs[["log_level_enc", "component_enc"]]
        else:
            logs_features = pd.DataFrame(columns=["log_level_enc", "component_enc"])

        # --- Preprocess TASKS ---
        if not tasks.empty:
            tasks["status_enc"] = LabelEncoder().fit_transform(tasks["status"])
            tasks["priority_enc"] = LabelEncoder().fit_transform(tasks["priority"])
            tasks_features = tasks[["status_enc", "priority_enc"]]
        else:
            tasks_features = pd.DataFrame(columns=["status_enc", "priority_enc"])

        # --- Preprocess METRICS ---
        if not metrics.empty:
            metrics_features = metrics[["cpu_usage", "memory_usage", "disk_io", "network_latency"]]
        else:
            metrics_features = pd.DataFrame(columns=["cpu_usage", "memory_usage", "disk_io", "network_latency"])

        # Check if we have enough data
        if logs_features.empty or tasks_features.empty or metrics_features.empty:
            return jsonify({"insights": ["⚠️ Insufficient data for anomaly detection"]})

        # --- Combine into SAME structure as training ---
        # Make sure all DataFrames have the same length
        min_length = min(len(logs_features), len(tasks_features), len(metrics_features))
        if min_length == 0:
            return jsonify({"insights": ["⚠️ No data available for analysis"]})

        logs_features = logs_features.head(min_length).reset_index(drop=True)
        tasks_features = tasks_features.head(min_length).reset_index(drop=True)
        metrics_features = metrics_features.head(min_length).reset_index(drop=True)

        X = pd.concat([logs_features, tasks_features, metrics_features], axis=1)

        # --- Predict anomalies ---
        preds = model.predict(X)

        insights = []
        anomaly_count = 0
        
        for i, p in enumerate(preds):
            if p == -1:  # Anomaly detected
                anomaly_count += 1
                insights.append(
                    f"⚠️ Anomaly detected at T{i+1}: "
                    f"CPU={X['cpu_usage'].iloc[i]}%, "
                    f"Memory={X['memory_usage'].iloc[i]}%, "
                    f"DiskIO={X['disk_io'].iloc[i]}, "
                    f"Latency={X['network_latency'].iloc[i]}ms"
                )

        # Add summary insights
        if anomaly_count == 0:
            insights.append("✅ No anomalies detected - system operating normally")
        else:
            insights.append(f"🚨 {anomaly_count} anomalies detected out of {len(preds)} data points")

        # Add some additional insights based on data analysis
        if not metrics.empty:
            avg_cpu = metrics['cpu_usage'].mean()
            avg_memory = metrics['memory_usage'].mean()
            max_latency = metrics['network_latency'].max()

            if avg_cpu > 80:
                insights.append("🔥 High CPU usage detected - consider resource scaling")
            elif avg_cpu < 30:
                insights.append("💡 Low CPU usage - potential for resource optimization")

            if avg_memory > 85:
                insights.append("⚠️ High memory usage - monitor for memory leaks")
            
            if max_latency > 150:
                insights.append("🐌 High network latency detected - check network performance")

        return jsonify({"insights": insights})

    except Exception as e:
        print(f"Error in insights endpoint: {e}")
        return jsonify({
            "insights": [
                f"❌ Error generating insights: {str(e)}",
                "🔧 Please check data format and model availability"
            ]
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "endpoints": ["/logs", "/tasks", "/metrics", "/insights", "/health"]
    })

if __name__ == "__main__":
    print("🚀 Starting AI DevOps Backend...")
    print("📊 Available endpoints:")
    print("  - GET  /logs")
    print("  - GET  /tasks") 
    print("  - GET  /metrics")
    print("  - GET  /insights")
    print("  - POST /insights")
    print("  - GET  /health")
    app.run(host="0.0.0.0", port=5001, debug=True)