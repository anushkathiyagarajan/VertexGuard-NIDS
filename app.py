from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import joblib
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Load trained model
model = joblib.load("ids_model.pkl")

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Global storage
global_logs = []
global_total = 0
global_normal = 0
global_attacks = 0
global_features = []
global_importance = []


# ---------------- LOGIN ----------------
@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "admin":
        return redirect(url_for("index"))

    return "Invalid Login"


# ---------------- INDEX PAGE ----------------
@app.route("/index")
def index():
    return render_template("index.html")


# ---------------- PREDICTION ----------------
@app.route("/predict", methods=["POST"])
def predict():

    global global_logs, global_total, global_normal, global_attacks
    global global_features, global_importance

    file = request.files["file"]
    df = pd.read_csv(file)

    # Capture attack categories
    if "attack_cat" in df.columns:
        attack_categories = df["attack_cat"]
    else:
        attack_categories = pd.Series(["Normal"] * len(df))

    # Remove columns not used by model
    drop_cols = []

    if "label" in df.columns:
        drop_cols.append("label")

    if "attack_cat" in df.columns:
        drop_cols.append("attack_cat")

    X = df.drop(columns=drop_cols, errors="ignore")

    # Encode categorical columns
    for col in X.columns:
        if X[col].dtype == "object":
            X[col] = X[col].astype("category").cat.codes

    # Fix feature mismatch
    model_features = model.feature_names_in_
    X = X.reindex(columns=model_features, fill_value=0)

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)

    total = len(predictions)
    attacks = sum(1 for p in predictions if p == 1)
    normal = total - attacks

    logs = []

    for i, p in enumerate(predictions):

        dataset_type = str(attack_categories.iloc[i]).strip()

        attack_prob = probabilities[i][1]
        normal_prob = probabilities[i][0]

        attack_conf = round(attack_prob * 100, 2)
        normal_conf = round(normal_prob * 100, 2)

        if p == 1:

            # Show real attack type
            if dataset_type.lower() != "normal":
                attack_type = dataset_type
            else:
                attack_type = "Suspicious Traffic"

            logs.append({
                "row": i + 1,
                "prediction": "Attack",
                "type": attack_type,
                "confidence": attack_conf
            })

        else:

            logs.append({
                "row": i + 1,
                "prediction": "Normal",
                "type": "Normal",
                "confidence": normal_conf
            })

    # Save alerts
    with open("logs/alerts.log", "a") as f:

        for log in logs:

            if log["prediction"] == "Attack":

                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                f.write(
                    f"{time} | Row {log['row']} | Attack | {log['type']} | Confidence {log['confidence']}%\n"
                )

    # Feature importance
    try:

        importances = model.feature_importances_

        feature_importance = sorted(
            zip(model_features, importances),
            key=lambda x: x[1],
            reverse=True
        )

        features = [f[0] for f in feature_importance]
        importance = [float(f[1]) for f in feature_importance]

    except:

        features = list(model_features)
        importance = [0] * len(features)

    # Confidence graph values
    normal_conf_avg = round((probabilities[:,0].mean()) * 100, 2)
    attack_conf_avg = round((probabilities[:,1].mean()) * 100, 2)

    # Store globally
    global_logs = logs
    global_total = total
    global_normal = normal
    global_attacks = attacks
    global_features = features
    global_importance = importance

    return render_template(
        "result.html",
        total=total,
        normal=normal,
        attacks=attacks,
        logs=logs,   # show all logs
        features=features,
        importance=importance,
        normal_conf=normal_conf_avg,
        attack_conf=attack_conf_avg
    )


# ---------------- DOWNLOAD REPORT ----------------
@app.route("/download_report")
def download_report():

    global global_logs, global_total, global_normal, global_attacks

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = f"logs/intrusion_report_{timestamp}.pdf"

    c = canvas.Canvas(filepath, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(170, 750, "VertexGuard IDS Security Report")

    c.setFont("Helvetica", 12)

    y = 700

    c.drawString(50, y, f"Generated Time: {datetime.now()}")
    y -= 40

    c.drawString(50, y, f"Total Traffic: {global_total}")
    y -= 20

    c.drawString(50, y, f"Normal Traffic: {global_normal}")
    y -= 20

    c.drawString(50, y, f"Attack Traffic: {global_attacks}")
    y -= 40

    c.drawString(50, y, "Detection Logs")
    y -= 20

    for log in global_logs[:50]:

        text = f"Row {log['row']} | {log['prediction']} | {log['type']} | {log['confidence']}%"

        c.drawString(50, y, text)

        y -= 15

        if y < 50:
            c.showPage()
            y = 750

    c.save()

    with open("logs/alerts.log", "a") as f:
        f.write(f"{datetime.now()} | Report Generated | {filepath}\n")

    return send_file(filepath, as_attachment=True)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)