# app.py
from flask import Flask, request, jsonify, render_template
from cryptography.fernet import Fernet

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_key', methods=['POST'])
def generate_key():
    key = Fernet.generate_key().decode()
    return jsonify({"key": key})

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    key = data['key'].encode()
    message = data['message'].encode()
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message)
    return jsonify({"encrypted_message": encrypted_message.decode()})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    key = data['key'].encode()
    encrypted_message = data['encrypted_message'].encode()
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message)
    return jsonify({"decrypted_message": decrypted_message.decode()})

if __name__ == '__main__':
    app.run(debug=True)