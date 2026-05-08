import os
import jwt
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Pobieranie tajnych danych z .env
SECRET_KEY = os.getenv("JWT_SECRET")
VALID_USER = os.getenv("ADMIN_LOGIN")
VALID_PASS = os.getenv("ADMIN_PASSWORD")

@app.route('/login', methods=['POST'])
def login():
    dane = request.json
    
    # Sprawdzamy czy uzytkownik przeslal login i haslo
    if not dane or 'login' not in dane or 'haslo' not in dane:
        return jsonify({"blad": "Brak danych logowania"}), 400

    # Sprawdzamy czy dane sa poprawne (zgodne z plikiem .env)
    if dane['login'] == VALID_USER and dane['haslo'] == VALID_PASS:
        # Generujemy token JWT ważny przez 1 godzinę
        waznosc_tokenu = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        token = jwt.encode({"user": dane['login'], "exp": waznosc_tokenu}, SECRET_KEY, algorithm="HS256")
        
        return jsonify({"wiadomosc": "Zalogowano pomyslnie", "token": token}), 200
    
    return jsonify({"blad": "Nieprawidlowy login lub haslo"}), 401

@app.route('/verify', methods=['POST'])
def verify():
    # Ten endpoint sluzy main-service do sprawdzania czy token jest wazny
    dane = request.json
    token = dane.get("token")

    if not token:
        return jsonify({"wazny": False, "blad": "Brak tokenu"}), 400

    try:
        # Probujemy rozszyfrowac token naszym kluczem
        zdekodowane = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"wazny": True, "uzytkownik": zdekodowane["user"]}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"wazny": False, "blad": "Token wygasl"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"wazny": False, "blad": "Nieprawidlowy token"}), 401

if __name__ == '__main__':
    # Odpalamy na porcie 5001 (wewnatrz dockera)
    app.run(host='0.0.0.0', port=5001)