import requests
import time
import os
import psycopg2
from flask import Flask, request, jsonify, send_file, Response
from saml import saml_login, saml_callback, get_data_from_token
import json


app = Flask(__name__)

# DeepL API key
DEEPL_API_KEY = '82a64fae-73d4-4739-9935-bbf3cfc15010'

# Replace with your DeepL API auth key
auth_key = "82a64fae-73d4-4739-9935-bbf3cfc15010"
translator = deepl.Translator(auth_key)

app.config["SECRET_KEY"] = "onelogindemopytoolkit"
app.config["SAML_PATH"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saml")
# SAML routes
@app.route('/saml/login')
def login():
    return saml_login(app.config["SAML_PATH"])

@app.route('/saml/callback', methods=['POST'])
def login_callback():
    return saml_callback(app.config["SAML_PATH"])

@app.route('/data_from_token', methods=['POST'])
def data_from_token():
    data = request.get_json()
    token = data.get('token')
    return get_data_from_token(token)
    

# Database connection details

    
if __name__ == '__main__':
    # Use the environment variable PORT, or default to port 5000 if not set
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
