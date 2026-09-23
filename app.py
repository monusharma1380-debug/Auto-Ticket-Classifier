import pandas as pd
from flask import Flask, render_template, request, jsonify
from utils.classify import classify
import os
import openpyxl
import gunicorn


app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/dashboard")
def home():
    return render_template("index.html")


def load_dataframe(uploaded_file):
    filename = uploaded_file.filename.lower()

    if filename.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif filename.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)
    elif filename.endswith(".json"):
        return pd.read_json(uploaded_file)
    else:
        raise ValueError(f"Unsupported file type: {filename}")


@app.route("/analyze", methods=["POST"])
def analyze():
    upload_file = request.files["file"]
    df = load_dataframe(upload_file)

    possible_names = ["query", "text", "ticket", "description", "message", "body"]

    text_column = None
    for col in df.columns:
        if col.lower() in possible_names:
            text_column = col
            break

    
    if text_column is None:
        raise ValueError(f"Couldn't find a text column. Available columns: {list(df.columns)}")

    result = []
    for _, row in df.iterrows():
        text = row[text_column]
        analysis = classify(text)
        analysis["id"] = row.get("id", _)
        analysis["text"] = row[text_column]
        result.append(analysis)

    result_df = pd.DataFrame(result)



    final_output = {
        "total_tickets": len(result_df),
        "high_priority_count": int((result_df["priority"] == "high").sum()),
        "category_summary": result_df["category"].value_counts().to_dict(),
        "priority_summary": result_df["priority"].value_counts().to_dict(),
        "tickets": result_df.to_dict(orient="records"),
    }
    return jsonify(final_output)

if __name__ == "__main__":
    app.run(debug=True)