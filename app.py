from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = "5493329438"

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/send', methods=['POST', 'OPTIONS'])
def send_order():
    if request.method == 'OPTIONS':
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response

    try:
        data = request.get_json()
        print("Получены данные:", data)  # Лог на Render

        name = data.get('name', 'Не указано')
        phone = data.get('phone', 'Не указан')
        address = data.get('address', 'Не указан')
        timestamp = data.get('timestamp', '')

        message = f"📨 <b>НОВАЯ ЗАЯВКА</b>\n\n👤 <b>Имя:</b> {name}\n📞 <b>Телефон:</b> {phone}\n🏠 <b>Адрес:</b> {address}\n🕐 <b>Время:</b> {timestamp}"

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "error", "message": "Telegram API error"}), 500

    except Exception as e:
        print("Ошибка:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
