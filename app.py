import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
from sklearn.linear_model import LinearRegression
from flask import Flask, jsonify

# Initialize Firebase Admin SDK (Ensure the service account key is provided)
app = Flask(__name__)
if not firebase_admin._apps:
    cred = credentials.Certificate("personal-finance-app-650d0-firebase-adminsdk-n3err-30850a5232.json")  # Update this path
    firebase_admin.initialize_app(cred)


def analyze_and_create_budget(historical_data, savings_percentage=20):
    # Analyze trends and compute averages
    total_income = 0
    category_trends = {}

    for category, data in historical_data.items():
        if len(data) < 2:
            continue

        # Calculate trend using linear regression
        X = np.arange(len(data)).reshape(-1, 1)  # Time indices
        y = np.array(data).reshape(-1, 1)  # Spending data
        model = LinearRegression()
        model.fit(X, y)

        # Predict next year's spending
        predicted_next_spending = model.predict([[len(data)]])[0][0]
        category_trends[category] = predicted_next_spending
        total_income += predicted_next_spending

    # Check if we have any valid data
    if total_income == 0:
        return {"error": "No historical data available to create a budget."}

    # Calculate predicted budget
    budget = {}
    for category, predicted_spending in category_trends.items():
        budget[category] = (predicted_spending / total_income) * (100 - savings_percentage)

    # Add savings
    budget["Savings"] = (savings_percentage / 100) * total_income

    return budget


def fetch_historical_data(user_id, year):
    # Get Firestore client
    db = firestore.client()
    historical_data = {}

    try:
        # Reference to the user's expense collection for the year
        year_ref = db.collection("users").document(user_id).collection("expense").document(str(year))

        # Loop through each month (1 to 12)
        for month in range(1, 13):
            month_ref = year_ref.collection(str(month))

            # Fetch all documents for the current month
            docs = month_ref.stream()
            for doc in docs:
                data = doc.to_dict()
                category = data.get("category", "Uncategorized")  # Default to "Uncategorized" if missing
                amount = data.get("amount", 0.0)  # Default to 0.0 if amount is missing

                if category not in historical_data:
                    historical_data[category] = [0.0] * 12  # Initialize with zeros for 12 months

                # Add the amount to the correct month (index is month - 1)
                historical_data[category][month - 1] += amount

        return historical_data

    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return {}


@app.route('/<string:user_id>/<int:year>', methods=['GET'])
def get_budget(user_id, year):
    try:
        # Fetch historical data for the user and year
        historical_data = fetch_historical_data(user_id, year)

        # Analyze data and create a budget
        budget = analyze_and_create_budget(historical_data)

        return jsonify(budget), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
