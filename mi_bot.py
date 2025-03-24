import requests
from flask import Flask, request

# Configuración: reemplaza estos valores con los tuyos
ACCESS_TOKEN = "EAAXsJvgzX60BO8vcI3sxd13YxO6A3KltZCDNavhHvZCZAMhL79cQVK5qCk8eDPUHXZBTYBt9CxZAGZAZAG0LUBm6JoRFuNSZBVBGVx1f4Ebt7n0MuIcXfynDoRxo1RUq7imuEkwTtpJqJizmcS8M81YtkfCUI8G1lhvwOu5VOi0x5WmYSan4at7nmNRJpU9GXmfzrYE5oc5mVgZDZD"
VERIFY_TOKEN = "susu_0102"

app = Flask(__name__)

# Ruta GET para la verificación del webhook
@app.route('/webhook', methods=['GET'])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge
    return "Error de verificación", 403

# Ruta POST para recibir mensajes
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'entry' in data:
        for entry in data['entry']:
            for message in entry.get('messaging', []):
                if 'message' in message:
                    sender_id = message['sender']['id']
                    text = message['message'].get('text', '')
                    responder_mensaje(sender_id, text)
    return "OK", 200

# Función para responder mensajes en Messenger
def responder_mensaje(sender_id, text):
    url = f"https://graph.facebook.com/v12.0/me/messages?access_token={ACCESS_TOKEN}"
    respuesta = {"recipient": {"id": sender_id}, "message": {"text": f"Recibí tu mensaje: {text}"}}
    headers = {"Content-Type": "application/json"}
    requests.post(url, json=respuesta, headers=headers)

if __name__ == "__main__":
    # Para Render se recomienda usar host "0.0.0.0" y un puerto como 8080
    app.run(host="0.0.0.0", port=8080)
