import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# URL naszego drugiego serwisu w sieci Dockerowej (nazwa z docker-compose)
AUTH_SERVICE_URL = "http://auth-service:5001/verify"

@app.route('/secret', methods=['GET'])
def pobierz_dane():
    # Wyciagamy token z naglowka (Authorization: Bearer <token>)
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"blad": "Brak tokenu w naglowku Authorization"}), 401
    
    token = auth_header.split(" ")[1]

    # Uderzamy do auth-service z pytaniem, czy ten token jest ok
    try:
        odpowiedz = requests.post(AUTH_SERVICE_URL, json={"token": token})
        wynik = odpowiedz.json()

        if odpowiedz.status_code == 200 and wynik.get("wazny") == True:
            # Token poprawny, zwracamy tajne dane
            return jsonify({
                "wiadomosc": "Dostep przyznany!",
                "zalogowany_jako": wynik["uzytkownik"],
                "sekretne_informacje": "To sa tajne dane widoczne tylko po zalogowaniu."
            }), 200
        else:
            # Token niepoprawny
            return jsonify({"blad": wynik.get("blad", "Brak dostepu")}), 401

    except Exception as e:
        return jsonify({"blad": "Blad komunikacji z auth-service", "szczegoly": str(e)}), 500

if __name__ == '__main__':
    # Odpalamy na porcie 8000 (wystawionym publicznie)
    app.run(host='0.0.0.0', port=8000)