from flask import Flask, jsonify, request
from src.server_1.mqtt_config import init_mqtt
from flask_cors import CORS
from src.server_1.firebase_config import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

body_parameter = {
    "height": None,
    "weight": None,
    "age": None,
    "sex": None,
    "bmi": None
}

message_ref = db.reference('message')
mqtt_client = init_mqtt(message_ref, body_parameter)


# def on_message(event):
#     print(f"New message added in message db: {event.data}")


# message_ref.listen(on_message)


@app.route('/body/parameters', methods=['POST'])
def send_message():
    height = request.json.get('height')
    weight = request.json.get('weight')
    age = request.json.get('age')
    sex = request.json.get('sex')

    try:
        if not height or not weight or not age or not sex:
            raise Exception('lack of parameters')

        if (type(height) is not int or
                type(weight) is not int or
                type(age) is not int or
                type(sex) is not str):
            raise Exception('wrong type')

        if sex != 'Male' and sex != 'Female':
            raise Exception('wrong sex')

        body_parameter['height'] = height
        body_parameter['weight'] = weight
        body_parameter['age'] = age
        body_parameter['sex'] = sex
        body_parameter['bmi'] = weight / (height / 100)**2

        print(body_parameter)

        return jsonify({"status": "Sent successfully"}), 200
    except Exception as e:
        return jsonify({'status': "invalid infor", "message": str(e), 'infor': {
            "height": height,
            "weight": weight,
            "age": age,
            "sex": sex
        }}), 400


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "status": "Error",
        "code": 404,
        "message": "Not Found"
    }), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030)
