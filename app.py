import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
from sklearn.linear_model import LinearRegression
from flask import Flask, jsonify
from cryptography.fernet import Fernet
import json

# Initialize Firebase Admin SDK (Ensure the service account key is provided)
app = Flask(__name__)
key= b'9Nng6r-V-wHuIQYAUCdbv6yiegWfwYBsmHlU8NDL8Vw='
d=b'gAAAAABne7Me2dJZKRdXKvVj-OGR1zmTjjFfZYhn1hQylzuICG2oyxt-NxIcFTqLXOVqSptacI5txgDP6rUNOIi6goft_riJUMYX4SM2y87nj1rj_1l0qS7Rzo-hgxW9M0NvtinotTgfhwR0oi9P0NwJ2I5KVN8hphJHlR5-T1ST-N4CziVH0856ALtVGAhDT0X-oLQLBdjfdLDSDbgb1legn5dL9cc7ULnbLgmHkV8jOcM1YUYb2PY2dhjPKv3GDY-_hnLIoNv3IZJkLV7RSHUFP75z0-1-Loi1pV-qa3Kq_djMTZd5PcYfSl0GKQL5WxfdGtzGB45Y4AT0ynyaP1LDufWXvNLiSV0nfaJyph2KjpsDgubOC7kBEOHFXXI0rl64rE5hU87wJ2ZSxkkE8x7JYb-Nrm2mb3Hwr6OfunaB1lxWSmnSgo5CbrRdJsuHuYFCpyzsx63EaIAy-jtNneMR9quxpiVyVVv8T2mPo0h36rdU2nKlJJ7drqT5IKPZYqNcyAWYL966PurArXlrFrLJabMMl9AbnF3AvagAc0lgT6oo0imbxEnjxBeBGn1HS0hPb-7nYl-Zv85Ka6Ic7OXKGHZ0s-sIwIptYvZCvQx_o0LL7dC5zPztwpmPqYr_a3pF5EbmzBVdLjl-VBJaCWQr2BHEoR5dlsRummH3zeMLH86Bxon0XT74q3ZGrh4tZ0IjLt_mRIt9H6QnVabRLZJNXx0ZACeGPsvck4x_axEoUQa3MxP-qEsPe-XTul2abBQwp3defhZf9Mfsp9oex4JlTF8THY3u74KUBZmjZ0yVK6qnZN4HRciDCZsmUmM4b9Qutsu68ZWtUiy2YTALp4dPsWQgnIcSgwsATcVqvAofaQ1ew_kH5CZtgTMejrnwnoZHsC2BKCJemqhI4Dy0JTmn2MTdM9sM6iLvXtskAia883PXpKcDvoxoo7doqNkLd78OvAyLTPzVnFAg0edPuVuTFvejhE1W74gAi7m0bT456fxYluRCiLtvXWf8a777y2-052xVxenHmfVRn4nEh5TllRA2Y5ANVMYpyyKQpIqWDd2GHRznJOspVeC4aPAJWya9_-piu16BHpiKqCwq-LVVWjIpTdA3mwsQkarRVQbL1G2Hx-_2z5giFjyjQAW8xjNFs-OPPByGh5UUyjvs2i8oQAuu50aUDLyUCG6R7y3KWFl8owmkTHTug72LToc0qEYumur5hjO_mmzyYkdsunb1e15W-fqWdFhVsNUMQQd-Qqll1rn9FuX0fgBnWdgz6KkSodPq4y3-QhvQmqiLZct7pXpf3Ao9Dxi_69d1ZI_4TB4XOEKBIb4sbnoH7_bKo8fah4-Dsxi6obE5aCiVJcfakjC0D7n_NkGshOIGc92tEx12QJBNFjgWS4Dc_1v7abyYrYD6mZ6Ls1ONqxIj9ZG3wValPOa74LDmnlKq77hRnT2o3ne8lIiiUuFHZOVtqEzndO2n4jC5NGfQLiHNu9nDYKT3clRa65lj1xfpSQt-3yCcTfDTfvZc27sQQiza2glyA4KrdCnIlyzabUv8M2aVrsp91uPTj344yIcV2A2IG77oVslO8lFT1na3I-eIkkeaj8GPd5D3Y-cuvb38LhjVa9gIrKizd1skPDE-uP9GcRww9XgKnbTMxDYd738xh1SSFxY_JzemkDsABa0yBSVfjPe67eepFPDDi31SJv8F1eft9kbwWXtCOFhC4vcUuKPX5RQlvvU45-lvbcqrUBzDTViqcQTOZvSIdk1Z6m4kQBzy6TTrR91SPuGMtWD8b0zrTM5KUNU2JzoqG-w-glN5zeW0pz-RsLGV95V2A09ndo9om0lj586AbktQCF3fcDnWqTMd2t0J2_T5kSbDgsBQ5NfaRhq9zJIJuhlbE7Stkhk-3C4fGFazputiLaGZQHXTyQ9A8tv9hJCn2pPrXdLj-oA_uIGovZvaJ5fQ4bC779m8VwJjIdcYPRkJftW-XE3pgzqnOeZ8NavLYo7O4dUKpMPsfc7WldfaKNKNdIq3QefKZCwOe_fhNpjBbN3-nbroPqurghts6uz7HeeI5OUk56YvMzqsl8bxCtzDK3kjG_TKUr4NLbsPFB9trtzOclQYRzunv6NCxshlXPNxtWKrXwlZmotwbnwo4TN4op-2DPn11xSrxU4s8OlWzOxd6Hbssw8ZjaZXtj2wMj8bDfS1TmQ8eK7lJ8hOyHvpsAH-zVsEdis6CwYF2uGi7DtvtXqBvS-iRIAbJW56p6cQZVMCiBsNgdBKTgJMWbaD5Azt57HhyQDJTFs7AmBeAV25UQExHVdSU437GinWJht04oZ-CfyOI4napfJZsT0-5v1QJCvyF8NNMaTeGC-3d8JX6y76CBhmynbLptsRGLNtr46srYuu38pU-ZSa2OOefch4lyoLmv3ibzmuQV7NHPaNjDA9B6A6MFqkUADRBf6Gc3jSkkP2Lb10W6gMtgflgwQooJXT5zFH83o1v13S734pCx6PdW8x0n84GfoMLSQj2TDAWt66dJAIXpMeREWF6rgN-ZHmgKtOd5OBaePyw_y0DBJ2c7ij0NolYyjUJquIth_Q1wjVHd8Dv69J7a_GEt5jPBPY7vPOQb3hKpGrV5RnbFV3L3YFDKNH4ZPijnImQOVezgpYfg7_-JljEPnAGuYaItJ9-ukvox-ZfEBGAY0hA7ZXrxLwK4XKuSKT_quTk_Lwd0G7dgHytfVk2TLar0eEi8-X9riz8PjqkHP9Ll93PAyzskDRWmL0E5GTALRoK714WTBr_Qa3zP8lzGdN2br0GTXjFPCtz7GC1m3cXfvgt-mdGG9mCHyURRzDGk0LPQH_ygeBKqXQaeUbsQqQRe79Sftjslv-CV7VxVygNPgcWyZQ9QBRCDgpqvFonDPqTVTX_deagyZsaWNeFb22u2PI4Dx1Af5nLestVt8yP3kWMehmENfuBP9q7b04CrApB-jO_BJBab29KlLWK_OUxRbny3GSzKavGci2pQ4pEvaj5DYSKiVSqWv0L_NKkBovdpKBsv2Pt6uofdWAfiyJ0J8oSM80ojaefjgfiJWYGlT1DdEcr-M9ZDANxBRVIrzTPO75UbfRQobJG_SVEy_mnc1PnN0y7_bpkiWDDbrc4ACvBvK9YqDG2i3LIc1E19iWlkcp4e3kAaGCz_7_fvKQ2-CtugmpfIsGQ0Ib8MI5XqpNYr_cbUQ6e91QkllDHV1N4NpFyf-tiE2dYSKSIljsfVf50HzRLs3v72zTQuDKggJnLKB4wgmCNFV3'



def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data.decode()



if not firebase_admin._apps:
    
    decrypted_data = decrypt_data(d, key)
    d1=decrypted_data.strip("'")
    d2=d1.strip("'")
    d3= json.loads(d2)
    cred = credentials.Certificate(d3)  # Update this path
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

@app.roout('/')
def welcome():
    return jsonify({"welcome": "Runninh"}),200
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
