import joblib

catergory_model = joblib.load(r"Category_model.pkl")
category_vect = joblib.load(r"Category_vectorizer.pkl")
priority_model = joblib.load(r"Priority_model.pkl")
priority_vec = joblib.load(r"Priority_vectorizer.pkl")

ROUTE_MAP = {
    "Billing and Payments": "Finance Team",
    "Returns and Exchanges": "Finance Team",
    "Technical Support": "IT Team",
    "IT Support": "IT Team",
    "Product Support": "IT Team",
    "Human Resources": "HR Team",
    "Sales and Pre-Sales": "Sales Team",
    "Service Outages and Maintenance": "IT Team",
    "Customer Service": "Support Team",
    "General Inquiry": "Support Team",
}

def classify(ticket_text : str) -> dict:
    cat_vec = category_vect.transform([ticket_text])
    category = catergory_model.predict(cat_vec)[0]
    pri_vec = priority_vec.transform([ticket_text])
    priority = priority_model.predict(pri_vec)[0]

    return {
        "category" : str(category),
        "priority" : priority,
        "route_to" : ROUTE_MAP.get(category, "Support team")
        }

if __name__ == "__main__":
    result = classify("My payment got deducted twice, please refund urgently")
    print(result)