from flask import Flask, jsonify, request
from src.server_2.mqtt_config import init_mqtt, DEVICE_TOPIC
import json
app = Flask(__name__)

# Init mqtt client
mqtt_client, received_messages = init_mqtt()

@app.route('/send', methods=['POST'])
def send_message():
    try:
        content = request.json.get('message', '')
        content_str = json.dumps(content)
        print(content_str)
        if not content:
            return jsonify({"error": "No message provided"}), 400

        mqtt_client.publish(DEVICE_TOPIC, content_str)  # Gửi lệnh tới SERVICE_TOPIC
        return jsonify({"status": "Message sent", "message": content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "status": "Error",
        "code": 404,
        "message": "Not Found"
    }), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3032)
