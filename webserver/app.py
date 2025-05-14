from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

LAMBDA_API_URL = os.environ.get("LAMBDA_API_URL")

@app.route('/')
def home():
    return "Benvenuto nel sistema ordini"

@app.route('/ordina', methods=['POST'])
def ordina():
    data = request.get_json()
    referenze = data.get("referenze")

    if not referenze or not isinstance(referenze, list):
        return jsonify({"error": "Fornisci una lista di referenze valida"}), 400

    try:
        response = requests.post(
            LAMBDA_API_URL,
            json={"referenze": referenze}
        )
        return jsonify({
            "esito": "Ordine ricevuto",
            "lambda_response": response.text
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
